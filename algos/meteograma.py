
from datetime import date, datetime
import pandas as pd
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date

# Pegar os dados - Mudar para a plataforma
end_dados = 'C:/SisMetEx/toydata/Praia_Vermelha/'
arq_final = 'dados_final.csv'

df_arq_final = pd.read_csv(
    end_dados + arq_final, encoding='utf-8', sep=';').drop(columns='Unnamed: 0')

# Classe e definição do meteograma


class Variable(object):
    def __init__(self, style, data=None):
        try:
            self.label = style['label']
        except KeyError:
            self.label = None

        self._style = style
        self._ylim = None
        if data:
            self._dates = date2num(data[0])
            self._vals = data[1]
        else:
            self._dates = []
            self._vals = []

    def append(self, date, val):
        self._dates.append(date2num(date))
        self._vals.append(val)

    def plot(self, axis):
        axis.plot_date(self._dates, self._vals, **self._style)


class Fill(Variable):
    def __init__(self, style, data=None):
        super(Fill, self).__init__(style, data)

    def plot(self, axis):
        axis.fill_between(self._dates, self._vals, **self._style)


class Bar(Variable):
    def __init__(self, style, data=None):
        super(Bar, self).__init__(style, data)

    def plot(self, axis):
        axis.bar(self._dates, self._vals, **self._style)


# Registry of all Variable types currently implemented
PLOT_TYPES = {'line': Variable,
              'marker': Variable,
              'bar': Bar,
              'fill_to': Fill}


class SubPlot:
    def __init__(self, left_vars, right_var=None):
        self._left_axis = None
        self._left_label = None
        self._right_axis = None
        self._right_label = None

        self._left_ylim = None
        self._right_ylim = None
        try:
            self._left_vars = [var for var in left_vars]
        except Exception:
            self._left_vars = [left_vars]

        self._right_var = right_var

    @property
    def left_ylim(self):
        return self._left_ylim

    @left_ylim.setter
    def left_ylim(self, top_bottom):
        self._left_ylim = top_bottom

    @property
    def right_ylim(self):
        return self._right_ylim

    @right_ylim.setter
    def right_ylim(self, top_bottom):
        self._right_ylim = top_bottom

    def plot_vars(self, axis):
        self._left_axis = axis
        for var in self._left_vars:
            var.plot(axis)
        axis.legend(loc=2, frameon=False, numpoints=1)
        self._left_axis.set_xticklabels([num2date(d).strftime('%Y-%m-%dT%H:%M:%S') for d in
                                         self._left_axis.get_xticks()], rotation=30)
        if self.left_ylim:
            self._left_axis.set_ylim(self._left_ylim)

        # Make room for legends
        left_ylim = self._left_axis.get_ylim()
        ticks = self._left_axis.get_yticks()
        self._left_axis.set_ylim(top=left_ylim[1]*1.2)
        self._left_axis.set_yticks(ticks)

        if self._right_var:
            self._right_axis = axis.twinx()
            self._right_var.plot(self._right_axis)
            if self._right_ylim:
                self._right_axis.set_ylim(self._right_ylim)

            # Make room for legends
            right_ylim = self._right_axis.get_ylim()
            ticks = self._right_axis.get_yticks()
            self._right_axis.set_ylim(top=right_ylim[1]*1.2)
            self._right_axis.set_yticks(ticks)
            self._right_axis.legend(loc=1, frameon=False, numpoints=1)


class Meteogram(object):
    def __init__(self, subplots, title=None):
        """
        :param subplots: Order matters.  Plots will be plotted in order top to bottom with the last
                         subplot being the "anchor".
        :param title:
        """
        # Setup a figure for this meteogram, and alter the subplots so there is no whitespace between them.
        self.fig = plt.figure(facecolor='white', figsize=(15, 8))
        self._title = title
        plt.subplots_adjust(bottom=0.2, hspace=0.1)

        try:
            self._subplots = [plot for plot in subplots]
        except Exception:
            self._subplots = [subplots]
        self._plotted = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @classmethod
    def variable(cls, style, data=None):
        try:
            return PLOT_TYPES[style['plot_type']](style['mpl_options'], data)
        except KeyError:
            raise Exception('plot_type of %s is unknown.' % style['plot_type'])

    def show(self):
        self._plot()
        plt.show(self.fig)

    def save(self, fname, **kwargs):
        """
        :param fname:
        :param kwargs: Any of the valid args at http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.savefig
        :return:
        """
        self._plot()
        if 'bbox_inches' not in kwargs.keys():
            kwargs['bbox'] = 'tight'
        plt.savefig(fname, **kwargs)

    def _plot(self):
        num_subplots = len(self._subplots)
        for i, subplot in enumerate(self._subplots):
            var_axis = plt.subplot2grid((num_subplots, 3), (i, 0), colspan=3)
            self._plotted.append(var_axis)
            subplot.plot_vars(var_axis)

        # Go through each subplot except the last (bottom) and:
        # 1.) Align the x-axis with the bottom subplot
        # 2.) Remove x-ticks to clean up the plot
        for axis in self._plotted[:-1]:
            axis.set_xlim(*self._plotted[-1].get_xlim())
            axis.set_xticks([])

        self.fig.suptitle(self._title)


