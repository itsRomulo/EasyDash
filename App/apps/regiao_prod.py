import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Navbar import Navbar
import plotly.graph_objs as go
import pFuncoes as fun
import dash
import dash_table
from dash.html import I
from dash.html.Img import Img
from dash.html.Title import Title
from dash.dependencies import Input, Output, State

import sys
sys.path.insert(1, 'C:/EasyDash/App'),
import montaGraficoPedidos as pedidoGraf

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
EASYDASH = "https://romulobrandao.com/EasyDash.png"


df4 = px.data.election()

geojson = px.data.election_geojson()

sql = "SELECT ano, uf_venda, estado, categoria_produto, cnt, longitude, latitude FROM (SELECT Substring(data_venda, 7, 4) AS ano, categoria_produto, uf_venda, COUNT(*) as cnt, CASE WHEN uf_venda = 'RO' THEN 'Rondônia' WHEN uf_venda = 'AC' THEN 'Acre' WHEN uf_venda = 'AM' THEN 'Amazonas' WHEN uf_venda = 'RR' THEN 'Roraima' WHEN uf_venda = 'PA' THEN 'Pará' WHEN uf_venda = 'AP' THEN 'Amapá' WHEN uf_venda = 'TO' THEN 'Tocantins' WHEN uf_venda = 'MA' THEN 'Maranhão' WHEN uf_venda = 'PI' THEN 'Piauí' WHEN uf_venda = 'CE' THEN 'Ceará' WHEN uf_venda = 'RN' THEN 'Rio Grande do Norte' WHEN uf_venda = 'PB' THEN 'Paraíba' WHEN uf_venda = 'PE' THEN 'Pernambuco' WHEN uf_venda = 'AL' THEN 'Alagoas' WHEN uf_venda = 'SE' THEN 'Sergipe' WHEN uf_venda = 'BA' THEN 'Bahia' WHEN uf_venda = 'MG' THEN 'Minas Gerais' WHEN uf_venda = 'ES' THEN 'Espírito Santo' WHEN uf_venda = 'RJ' THEN 'Rio de Janeiro' WHEN uf_venda = 'SP' THEN 'São Paulo' WHEN uf_venda = 'PR' THEN 'Paraná' WHEN uf_venda = 'SC' THEN 'Santa Catarina' WHEN uf_venda = 'RS' THEN 'Rio Grande do Sul' WHEN uf_venda = 'MS' THEN 'Mato Grosso do Sul' WHEN uf_venda = 'MT' THEN 'Mato Grosso' WHEN uf_venda = 'GO' THEN 'Goiás' WHEN uf_venda = 'DF' THEN 'Distrito Federal' END AS estado, CASE WHEN uf_venda = 'RO' THEN '-11474053' WHEN uf_venda = 'AC' THEN '-949865' WHEN uf_venda = 'AM' THEN '-3976318' WHEN uf_venda = 'RR' THEN '2148823' WHEN uf_venda = 'PA' THEN '-4239015' WHEN uf_venda = 'AP' THEN '2406605' WHEN uf_venda = 'TO' THEN '-9596869' WHEN uf_venda = 'MA' THEN '-4042' WHEN uf_venda = 'PI' THEN '-6995318' WHEN uf_venda = 'CE' THEN '-4354732' WHEN uf_venda = 'RN' THEN '-5607038' WHEN uf_venda = 'PB' THEN '-6950165' WHEN uf_venda = 'PE' THEN '-8140122' WHEN uf_venda = 'AL' THEN '-9521841' WHEN uf_venda = 'SE' THEN '-8263146' WHEN uf_venda = 'BA' THEN '-12197327' WHEN uf_venda = 'MG' THEN '-18824095' WHEN uf_venda = 'ES' THEN '-19768337' WHEN uf_venda = 'RJ' THEN '-227641' WHEN uf_venda = 'SP' THEN '-22763116' WHEN uf_venda = 'PR' THEN '-24722653' WHEN uf_venda = 'SC' THEN '-27257104' WHEN uf_venda = 'RS' THEN '-30055067' WHEN uf_venda = 'MS' THEN '-20616023' WHEN uf_venda = 'MT' THEN '-13434091' WHEN uf_venda = 'GO' THEN '-168529' WHEN uf_venda = 'DF' THEN '-15858437' END AS longitude, CASE WHEN uf_venda = 'RO' THEN '-62226545' WHEN uf_venda = 'AC' THEN '-69629581' WHEN uf_venda = 'AM' THEN '-64399382' WHEN uf_venda = 'RR' THEN '-61412437' WHEN uf_venda = 'PA' THEN '-52218322' WHEN uf_venda = 'AP' THEN '-51428199' WHEN uf_venda = 'TO' THEN '-48201864' WHEN uf_venda = 'MA' THEN '-45107216' WHEN uf_venda = 'PI' THEN '-41807852' WHEN uf_venda = 'CE' THEN '-39712723' WHEN uf_venda = 'RN' THEN '-368261' WHEN uf_venda = 'PB' THEN '-35588089' WHEN uf_venda = 'PE' THEN '-37779227' WHEN uf_venda = 'AL' THEN '-36039082' WHEN uf_venda = 'SE' THEN '-35510823' WHEN uf_venda = 'BA' THEN '-40191427' WHEN uf_venda = 'MG' THEN '-440345' WHEN uf_venda = 'ES' THEN '-403565' WHEN uf_venda = 'RJ' THEN '-421726' WHEN uf_venda = 'SP' THEN '-479046' WHEN uf_venda = 'PR' THEN '-5109548' WHEN uf_venda = 'SC' THEN '-49879454' WHEN uf_venda = 'RS' THEN '-52387882' WHEN uf_venda = 'MS' THEN '-55095124' WHEN uf_venda = 'MT' THEN '-55501919' WHEN uf_venda = 'GO' THEN '-511050' WHEN uf_venda = 'DF' THEN '-47596956' END AS latitude, ROW_NUMBER() OVER (PARTITION BY uf_venda ORDER BY COUNT(*) DESC) as seqnum FROM public.historico_2jr WHERE Substring(data_venda, 7, 4) = '2022' GROUP BY categoria_produto, uf_venda, Substring(data_venda, 7, 4) ) ct WHERE seqnum = 1;"
  
