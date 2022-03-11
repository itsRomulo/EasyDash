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


df4 = px.data.election()

geojson = px.data.election_geojson()


fig4 = pedidoGraf.montaGraficoProdutosRegiao()

linha  = dbc.Row(dbc.Card())
pulalinha = html.Br()




linha2_grafico = dbc.CardGroup(
    [
        
         dbc.Card(
            dbc.CardBody(
                 [
                    html.H5("Produtos x Região", className="card-title"),
                     dcc.Graph(
                     id='example-graph5',
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


layout =html.Div([linha2_grafico]) 

