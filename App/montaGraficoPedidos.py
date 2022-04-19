import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import sys
sys.path.insert(1, 'C:/EasyDash')
import pFuncoes as fun
import json
from urllib.request import urlopen

def montaIndicadores(sql_contaProdutos, sql_principalCategoria, sql_principalMarca):

#conecta_bd()
    contaProdutos = fun.consulta_bd(sql_contaProdutos)
    principalCategoria = fun.consulta_bd(sql_principalCategoria)
    principalMarca = fun.consulta_bd(sql_principalMarca)

    df_cP = pd.DataFrame(contaProdutos, columns=['Qtd'])
    qtd_cP = df_cP['Qtd'][0]

    df_pC = pd.DataFrame(principalCategoria, columns=['Qtd', 'Categoria'])
    qtd_pC = df_pC['Categoria'][0]

    df_pM = pd.DataFrame(principalMarca, columns=['Qtd', 'Marca'])
    qtd_pM = df_pM['Marca'][0]

    return qtd_cP, qtd_pC, qtd_pM

def montaGraficoVendasCategoria(sql_vendCat):
    
    vendCat =  fun.consulta_bd(sql_vendCat)

    df_vC = pd.DataFrame(vendCat, columns=['Qtd', 'Categoria'])

    fig = px.bar(df_vC, x='Categoria', y='Qtd')

    return fig

def montaGraficoTop10(sql_top10):
    
    top10 = fun.consulta_bd(sql_top10)

    df_tP = pd.DataFrame(top10, columns=['Qtd', 'Modelo', 'Marca'])

    fig = go.Figure(go.Bar(
            x=[df_tP['Qtd'][9], df_tP['Qtd'][8], df_tP['Qtd'][7], df_tP['Qtd'][6], df_tP['Qtd'][5], df_tP['Qtd'][4], df_tP['Qtd'][3], df_tP['Qtd'][2], df_tP['Qtd'][1], df_tP['Qtd'][0]],
            y=[df_tP['Marca'][9] +' - ' +df_tP['Modelo'][9], df_tP['Marca'][8] +' - ' +df_tP['Modelo'][8], df_tP['Marca'][7] +' - ' +df_tP['Modelo'][7], df_tP['Marca'][6] +' - ' +df_tP['Modelo'][6], df_tP['Marca'][5] +' - ' +df_tP['Modelo'][5], df_tP['Marca'][4] +' - ' +df_tP['Modelo'][4], df_tP['Marca'][3] +' - ' +df_tP['Modelo'][3], df_tP['Marca'][2] +' - ' +df_tP['Modelo'][2], df_tP['Marca'][1] +' - ' +df_tP['Modelo'][1], df_tP['Marca'][0] +' - ' +df_tP['Modelo'][0]],
            orientation='h'))

    return fig

def montaGraficoVendasMarca(sql_vendMarca):
    
    vendMarca = fun.consulta_bd(sql_vendMarca)

    df_vM = pd.DataFrame(vendMarca, columns=['Quantidade', 'Marca'])

    df_vM['Marca'][9] = 'Outros'
    linhas = df_vM.shape[0]


    for i in range(10, linhas):
        #print(i)
        df_vM['Quantidade'][9] = df_vM['Quantidade'][i]+df_vM['Quantidade'][9]

        df_vM['Quantidade'][i] = ''

        df_vM['Marca'][i] = ''

    labels = [df_vM['Marca']]

    values = [df_vM['Quantidade']]

    fig = px.pie(df_vM, values='Quantidade', names='Marca')

    #

    return fig

