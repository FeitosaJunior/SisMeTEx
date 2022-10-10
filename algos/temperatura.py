
from datetime import date, datetime
import pandas as pd
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date


def graf_temp(session):
    # Pegar os dados - Mudar para a plataforma
    end_dados = 'C:/SisMetEx/toydata/' + session['station'] + '/'
    arq_final = 'dados_final.csv'
    df_arq_final = pd.read_csv(
        end_dados + arq_final, encoding='utf-8', sep=';').drop(columns='Unnamed: 0')

    # Pegar data
    data_inicio = str(session['startdate'])
    data_final = str(session['enddate'])
    # Transformar texto em data
    dt_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
    dt_final = datetime.strptime(data_final, '%Y-%m-%d')

    # Transformar datas
    for i in range(len(df_arq_final)):
        df_arq_final['Date'][i] = datetime.strptime(
            df_arq_final['Date'][i], '%Y-%m-%d %H:%M:%S')

    # Cortar o dataframe
    df_cort = df_arq_final[df_arq_final['Date'] < dt_final]
    df_cort = df_cort[df_arq_final['Date'] > dt_inicio]
    df_cort = df_cort.reset_index(drop=True)

    if len(df_cort) < 3:  # Se o corte tiver muitos poucos dados, mandar tudão
        df_cort = df_arq_final.copy()

    dates = df_cort['Date'].tolist()

    # Plot
    figure(figsize=(6, 4), dpi=100)
    plt.plot(dates, df_cort["Indoor Temperature(°C)"],
             color='#1C6E98', label='Temp. Interna')
    plt.plot(dates, df_cort["Outdoor Temperature(°C)"],
             color='#8E4021', label='Temp. Externa', linestyle='--')
    plt.xticks(rotation=30)

    # Labelling
    plt.xlabel("Date")
    plt.ylabel("Temperatura (°C)")
    plt.title("Temperaturas Interna e Externa - " +
              session['station'].replace('_', ' '))
    plt.legend(loc="upper right")
    # Display
    plt.show()
    return