fig4 = pedidoGraf.montaGraficoProdutosRegiao(sql)

linha  = dbc.Row(dbc.Card())
pulalinha = html.Br()




linha2_grafico = dbc.CardGroup(
    [
        
         dbc.Card(
            dbc.CardBody(
                 [
                    html.H5("Produtos x Região", className="card-title"),
                     dcc.Graph(
                     id='PxR',
                     figure=fig4
                ),
                     dbc.Button(
                         "Vendas por Região", size="lg", className="me-1", href='/apps/regiao'
                     ),
                ]
            )
        ),
        
        
    ]
)




SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 100,
    "left": 10,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#ffffff",
}



def preencheDropDownANO(sqlAno):
    ano = fun.consulta_bd(sqlAno)
    df_ano = pd.DataFrame(ano, columns=['Ano'])
    return df_ano


def preencheDropDownMES(sqlMes):
    mes = fun.consulta_bd(sqlMes)
    df_mes = pd.DataFrame(mes, columns=['Mes'])
    
    return df_mes 


def preencheDropDownDIA(sqlDia):
    dia = fun.consulta_bd(sqlDia)
    df_dia = pd.DataFrame(dia, columns=['Dia'])
    return df_dia



sqlAno = 'SELECT distinct(substring(data_venda, 7, 4)) FROM public.historico_2jr order by substring(data_venda, 7, 4) ASC;'
sqlMes = 'SELECT distinct(substring(data_venda, 4, 2)) FROM public.historico_2jr order by substring(data_venda, 4, 2) ASC;'
sqlDia = 'SELECT distinct(substring(data_venda, 1, 2)) FROM public.historico_2jr order by substring(data_venda, 1, 2) ASC;'
ano = preencheDropDownANO(sqlAno)   
mes = preencheDropDownMES(sqlMes) 
dia = preencheDropDownDIA(sqlDia)


sidebar = html.Div(
    [
        html.H2(dbc.Col(html.Img(src='/assets/EasyDash.png', height="20px"))),
        html.Hr(),
        html.P(
            "Selecione o Período desejado", className="lead"
        ),
        dbc.Nav(
            [
                dbc.DropdownMenu(
                 children=[   
                dcc.Checklist(
                    
                    ano['Ano'],
                    ano['Ano'].values, id = "DropDownAno",
            ), 
                ],
                    label="Ano", 
                ),

            ]),

            html.Br(),

            dbc.Nav([  
                
                dbc.DropdownMenu( id = "DropDownMes",
                 children=[],
                    label="Mês",
                ),
            ]),

        #     html.Br(),

        #     dbc.Nav([
        #         dbc.DropdownMenu(
        #          children=[   
        #         dcc.Checklist(
        #             dia['Dia'],
        #             dia['Dia'].values, 
        #         ),
        #         ],
        #             label="Dia", id = "DropDownDia"
        #         ),
        #         # dbc.NavLink("Home", href="/", active="exact"),
        #         # dbc.NavLink("Page 1", href="/page-1", active="exact"),
        #         # dbc.NavLink("Page 2", href="/page-2", active="exact"),
        #     ],
        #     vertical=True,
        #     pills=True,
        # ),
    ],
    style=SIDEBAR_STYLE,
)




layout =html.Div([sidebar, linha2_grafico]) 