# Modelos Plot
Temperature = {'plot_type': 'line',
               'mpl_options': {'linestyle': '-',
                               'linewidth': 2,
                               'color': 'red',
                               'marker': None,
                               'label': 'Temp in C'}}

Dewpoint = {'plot_type': 'line',
            'mpl_options': {'linestyle': '-',
                            'linewidth': 2,
                            'color': 'green',
                            'marker': None,
                            'label': 'Dewpoint in C'}}

Precipitation = {'plot_type': 'bar',
                 'mpl_options': {'width': 0.01,
                                 'bottom': 0,
                                 'color': 'lightgreen',
                                 'edgecolor': 'green',
                                 'alpha': 0.5,
                                 'label': 'Precipitation in mm'}}

Freezing = {'plot_type': 'line',
            'mpl_options': {'linewidth': 1,
                            'linestyle': 'dashed',
                            'marker': None,
                            'color': 'blue',
                            'label': 'Freezing'}}

WindSpeed = {'plot_type': 'fill_to',
             'mpl_options': {'linestyle': '-',
                             'linewidth': 1,
                             'color': 'lightblue',
                             'edgecolor': 'blue',
                             'alpha': 0.5,
                             'label': 'Wind Speed in m/s'}}

WindDirection = {'plot_type': 'marker',
                 'mpl_options': {'marker': 'o',
                                 'markersize': 3,
                                 'color': 'blue',
                                 'label': 'Wind Direction in deg from North'}}


# New additions
Gust = {'plot_type': 'line',
        'mpl_options': {'linestyle': '-',
                        'linewidth': 1,
                        'color': 'green',
                        'marker': None,
                        'label': 'Gust in m/s'}}

AirHumidity = {'plot_type': 'fill_to',
               'mpl_options': {'linestyle': '-',
                               'linewidth': 1,
                               'color': 'lightblue',
                               'edgecolor': 'blue',
                               'alpha': 0.5,
                               'label': 'Air Humidity in %'}}

AbsolutePressure = {'plot_type': 'line',
                    'mpl_options': {'linestyle': '-',
                                    'linewidth': 1,
                                    'color': 'black',
                                    'marker': None,
                                    'label': 'Absolute Pressure in hpa'}}


def criar_mateograma(df, estacao):
    temperature_data = df['Indoor Temperature(°C)'].tolist()
    freezing_data = df['DewPoint(°C)'].tolist()
    precipitation_data = df['Hour Rainfall(mm)'].tolist()
    wind_speed_data = df['Wind Speed(m/s)'].tolist()
    wind_direction_data = df['Wind Direction Degrees from North'].tolist()
    gust_data = df['Gust(m/s)'].tolist()
    humidity_data = df['Indoor Humidity(%)'].tolist()
    pressure_data = df['Absolute Pressure(hpa)'].tolist()

    datas_df = df['Date'].tolist()
    dates = datas_df.copy()
    for i in range(len(datas_df)):
        dates[i] = datetime.strptime(datas_df[i], '%Y-%m-%d %H:%M:%S')

    temp = Meteogram.variable(Temperature, [dates, temperature_data])
    freezing = Meteogram.variable(Freezing, [dates, freezing_data])
    prec = Meteogram.variable(Precipitation, [dates, precipitation_data])

    wind_speed = Meteogram.variable(WindSpeed, [dates, wind_speed_data])
    wind_direction = Meteogram.variable(
        WindDirection, [dates, wind_direction_data])

    gust_speed = Meteogram.variable(Gust, [dates, gust_data])

    humidity = Meteogram.variable(AirHumidity, [dates, humidity_data])
    pressure = Meteogram.variable(AbsolutePressure, [dates, pressure_data])

    #nome_estação = 'Praia Vermelha'
    nome_estação = estacao

    # Plot both freezing and temp on the same axis and subplot
    temp_plot = SubPlot(left_vars=(temp, freezing), right_var=prec)

    # Plot wind speed on left axis, wind direction on right, but still on same subplot
    wind_plot = SubPlot(left_vars=(wind_speed, gust_speed),
                        right_var=wind_direction)
    wind_plot.right_ylim = (0, 300)

    # Plot wind speed on left axis, wind direction on right, but still on same subplot
    pressure_plot = SubPlot(left_vars=(humidity), right_var=pressure)
    pressure_plot.left_ylim = (0, 100)
    pressure_plot.right_ylim = (500, 1500)

    meteogram = Meteogram((wind_plot, temp_plot, pressure_plot))
    meteogram.title = "Meteograma - " + nome_estação
    meteogram.show()

    return


criar_mateograma(df_arq_final, 'Praia Vermelha')
