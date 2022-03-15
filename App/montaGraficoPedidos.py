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
    vR = fun.consulta_bd(sql)
    df_vR = pd.DataFrame(vR, columns=['Ano','UF','Estado','Categoria','Quantidade','Longitude','Latitude'])
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
        brazil.rename(columns = {'Vendas': 'Quantidade'}, inplace = True)
        brazil.insert(1, "UF", df_vR['UF'], allow_duplicates=False)
        brazil.insert(3, "Categoria", df_vR['Categoria'], allow_duplicates=False)
        brazil['Quantidade']=df_vR['Quantidade']
        
        # #brazil['Vendas'] = locale.currency(brazil['Vendas'], grouping=True, symbol=None)

        fig = px.choropleth(
        brazil, #soybean database
        locations = "Estado", #define the limits on the map/geography
        geojson = Brazil, #shape information
        color = "Quantidade", #defining the color of the scale through the database
        hover_name = "Estado", #the information in the box
        hover_data =["UF","Categoria","Quantidade"],
        #title of the map
        #animation_frame = "ano" #creating the application based on the year
        )
        fig.update_geos(fitbounds = "locations", visible = False)
        
    return fig
