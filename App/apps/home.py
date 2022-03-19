from pydoc import classname
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

import dash_bootstrap_components as dbc

from apps import vendas, produto, regiao

cardVendas = dbc.Card(
    [
        dbc.CardImg(src="assets/vendas.png", top=True),
        dbc.CardBody(
            [
                html.H4("Dashboard Vendas", className="card-title"),
                html.P(
                    "Você visualiza e compara sua performance de forma ampla através de diversos indicadores",
                    
                    className="card-text",
                ),
                dbc.Button("Acessar", 
                href="/apps/vendas",
                color="info",
                className="btn btn-primary btn-lg"),
            ]
        ),
    ],
    style={"width": "22rem", "height": "500px", "textAlign": "center"},
)

cardProd = dbc.Card(
    [
        dbc.CardImg(src="assets/produtos.png", top=True),
        dbc.CardBody(
            [
                html.H4("Dashboard Produtos", className="card-title"),
                html.P(
                    "Apresenta não somente a quantidade de saída do produto mas também as principais marcas e categorias vendidas",
                    
                    className="card-text",
                ),
                dbc.Button("Acessar", 
                href="/apps/produto",
                color="info",
                className="btn btn-primary btn-lg"),
            ]
        ),
    ],
    style={"width": "22rem", "height": "500px", "textAlign": "center"},
)

cardRegiao = dbc.Card(
    [
        dbc.CardImg(src="assets/mapas.png", top=True),
        dbc.CardBody(
            [
                html.H4("Dashboard Regiao", className="card-title"),
                html.P(
                    "Auxilia quanto ao foco regional de suas vendas, mostrando de forma interativa os estados que estão alcançando",
                    
                    className="card-text",
                ),
                dbc.Button("Acessar", 
                href="/apps/regiao",
                color="info",
                className="btn btn-primary btn-lg"),
            ]
        ),
    ],
    style={"width": "22rem", "height": "500px", "textAlign": "center"},
)

cards = dbc.Row(
    [
        dbc.Col(cardVendas, width=4),
        dbc.Col(cardProd, width=4),
        dbc.Col(cardRegiao, width=4),
    ]
)

layout = html.Div([
    
    # html.H1('Seja bem-vindo ao ', style={"color": "black", "display": "inline", "fontSize": 35, "marginLeft": "500px"}),
    # html.H1('Easy', style={"color": "gray", "display": "inline"}), 
    # html.H1('Dash', style={"color": "green", "display": "inline"}),
    # html.H1('!', style={"color": "black", "display": "inline"}),
    #html.H5('O Dashboard feito sob medida para auxiliar você e sua equipe a tomarem as melhores decisões!'),
    cards
], style={})






