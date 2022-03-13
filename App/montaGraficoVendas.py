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

def montaIndicadores():
  sql_vendaTotal = 'SELECT sum(cast(valor_produto as float)) FROM historico_2jr;'
  sql_somaLucro = 'SELECT sum(cast(lucro_venda as float)) FROM historico_2jr;'
  sql_mediaMargem = 'select cast(avg((cast(lucro_venda as float) * 100)/(cast(custo_produto as float))) as numeric(15,2)) from historico_2jr'
  sql_contaPedidos = 'select count(distinct(cod_venda)) from historico_2jr'
  sql_medioPedidos = 'select cast((sum(cast(valor_produto as float)))/(count(distinct(cod_venda))) as numeric (10,2)) from historico_2jr'
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

def montaGraficoVxA():
  sql = 'select sum(cast(valor_produto as float)), substring(data_venda, 7, 4) from historico_2jr GROUP BY substring(data_venda, 7, 4) ORDER BY substring(data_venda, 7, 4) ASC'
  VxA = fun.consulta_bd(sql)
  df_vA = pd.DataFrame(VxA, columns=['Valor','Ano'])
  fig = px.bar(df_vA, x="Ano", y="Valor")
  
  return fig

def montaGraficoVxM():
  sql = 'select sum(cast(valor_produto as float)), substring(data_venda, 4, 2) from historico_2jr GROUP BY substring(data_venda, 4, 2)  ORDER BY substring(data_venda, 4, 2) ASC'
  VxM = fun.consulta_bd(sql)
  df_vM = pd.DataFrame(VxM, columns=['Valor','Mês'])
  fig = px.histogram(df_vM, x="Mês", y="Valor")
  
  return fig

def montaGraficoVxS():
  mesAtual = datetime.now().strftime('%m')
  anoAtual = datetime.now().strftime('%Y')
  sql_sem1 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '01' and '07' and substring(data_venda, 7, 4) = '"+anoAtual+"' and substring(data_venda, 4, 2) = '"+mesAtual+"'"
  sql_sem2 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '08' and '15' and substring(data_venda, 7, 4) = '"+anoAtual+"' and substring(data_venda, 4, 2) = '"+mesAtual+"'"
  sql_sem3 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '16' and '22' and substring(data_venda, 7, 4) = '"+anoAtual+"' and substring(data_venda, 4, 2) = '"+mesAtual+"'"
  sql_sem4 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '23' and '31' and substring(data_venda, 7, 4) = '"+anoAtual+"' and substring(data_venda, 4, 2) = '"+mesAtual+"'"
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

def montaGraficoVxD():
  mesAtual = datetime.now().strftime('%m')
  anoAtual = datetime.now().strftime('%Y')
  sql = "select data_venda, sum(cast(valor_produto as float)) from historico_2jr where substring(data_venda, 7, 4) = '"+anoAtual+"' and substring(data_venda, 4, 2) = '"+mesAtual+"' group by data_venda"
  diasMes = fun.consulta_bd(sql)
  df_dM = pd.DataFrame(diasMes, columns=['Data','Valor Vendido'])
  fig = px.bar(df_dM, x='Data', y='Valor Vendido')
  return fig

def montaGraficoVxC():
  sql_internet = "select count(cod_vendedor) FROM historico_2jr where cod_vendedor = '1'"
  sql_lojafisica = "select count(cod_vendedor) FROM historico_2jr where cod_vendedor <> '1'"
  vI = fun.consulta_bd(sql_internet)
  vLF = fun.consulta_bd(sql_lojafisica)
  df_vI = pd.DataFrame(vI, columns=['Internet'])
  df_vLF = pd.DataFrame(vLF, columns=['Loja Fisica'])
  dfcanal = pd.concat([df_vI, df_vLF], axis=1)
  fig = px.pie(values=[dfcanal['Internet'][0], dfcanal['Loja Fisica'][0]], names=['Internet', 'Loja Fisica'])
  
  return fig

