import requests
import pandas as pd
import plotly.graph_objects as go
from prefect import task, flow

@task
def report():
    # Realizamos una solicitud GET con requests para extraer los datos de la página
    url0 = 'https://www.gnssplanning.com/api/ionoindex/-69.1660765278/-22.6687649722/2023-02-04T12:00:00/24/600'
    url = 'https://www.gnssplanning.com/api/ionoindex/-69.1660765278/-22.6687649722/2023-02-05T12:00:00/24/600' 
    url2 ='https://www.gnssplanning.com/api/ionoindex/-69.1660765278/-22.6687649722/2023-02-06T12:00:00/24/600'

    response0 = requests.get(url0)
    response1 = requests.get(url)
    response2 = requests.get(url2)

    # Procesamos los datos a formato JSON para poder trabajarlos en Pandas
    data0 = response0.json()
    data1 = response1.json()
    data2 = response2.json()

    # Creamos el DataFrame
    df0 = pd.DataFrame(data0, columns=['timeOfEstimation', 'scintiValue'])
    df1 = pd.DataFrame(data1, columns=['timeOfEstimation', 'scintiValue'])
    df2 = pd.DataFrame(data2, columns=['timeOfEstimation', 'scintiValue'])

    #convertir timeOfEstimation de hrs UTC a hrs local UTC-3 usando tz_convert
    df0['timeOfEstimation'] = pd.to_datetime(df0['timeOfEstimation']).dt.tz_localize('UTC').dt.tz_convert('America/Santiago')
    df0['timeOfEstimation'] = df0['timeOfEstimation'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    df1['timeOfEstimation'] = pd.to_datetime(df1['timeOfEstimation']).dt.tz_localize('UTC').dt.tz_convert('America/Santiago')
    df1['timeOfEstimation'] = df1['timeOfEstimation'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    df2['timeOfEstimation'] = pd.to_datetime(df2['timeOfEstimation']).dt.tz_localize('UTC').dt.tz_convert('America/Santiago')
    df2['timeOfEstimation'] = df2['timeOfEstimation'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    #Graficamos los datos usando plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df0['timeOfEstimation'], y=df0['scintiValue'],
                             mode='lines+markers',
                             name=df0.iloc[0]['timeOfEstimation']+' UTC-3'
                            ))

    fig.add_trace(go.Scatter(x=df1['timeOfEstimation'], y=df1['scintiValue'],
                             mode='lines+markers',
                             name=df1.iloc[0]['timeOfEstimation']+' UTC-3'
                            ))
    fig.add_trace(go.Scatter(x=df2['timeOfEstimation'], y=df2['scintiValue'],
                             mode='lines+markers',
                             name=df2.iloc[0]['timeOfEstimation']+' UTC-3'
                            ))

    fig.update_layout(title=' Events of scintiValue ' + df0.iloc[0]['timeOfEstimation'] + '-' +'scintiValue' + df1.iloc[0]['timeOfEstimation'] + ' - ' + df2.iloc[0]['timeOfEstimation'],
                      hoverlabel_bgcolor="yellow",
                      hovermode="x unified",
                      template="plotly_white",
    )

    fig.update_xaxes(title_text='timeOfEstimation')
    fig.update_yaxes(title_text='scintiValue')

    fig.show()

@flow(name= 'report Scintillation Trimble')
def reportTrimble():
    report()

if __name__ == "__main__":
    reportTrimble()
    
#si sale el error de sqlite3, escribir: rm ~/.prefect/orion.db