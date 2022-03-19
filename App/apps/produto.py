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

df = pd.DataFrame({
    "Marca": ["Nike", "Adidas", "Lacoste", "Nike", "Adidas", "Lacoste"],
    "Quantidade": [5, 2, 3, 3, 5, 6],
    #"Cidade": ["SP", "SP", "SP", "RJ", "RJ", "RJ"]
})
df2 = px.data.tips()
df3 = px.data.gapminder().query("country=='Canada'")

df4 = px.data.election()
geojson = px.data.election_geojson()

sql_vendCat = 'SELECT count(categoria_produto), categoria_produto FROM historico_2jr GROUP BY categoria_produto HAVING COUNT(categoria_produto) > 1 ORDER BY count(categoria_produto) DESC'
sql_top10 = 'SELECT count(modelo_produto), modelo_produto, marca_produto FROM historico_2jr GROUP BY modelo_produto, marca_produto HAVING COUNT(modelo_produto) > 1 ORDER BY count(modelo_produto) DESC'
sql_vendMarca = 'SELECT count(marca_produto), marca_produto FROM historico_2jr GROUP BY marca_produto HAVING COUNT(marca_produto) > 1 ORDER BY count(marca_produto) DESC'

fig  = pedidoGraf.montaGraficoVendasCategoria(sql_vendCat)
fig2 = pedidoGraf.montaGraficoTop10(sql_top10)
fig3 = pedidoGraf.montaGraficoVendasMarca(sql_vendMarca)

linha  = dbc.Row(dbc.Card())
pulalinha = html.Br()

sql_contaProdutos = 'select count(cod_venda) from historico_2jr'
sql_principalCategoria = 'SELECT count(categoria_produto), categoria_produto FROM historico_2jr GROUP BY categoria_produto HAVING COUNT(categoria_produto) > 1 ORDER BY count(categoria_produto) DESC'
sql_principalMarca = 'SELECT count(marca_produto), marca_produto FROM historico_2jr GROUP BY marca_produto HAVING COUNT(marca_produto) > 1 ORDER BY count(marca_produto) DESC'

cP, pC, pM = pedidoGraf.montaIndicadores(sql_contaProdutos, sql_principalCategoria, sql_principalMarca)
cP = str(cP)

Primeiras_Informacoes = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3( children=[cP], className="card-title", id = "IndicadorProdutoVendido"),
                    html.P(
                        "Quantidade de Produtos Vendidos",
                        
                        className="card-text",
                    ),
                   
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(children=[pC], className="card-title", id = "IndicadorCategoriaVendida"),
                    html.P(
                        "Principal Categoria Vendida",
                        
                        className="card-text")
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(children=[pM], className="card-title", id = "IndicadorMarcaVendida"),
                    html.P(
                        "Principal Marca Vendida",
                        
                        className="card-text")
                ]
            )
        ),
    ]
)


linha1_grafico = dbc.CardGroup(
    [
        dbc.Card(
            
            dbc.CardBody(
                [
                    html.H5("Vendas x Categoria (Qtd)", className="card-title"),
                     dcc.Graph(
                    id='VxCat',
                    figure=fig
                ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            )
        ),
        
        
    ]
)



linha2_grafico = dbc.CardGroup(
    [
        dbc.Card(
            
            dbc.CardBody(
                [
                    html.H5("Vendas x Marca", className="card-title"),
                    dcc.Graph(
                    id='VxMarca',
                    figure=fig3
                ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            )
        ),
        # dbc.Card(
        #     dbc.CardBody(
        #         [
        #             html.H5("Produtos por Região", className="card-title"),
        #             dcc.Graph(
        #             id='example-graph5',
        #             figure=fig4
        #         ),
        #             dbc.Button(
        #                 "Click here", className="mt-auto"
        #             ),
        #         ]
        #     )
        # )
        dbc.Card(
            dbc.CardBody(
                [   html.H5("Top 10 produtos", className="card-title"),
                     dcc.Graph(
                    id='Top10',
                    figure=fig2
                    ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    
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

            html.Br(),

            dbc.Nav([
                dbc.DropdownMenu(
                 children=[   
                dcc.Checklist(
                    dia['Dia'],
                    dia['Dia'].values, 
                ),
                ],
                    label="Dia", id = "DropDownDia"
                ),
                # dbc.NavLink("Home", href="/", active="exact"),
                # dbc.NavLink("Page 1", href="/page-1", active="exact"),
                # dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)



layout =html.Div([sidebar, Primeiras_Informacoes, linha1_grafico, linha2_grafico]) 