def montaGraficoProdutosRegiao(sql):
    #sql = "SELECT ano, uf_venda, estado, categoria_produto, cnt, longitude, latitude FROM (SELECT Substring(data_venda, 7, 4) AS ano, categoria_produto, uf_venda, COUNT(*) AS cnt, CASE WHEN uf_venda = 'RO' THEN 'Rondônia' WHEN uf_venda = 'AC' THEN 'Acre' WHEN uf_venda = 'AM' THEN 'Amazonas' WHEN uf_venda = 'RR' THEN 'Roraima' WHEN uf_venda = 'PA' THEN 'Pará' WHEN uf_venda = 'AP' THEN 'Amapá' WHEN uf_venda = 'TO' THEN 'Tocantins' WHEN uf_venda = 'MA' THEN 'Maranhão' WHEN uf_venda = 'PI' THEN 'Piauí' WHEN uf_venda = 'CE' THEN 'Ceará' WHEN uf_venda = 'RN' THEN 'Rio Grande do Norte' WHEN uf_venda = 'PB' THEN 'Paraíba' WHEN uf_venda = 'PE' THEN 'Pernambuco' WHEN uf_venda = 'AL' THEN 'Alagoas' WHEN uf_venda = 'SE' THEN 'Sergipe' WHEN uf_venda = 'BA' THEN 'Bahia' WHEN uf_venda = 'MG' THEN 'Minas Gerais' WHEN uf_venda = 'ES' THEN 'Espírito Santo' WHEN uf_venda = 'RJ' THEN 'Rio de Janeiro' WHEN uf_venda = 'SP' THEN 'São Paulo' WHEN uf_venda = 'PR' THEN 'Paraná' WHEN uf_venda = 'SC' THEN 'Santa Catarina' WHEN uf_venda = 'RS' THEN 'Rio Grande do Sul' WHEN uf_venda = 'MS' THEN 'Mato Grosso do Sul' WHEN uf_venda = 'MT' THEN 'Mato Grosso' WHEN uf_venda = 'GO' THEN 'Goiás' WHEN uf_venda = 'DF' THEN 'Distrito Federal' END AS estado, CASE WHEN uf_venda = 'RO' THEN '-11.474053' WHEN uf_venda = 'AC' THEN '-9.49865' WHEN uf_venda = 'AM' THEN '-3.976318' WHEN uf_venda = 'RR' THEN '2.148823' WHEN uf_venda = 'PA' THEN '-4.239015' WHEN uf_venda = 'AP' THEN '2.406605' WHEN uf_venda = 'TO' THEN '-9.596869' WHEN uf_venda = 'MA' THEN '-4.042' WHEN uf_venda = 'PI' THEN '-6.995318' WHEN uf_venda = 'CE' THEN '-4.354732' WHEN uf_venda = 'RN' THEN '-5.607038' WHEN uf_venda = 'PB' THEN '-6.950165' WHEN uf_venda = 'PE' THEN '-8.140122' WHEN uf_venda = 'AL' THEN '-9.521841' WHEN uf_venda = 'SE' THEN '-8.263146' WHEN uf_venda = 'BA' THEN '-12.197327' WHEN uf_venda = 'MG' THEN '-18.824095' WHEN uf_venda = 'ES' THEN '-19.768337' WHEN uf_venda = 'RJ' THEN '-22.7641' WHEN uf_venda = 'SP' THEN '-22.763116' WHEN uf_venda = 'PR' THEN '-24.722653' WHEN uf_venda = 'SC' THEN '-27.257104' WHEN uf_venda = 'RS' THEN '-30.055067' WHEN uf_venda = 'MS' THEN '-20.616023' WHEN uf_venda = 'MT' THEN '-13.434091' WHEN uf_venda = 'GO' THEN '-16.8529' WHEN uf_venda = 'DF' THEN '-15.858437' END AS longitude, CASE WHEN uf_venda = 'RO' THEN '-62.226545' WHEN uf_venda = 'AC' THEN '-69.629581' WHEN uf_venda = 'AM' THEN '-64.399382' WHEN uf_venda = 'RR' THEN '-61.412437' WHEN uf_venda = 'PA' THEN '-52.218322' WHEN uf_venda = 'AP' THEN '-51.428199' WHEN uf_venda = 'TO' THEN '-48.201864' WHEN uf_venda = 'MA' THEN '-45.107216' WHEN uf_venda = 'PI' THEN '-41.807852' WHEN uf_venda = 'CE' THEN '-39.712723' WHEN uf_venda = 'RN' THEN '-36.8261' WHEN uf_venda = 'PB' THEN '-35.588089' WHEN uf_venda = 'PE' THEN '-37.779227' WHEN uf_venda = 'AL' THEN '-36.039082' WHEN uf_venda = 'SE' THEN '-35.510823' WHEN uf_venda = 'BA' THEN '-40.191427' WHEN uf_venda = 'MG' THEN '-44.0345' WHEN uf_venda = 'ES' THEN '-40.3565' WHEN uf_venda = 'RJ' THEN '-42.1726' WHEN uf_venda = 'SP' THEN '-47.9046' WHEN uf_venda = 'PR' THEN '-51.09548' WHEN uf_venda = 'SC' THEN '-49.879454' WHEN uf_venda = 'RS' THEN '-52.387882' WHEN uf_venda = 'MS' THEN '-55.095124' WHEN uf_venda = 'MT' THEN '-55.501919' WHEN uf_venda = 'GO' THEN '-51.1050' WHEN uf_venda = 'DF' THEN '-47.596956' END AS latitude, ROW_NUMBER() OVER (PARTITION BY uf_venda ORDER BY COUNT(*) DESC) AS seqnum FROM public.historico_2jr WHERE Substring(data_venda, 7, 4) = '2022' GROUP BY categoria_produto, uf_venda, Substring(data_venda, 7, 4)) ct WHERE seqnum = 1;"
    vR = fun.consulta_bd(sql)
    df_vR = pd.DataFrame(vR, columns=['UF','Estado','Categoria','Quantidade','Longitude','Latitude'])
    df_vR['Longitude']=df_vR['Longitude'].astype(float, errors = 'raise')
    df_vR['Latitude']=df_vR['Latitude'].astype(float, errors = 'raise')
    # df_vR['Ano']=df_vR['Ano'].astype(int, errors = 'raise')

    print(df_vR)
    print(df_vR.dtypes)

    with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
        Brazil = json.load(response) # Javascrip object notation

        state_id_map = {}
        for feature in Brazil ['features']:
            feature['id'] = feature['properties']['name']
            state_id_map[feature['properties']['sigla']] = feature['id']

        fig = px.choropleth(
        df_vR, #soybean database
        locations = "Estado", #define the limits on the map/geography
        geojson = Brazil, #shape information
        color = "Quantidade", #defining the color of the scale through the database
        hover_name = "Estado", #the information in the box
        hover_data =["UF","Categoria","Quantidade"],
        #title of the map
        #animation_frame = "ano" #creating the application based on the year
        )
        fig.update_geos(fitbounds = "locations", visible = False)
        fig.update_layout(
        autosize=True,
        width=1500,
        height=800)
    return fig