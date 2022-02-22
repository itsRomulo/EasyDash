import dash
from   dash import dcc
from   dash import html
import dash_table
from dash.html import I
from dash.html.Img import Img
from dash.html.Title import Title
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Navbar import Navbar
from pyparsing import line
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import Layout 

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout =html.Div([Layout.navbar, Layout.Primeiras_Informacoes, Layout.linha1_grafico, Layout.linha2_grafico]) 
if __name__ == '__main__':
    app.run_server(debug=True)