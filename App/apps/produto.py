import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Navbar import Navbar
import plotly.graph_objs as go

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


layout =html.Div([Primeiras_Informacoes, linha1_grafico, linha2_grafico]) 

