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
import montaGraficoVendas as vendasGraf

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
EASYDASH = "https://romulobrandao.com/EasyDash.png"

df6 = px.data.tips()
fig6 = px.histogram(df6, x="total_bill")

geojson = px.data.election_geojson()

linha  = dbc.Row(dbc.Card())
pulalinha = html.Br()

#sql_mapa = "SELECT Substring(data_venda,7,4) as ano,uf_venda, case when uf_venda =  'RO' then 'Rondônia' when uf_venda =  'AC' then 'Acre' when uf_venda =  'AM' then 'Amazonas' when uf_venda =  'RR' then 'Roraima' when uf_venda =  'PA' then 'Pará' when uf_venda =  'AP' then 'Amapá' when uf_venda =  'TO' then 'Tocantins' when uf_venda =  'MA' then 'Maranhão' when uf_venda =  'PI' then 'Piauí' when uf_venda =  'CE' then 'Ceará' when uf_venda =  'RN' then 'Rio Grande do Norte' when uf_venda =  'PB' then 'Paraíba' when uf_venda =  'PE' then 'Pernambuco'	when uf_venda =  'AL' then 'Alagoas'	when uf_venda =  'SE' then 'Sergipe'	when uf_venda =  'BA' then 'Bahia'	when uf_venda =  'MG' then 'Minas Gerais'	when uf_venda =  'ES' then 'Espírito Santo'	when uf_venda =  'RJ' then 'Rio de Janeiro'	when uf_venda =  'SP' then 'São Paulo'	when uf_venda =  'PR' then 'Paraná'	when uf_venda =  'SC' then 'Santa Catarina'	when uf_venda =  'RS' then 'Rio Grande do Sul'	when uf_venda =  'MS' then 'Mato Grosso do Sul'	when uf_venda =  'MT' then 'Mato Grosso'	when uf_venda =  'GO' then 'Goiás'	when uf_venda =  'DF' then 'Distrito Federal'	end as estado,sum(cast(valor_produto as float)) as vendas,case when uf_venda =  'RO' then '-11474053'	when uf_venda =  'AC' then '-949865'	when uf_venda =  'AM' then '-3976318'	when uf_venda =  'RR' then '2148823'	when uf_venda =  'PA' then '-4239015'	when uf_venda =  'AP' then '2406605'	when uf_venda =  'TO' then '-9596869'	when uf_venda =  'MA' then '-4042'	when uf_venda =  'PI' then '-6995318'	when uf_venda =  'CE' then '-4354732'	when uf_venda =  'RN' then '-5607038'	when uf_venda =  'PB' then '-6950165'	when uf_venda =  'PE' then '-8140122'	when uf_venda =  'AL' then '-9521841'	when uf_venda =  'SE' then '-8263146'	when uf_venda =  'BA' then '-12197327'	when uf_venda =  'MG' then '-18824095'	when uf_venda =  'ES' then '-19768337'	when uf_venda =  'RJ' then '-227641' when uf_venda =  'SP' then '-22763116'	when uf_venda =  'PR' then '-24722653'	when uf_venda =  'SC' then '-27257104'	when uf_venda =  'RS' then '-30055067'	when uf_venda =  'MS' then '-20616023'	when uf_venda =  'MT' then '-13434091'	when uf_venda =  'GO' then '-168529'	when uf_venda =  'DF' then '-15858437'	end as longitude,case when uf_venda =  'RO' then '-62226545'	when uf_venda =  'AC' then '-69629581'	when uf_venda =  'AM' then '-64399382'	when uf_venda =  'RR' then '-61412437'	when uf_venda =  'PA' then '-52218322'	when uf_venda =  'AP' then '-51428199'	when uf_venda =  'TO' then '-48201864'	when uf_venda =  'MA' then '-45107216' when uf_venda =  'PI' then '-41807852'	when uf_venda =  'CE' then '-39712723'	when uf_venda =  'RN' then '-368261'	when uf_venda =  'PB' then '-35588089'	when uf_venda =  'PE' then '-37779227'	when uf_venda =  'AL' then '-36039082'	when uf_venda =  'SE' then '-35510823'	when uf_venda =  'BA' then '-40191427'	when uf_venda =  'MG' then '-440345'	when uf_venda =  'ES' then '-403565'	when uf_venda =  'RJ' then '-421726'	when uf_venda =  'SP' then '-479046'	when uf_venda =  'PR' then '-5109548' when uf_venda =  'SC' then '-49879454'	when uf_venda =  'RS' then '-52387882'	when uf_venda =  'MS' then '-55095124'	when uf_venda =  'MT' then '-55501919'	when uf_venda =  'GO' then '-511050'	when uf_venda =  'DF' then '-47596956'	end as latitude FROM public.historico_2jr where Substring(data_venda,7,4) = '2022' group by uf_venda, Substring(data_venda,7,4);"
sql_mapa = "SELECT uf_venda, CASE WHEN uf_venda = 'RO' THEN 'Rondônia' WHEN uf_venda = 'AC' THEN 'Acre' WHEN uf_venda = 'AM' THEN 'Amazonas' WHEN uf_venda = 'RR' THEN 'Roraima' WHEN uf_venda = 'PA' THEN 'Pará' WHEN uf_venda = 'AP' THEN 'Amapá' WHEN uf_venda = 'TO' THEN 'Tocantins' WHEN uf_venda = 'MA' THEN 'Maranhão' WHEN uf_venda = 'PI' THEN 'Piauí' WHEN uf_venda = 'CE' THEN 'Ceará' WHEN uf_venda = 'RN' THEN 'Rio Grande do Norte' WHEN uf_venda = 'PB' THEN 'Paraíba' WHEN uf_venda = 'PE' THEN 'Pernambuco' WHEN uf_venda = 'AL' THEN 'Alagoas' WHEN uf_venda = 'SE' THEN 'Sergipe' WHEN uf_venda = 'BA' THEN 'Bahia' WHEN uf_venda = 'MG' THEN 'Minas Gerais' WHEN uf_venda = 'ES' THEN 'Espírito Santo' WHEN uf_venda = 'RJ' THEN 'Rio de Janeiro' WHEN uf_venda = 'SP' THEN 'São Paulo' WHEN uf_venda = 'PR' THEN 'Paraná' WHEN uf_venda = 'SC' THEN 'Santa Catarina' WHEN uf_venda = 'RS' THEN 'Rio Grande do Sul' WHEN uf_venda = 'MS' THEN 'Mato Grosso do Sul' WHEN uf_venda = 'MT' THEN 'Mato Grosso' WHEN uf_venda = 'GO' THEN 'Goiás' WHEN uf_venda = 'DF' THEN 'Distrito Federal' END AS estado, sum(cast(valor_produto AS float)) AS vendas, CASE WHEN uf_venda = 'RO' THEN '-11.474053' WHEN uf_venda = 'AC' THEN '-9.49865' WHEN uf_venda = 'AM' THEN '-3.976318' WHEN uf_venda = 'RR' THEN '2.148823' WHEN uf_venda = 'PA' THEN '-4.239015' WHEN uf_venda = 'AP' THEN '2.406605' WHEN uf_venda = 'TO' THEN '-9.596869' WHEN uf_venda = 'MA' THEN '-4.042' WHEN uf_venda = 'PI' THEN '-6.995318' WHEN uf_venda = 'CE' THEN '-4.354732' WHEN uf_venda = 'RN' THEN '-5.607038' WHEN uf_venda = 'PB' THEN '-6.950165' WHEN uf_venda = 'PE' THEN '-8.140122' WHEN uf_venda = 'AL' THEN '-9.521841' WHEN uf_venda = 'SE' THEN '-8.263146' WHEN uf_venda = 'BA' THEN '-12.197327' WHEN uf_venda = 'MG' THEN '-18.824095' WHEN uf_venda = 'ES' THEN '-19.768337' WHEN uf_venda = 'RJ' THEN '-22.7641' WHEN uf_venda = 'SP' THEN '-22.763116' WHEN uf_venda = 'PR' THEN '-24.722653' WHEN uf_venda = 'SC' THEN '-27.257104' WHEN uf_venda = 'RS' THEN '-30.055067' WHEN uf_venda = 'MS' THEN '-20.616023' WHEN uf_venda = 'MT' THEN '-13.434091' WHEN uf_venda = 'GO' THEN '-16.8529' WHEN uf_venda = 'DF' THEN '-15.858437' END AS longitude, CASE WHEN uf_venda = 'RO' THEN '-62.226545' WHEN uf_venda = 'AC' THEN '-69.629581' WHEN uf_venda = 'AM' THEN '-64.399382' WHEN uf_venda = 'RR' THEN '-61.412437' WHEN uf_venda = 'PA' THEN '-52.218322' WHEN uf_venda = 'AP' THEN '-51.428199' WHEN uf_venda = 'TO' THEN '-48.201864' WHEN uf_venda = 'MA' THEN '-45.107216' WHEN uf_venda = 'PI' THEN '-41.807852' WHEN uf_venda = 'CE' THEN '-39.712723' WHEN uf_venda = 'RN' THEN '-36.8261' WHEN uf_venda = 'PB' THEN '-35.588089' WHEN uf_venda = 'PE' THEN '-37.779227' WHEN uf_venda = 'AL' THEN '-36.039082' WHEN uf_venda = 'SE' THEN '-35.510823' WHEN uf_venda = 'BA' THEN '-40.191427' WHEN uf_venda = 'MG' THEN '-44.0345' WHEN uf_venda = 'ES' THEN '-40.3565' WHEN uf_venda = 'RJ' THEN '-42.1726' WHEN uf_venda = 'SP' THEN '-47.9046' WHEN uf_venda = 'PR' THEN '-51.09548' WHEN uf_venda = 'SC' THEN '-49.879454' WHEN uf_venda = 'RS' THEN '-52.387882' WHEN uf_venda = 'MS' THEN '-55.095124' WHEN uf_venda = 'MT' THEN '-55.501919' WHEN uf_venda = 'GO' THEN '-51.1050' WHEN uf_venda = 'DF' THEN '-47.596956' END AS latitude FROM public.historico_2jr WHERE Substring(data_venda, 7, 4) = '2022' GROUP BY uf_venda;"
fig6=vendasGraf.montaGraficoVxR(sql_mapa)


linha1_grafico = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Vendas x Região", className="card-title"),
                    dcc.Graph(
                    id='VxR',
                    figure=fig6
                ),
                    dbc.Button(
                        "Produtos por Região", size="lg", className="me-1", href='/apps/regiao_prod'
                    ),
                ]
            )
        )
        
        
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


layout =html.Div([sidebar, linha1_grafico]) 

