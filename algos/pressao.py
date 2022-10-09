
from datetime import date, datetime
import pandas as pd
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date


def graf_pressão(session):
    # Pegar os dados - Mudar para a plataforma
    end_dados = 'C:/SisMetEx/toydata/' + session['station'] + '/'
    arq_final = 'dados_final.csv'

    df_arq_final = pd.read_csv(
        end_dados + arq_final, encoding='utf-8', sep=';').drop(columns='Unnamed: 0')

    df = df_arq_final

    datas_df = df_arq_final['Date'].tolist()
    dates = datas_df.copy()
    for i in range(len(datas_df)):
        dates[i] = datetime.strptime(datas_df[i], '%Y-%m-%d %H:%M:%S')

    # Plot
    figure(figsize=(6, 4), dpi=100)

    plt.plot(dates, df["Relative Pressure(hpa)"], label='Relativa')
    plt.plot(dates, df["Absolute Pressure(hpa)"], label='Absoluta')

    # Labelling

    plt.xlabel("Date")
    plt.ylabel("Pressão (hpa)")
    plt.title("Pressão Relativa e Absoluta - " +
              session['station'].replace('_', ' '))
    plt.legend(loc="upper right")

    # Display

    plt.show()

    return


# graf_pressão(df_arq_final)