def montaGraficoVxR():
    sql = "SELECT Substring(data_venda,7,4) as ano,uf_venda, case when uf_venda =  'RO' then 'Rondônia' when uf_venda =  'AC' then 'Acre' when uf_venda =  'AM' then 'Amazonas' when uf_venda =  'RR' then 'Roraima' when uf_venda =  'PA' then 'Pará' when uf_venda =  'AP' then 'Amapá' when uf_venda =  'TO' then 'Tocantins' when uf_venda =  'MA' then 'Maranhão' when uf_venda =  'PI' then 'Piauí' when uf_venda =  'CE' then 'Ceará' when uf_venda =  'RN' then 'Rio Grande do Norte' when uf_venda =  'PB' then 'Paraíba' when uf_venda =  'PE' then 'Pernambuco'	when uf_venda =  'AL' then 'Alagoas'	when uf_venda =  'SE' then 'Sergipe'	when uf_venda =  'BA' then 'Bahia'	when uf_venda =  'MG' then 'Minas Gerais'	when uf_venda =  'ES' then 'Espírito Santo'	when uf_venda =  'RJ' then 'Rio de Janeiro'	when uf_venda =  'SP' then 'São Paulo'	when uf_venda =  'PR' then 'Paraná'	when uf_venda =  'SC' then 'Santa Catarina'	when uf_venda =  'RS' then 'Rio Grande do Sul'	when uf_venda =  'MS' then 'Mato Grosso do Sul'	when uf_venda =  'MT' then 'Mato Grosso'	when uf_venda =  'GO' then 'Goiás'	when uf_venda =  'DF' then 'Distrito Federal'	end as estado,sum(cast(valor_produto as float)) as vendas,case when uf_venda =  'RO' then '-11474053'	when uf_venda =  'AC' then '-949865'	when uf_venda =  'AM' then '-3976318'	when uf_venda =  'RR' then '2148823'	when uf_venda =  'PA' then '-4239015'	when uf_venda =  'AP' then '2406605'	when uf_venda =  'TO' then '-9596869'	when uf_venda =  'MA' then '-4042'	when uf_venda =  'PI' then '-6995318'	when uf_venda =  'CE' then '-4354732'	when uf_venda =  'RN' then '-5607038'	when uf_venda =  'PB' then '-6950165'	when uf_venda =  'PE' then '-8140122'	when uf_venda =  'AL' then '-9521841'	when uf_venda =  'SE' then '-8263146'	when uf_venda =  'BA' then '-12197327'	when uf_venda =  'MG' then '-18824095'	when uf_venda =  'ES' then '-19768337'	when uf_venda =  'RJ' then '-227641' when uf_venda =  'SP' then '-22763116'	when uf_venda =  'PR' then '-24722653'	when uf_venda =  'SC' then '-27257104'	when uf_venda =  'RS' then '-30055067'	when uf_venda =  'MS' then '-20616023'	when uf_venda =  'MT' then '-13434091'	when uf_venda =  'GO' then '-168529'	when uf_venda =  'DF' then '-15858437'	end as longitude,case when uf_venda =  'RO' then '-62226545'	when uf_venda =  'AC' then '-69629581'	when uf_venda =  'AM' then '-64399382'	when uf_venda =  'RR' then '-61412437'	when uf_venda =  'PA' then '-52218322'	when uf_venda =  'AP' then '-51428199'	when uf_venda =  'TO' then '-48201864'	when uf_venda =  'MA' then '-45107216' when uf_venda =  'PI' then '-41807852'	when uf_venda =  'CE' then '-39712723'	when uf_venda =  'RN' then '-368261'	when uf_venda =  'PB' then '-35588089'	when uf_venda =  'PE' then '-37779227'	when uf_venda =  'AL' then '-36039082'	when uf_venda =  'SE' then '-35510823'	when uf_venda =  'BA' then '-40191427'	when uf_venda =  'MG' then '-440345'	when uf_venda =  'ES' then '-403565'	when uf_venda =  'RJ' then '-421726'	when uf_venda =  'SP' then '-479046'	when uf_venda =  'PR' then '-5109548' when uf_venda =  'SC' then '-49879454'	when uf_venda =  'RS' then '-52387882'	when uf_venda =  'MS' then '-55095124'	when uf_venda =  'MT' then '-55501919'	when uf_venda =  'GO' then '-511050'	when uf_venda =  'DF' then '-47596956'	end as latitude FROM public.historico_2jr where Substring(data_venda,7,4) = '2022' group by uf_venda, Substring(data_venda,7,4);"
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