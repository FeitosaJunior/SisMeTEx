
from datetime import date, datetime
import pandas as pd
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date


# Gráfico final pro server
def graf_prec_umid(session):
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

    # Gráfico
    figure(figsize=(6, 4), dpi=100)
    plt.plot(dates, df_cort["24 Hour Rainfall(mm)"],
             color='green', label='Men means')
    plt.ylabel('Precipitação diária (mm)', color="green", fontsize=14)
    plt.xticks(rotation=30)
    axes2 = plt.twinx()
    axes2.plot(dates, df_cort["Outdoor Humidity(%)"],
               color='#7A90FF', label='Umidade')
    axes2.set_ylim(0, 100)
    axes2.set_ylabel('Umidade externa', color="#7A90FF", fontsize=14)

    # Labelling
    plt.xlabel("Date")
    plt.title("Precipitação Diária e Umidade do Ar - " +
              session['station'].replace('_', ' '))
    plt.legend(loc="upper right")
    plt.fill_between(
        dates, df_cort["Outdoor Humidity(%)"], color='#A1D2FF', alpha=0.7)
    # Display
    plt.show()
    return
