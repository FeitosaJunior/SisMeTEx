
from datetime import date, datetime
import pandas as pd
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date


def mult_graficos(session):
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

    fig, axs = plt.subplots(2, 2, figsize=(16, 10))

    # Plot 1 - Temperatura
    axs[0, 0].plot(dates, df_cort["Indoor Temperature(°C)"],
                   color='#1C6E98', label='Temp. Interna')
    axs[0, 0].plot(dates, df_cort["Outdoor Temperature(°C)"],
                   color='#8E4021', label='Temp. Externa', linestyle='-.')
    # Labelling
    axs[0, 0].set(ylabel=("Temperatura (°C)"), title=(
        "Temperaturas Interna e Externa"))
    axs[0, 0].legend(loc="upper right")
    axs[0, 0].tick_params(labelrotation=15)

    # Plot 2 - Vento
    axs[0, 1].plot(dates, df_cort["Wind Speed(m/s)"],
                   color='#947494', label='Velocidade do Vento')
    axes2 = axs[0, 1].twinx()
    axes2.scatter(dates, df_cort["Wind Direction Degrees from North"],
                  color="#F31111", label='Direção do Vento (graus em relação ao Norte)')
    axes2.set_ylim(0, 360)
    axes2.set_yticks([0, 90, 180, 270, 360])
    axes2.set_ylabel('Direção do Vento', color="#F31111")
    # Labelling
    axs[0, 1].set(ylabel=("Velocidade do Vento (m/s)"),
                  title=("Velocidade e Direção do Vento"))
    axs[0, 1].tick_params(labelrotation=15)
    axs[0, 1].legend(loc="upper right")

    # Plot 3 - Pressão
    axs[1, 0].plot(dates, df_cort["Relative Pressure(hpa)"], label='Relativa')
    axs[1, 0].plot(dates, df_cort["Absolute Pressure(hpa)"],
                   label='Absoluta', linestyle='--')
    # Labelling
    axs[1, 0].set(ylabel=("Pressão (hpa)"), title=(
        "Pressão Relativa e Absoluta"))
    axs[1, 0].legend(loc="upper right")
    axs[1, 0].tick_params(labelrotation=15)

    # Plot 4 - Precipitação
    axs[1, 1].plot(dates, df_cort["24 Hour Rainfall(mm)"],
                   color='green', label='Precipitação')
    axes3 = axs[1, 1].twinx()
    axes3.fill_between(dates, df_cort["Outdoor Humidity(%)"],
                       color='#7A90FF', label='Umidade Externa (%)', alpha=0.6)
    axes3.set_ylim(0, 100)
    axes3.set_ylabel('Umidade Externa', color="#7A90FF")
    # Labelling
    axs[1, 1].set(ylabel=("Precipitação diária (mm)"),
                  title=("Precipitação Diária e Umidade do Ar"))
    axs[1, 1].tick_params(labelrotation=15)
    axs[1, 1].legend(loc="upper right")

    for ax in axs.flat:
        ax.label_outer()
    plt.show()
    return
