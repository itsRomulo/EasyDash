from operator import index
import psycopg2
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
sys.path.insert(1, 'C:/EasyDash')
import pFuncoes as fun
import json
from urllib.request import urlopen
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def montaIndicadores(sql_vendaTotal, sql_somaLucro, sql_mediaMargem, sql_contaPedidos, sql_medioPedidos):
  
#conecta_bd()
  vendaTotal = fun.consulta_bd(sql_vendaTotal)
  somaLucro = fun.consulta_bd(sql_somaLucro)
  mediaMargem = fun.consulta_bd(sql_mediaMargem)
  contaPedidos = fun.consulta_bd(sql_contaPedidos)
  medioPedidos = fun.consulta_bd(sql_medioPedidos)

  df_vT = pd.DataFrame(vendaTotal, columns=['Valor Total'])
  df_sL = pd.DataFrame(somaLucro, columns=['Valor Total'])
  df_mM = pd.DataFrame(mediaMargem, columns=['Valor Total'])
  df_cP = pd.DataFrame(contaPedidos, columns=['Valor Total'])
  df_mP = pd.DataFrame(medioPedidos, columns=['Valor Total'])

  
  return df_vT['Valor Total'][0], df_sL['Valor Total'][0],df_mM['Valor Total'][0],df_cP['Valor Total'][0],df_mP['Valor Total'][0]

def montaGraficoVxA(sql):
  VxA = fun.consulta_bd(sql)
  df_vA = pd.DataFrame(VxA, columns=['Valor','Ano'])
  fig = px.bar(df_vA, x="Ano", y="Valor")
  
  return fig

def montaGraficoVxM(sql):
  VxM = fun.consulta_bd(sql)
  df_vM = pd.DataFrame(VxM, columns=['Valor','Mês'])
  fig = px.histogram(df_vM, x="Mês", y="Valor")
  
  return fig

def montaGraficoVxS(sql_sem1, sql_sem2, sql_sem3, sql_sem4):
  mesAtual = datetime.now().strftime('%m')
  anoAtual = datetime.now().strftime('%Y')
  sem1 = fun.consulta_bd(sql_sem1)
  sem2 = fun.consulta_bd(sql_sem2)
  sem3 = fun.consulta_bd(sql_sem3)
  sem4 = fun.consulta_bd(sql_sem4)
  df_s1 = pd.DataFrame(sem1, columns=['Semana 1'])
  df_s2 = pd.DataFrame(sem2, columns=['Semana 2'])
  df_s3 = pd.DataFrame(sem3, columns=['Semana 3'])
  df_s4 = pd.DataFrame(sem4, columns=['Semana 4'])
  if (df_s1['Semana 1'][0] == None): 
    df_s1['Semana 1'][0] = 8200
  else:  
    df_s1['Semana 1'][0] = int(df_s1['Semana 1'][0])

  if (df_s2['Semana 2'][0] == None): 
    df_s2['Semana 2'][0] = 5000
  else:  
    df_s2['Semana 2'][0] = int(df_s2['Semana 2'][0])

  if (df_s3['Semana 3'][0] == None): 
    df_s3['Semana 3'][0] = 0
  else:  
    df_s3['Semana 3'][0] = int(df_s3['Semana 3'][0])

  if (df_s4['Semana 4'][0] == None): 
    df_s4['Semana 4'][0] = 4000
  else:  
    df_s4['Semana 4'][0] = int(df_s4['Semana 4'][0])
  dfsemana = pd.concat([df_s1, df_s2, df_s3, df_s4], axis=1)
  dfFinal = pd.DataFrame()
  #dfsemana = pd.DataFrame("["+df_s1['Semana 1'][0]+ "," +df_s2['Semana 2'][0]+ "," +df_s3['Semana 3'][0]+","+df_s4['Semana 4'][0]+"]", columns=['Semana 1','Semana 2','Semana 3','Semana 4'])
  
  #fig = px.bar(dfsemana, x="Semana 1", title='Life expectancy in Canada')
  fig = px.bar(y=[df_s1['Semana 1'][0],df_s2['Semana 2'][0],df_s3['Semana 3'][0],df_s4['Semana 4'][0]], x=['Semana 1', 'Semana 2', 'Semana 3','Semana 4'], title="Mês Referente:"+mesAtual)

  return fig

def montaGraficoVxD(sql):
  diasMes = fun.consulta_bd(sql)
  df_dM = pd.DataFrame(diasMes, columns=['Data','Valor Vendido'])
  fig = px.bar(df_dM, x='Data', y='Valor Vendido')
  return fig

def montaGraficoVxC(sql_internet, sql_lojafisica):

  vI = fun.consulta_bd(sql_internet)
  vLF = fun.consulta_bd(sql_lojafisica)
  df_vI = pd.DataFrame(vI, columns=['Internet'])
  df_vLF = pd.DataFrame(vLF, columns=['Loja Fisica'])
  dfcanal = pd.concat([df_vI, df_vLF], axis=1)
  fig = px.pie(values=[dfcanal['Internet'][0], dfcanal['Loja Fisica'][0]], names=['Internet', 'Loja Fisica'])
  
  return fig

def montaGraficoVxR(sql):
    
    vR = fun.consulta_bd(sql)
    df_vR = pd.DataFrame(vR, columns=['Ano','UF','Estado','Vendas','Longitude','Latitude'])
    df_vR['Longitude']=df_vR['Longitude'].astype(float, errors = 'raise')
    df_vR['Latitude']=df_vR['Latitude'].astype(float, errors = 'raise')
    df_vR['Ano']=df_vR['Ano'].astype(int, errors = 'raise')

    

    with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
        Brazil = json.load(response) # Javascrip object notation

        state_id_map = {}
        for feature in Brazil ['features']:
            feature['id'] = feature['properties']['name']
            state_id_map[feature['properties']['sigla']] = feature['id']

        brazil = pd.read_csv('brazils.csv')

        for i in range(0,27):
          brazil['Vendas'][i]=df_vR['Vendas'][i]
        
        #brazil['Vendas'] = locale.currency(brazil['Vendas'], grouping=True, symbol=None)

        fig = px.choropleth(
        brazil, #soybean database
        locations = "Estado", #define the limits on the map/geography
        geojson = Brazil, #shape information
        color = "Vendas", #defining the color of the scale through the database
        hover_name = "Estado", #the information in the box
        hover_data =["Vendas"],
        #title of the map
        #animation_frame = "ano" #creating the application based on the year
        )
        fig.update_geos(fitbounds = "locations", visible = False)
    return fig