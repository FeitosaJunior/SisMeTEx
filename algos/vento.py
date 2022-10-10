
from datetime import date, datetime
import pandas as pd
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date


# Gráfico final pro server
def graf_vento(session):
    # Pegar os dados - Mudar para a plataforma
    end_dados = 'C:/SisMetEx/toydata/' + session['station'] + '/'
    arq_final = 'dados_final.csv'
    df_arq_final = pd.read_csv(end_dados + arq_final, encoding='utf-8', sep=';').drop(columns='Unnamed: 0')

    # Pegar data
    data_inicio = str(session['startdate'])
    data_final = str(session['enddate'])
    # Transformar texto em data
    dt_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
    dt_final = datetime.strptime(data_final, '%Y-%m-%d')

    # Transformar datas
    for i in range(len(df_arq_final)):
        df_arq_final['Date'][i] = datetime.strptime(df_arq_final['Date'][i], '%Y-%m-%d %H:%M:%S')

    # Cortar o dataframe
    df_cort = df_arq_final[df_arq_final['Date'] < dt_final]
    df_cort = df_cort[df_arq_final['Date'] > dt_inicio]
    df_cort = df_cort.reset_index(drop = True)

    if len(df_cort) < 3: # Se o corte tiver muitos poucos dados, mandar tudão
        df_cort = df_arq_final.copy()
    
    dates = df_cort['Date'].tolist()

    # Gráfico
    plt.figure()      
    figure(figsize=(6, 4), dpi=100)   
    plt.plot(dates, df["Wind Speed(m/s)"], color='#947494', label='Velocidade do Vento')
    plt.ylabel('Velocidade do Vento (m/s)',color="#947494",fontsize=14)      
    plt.xticks(rotation=30)
    axes2 = plt.twinx()
    axes2.plot(dates, df["Wind Direction Degrees from North"], 'ro', label='Direção do Vento (graus em relação ao Norte)')
    axes2.set_ylim(0, 360)
    axes2.set_ylabel('Direção do Vento',color="#F31111",fontsize=14)
    # Labelling
    plt.xlabel("Date")
    plt.title("Velocidade e Direção do Vento - " + session['station'].replace('_', ' '))
    plt.legend(loc="upper right")
    # Display
    plt.show()
    return