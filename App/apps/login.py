import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State

layout = html.Div([
    html.Div(
    dcc.Input(id="user", type="text", placeholder="Digite o usuário",className="inputbox1",
    style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'60px',
    'font-size':'16px','border-width':'3px','border-color':'#a0a3a2'
    }),
    ),
    html.Div(
    dcc.Input(id="password", type="password", placeholder="Digite a senha",className="inputbox2",
    style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'10px',
    'font-size':'16px','border-width':'3px','border-color':'#a0a3a2',
    }),
    ),
    html.Div(
    html.Button('Entrar', id='verify', n_clicks=0, style={'border-width':'3px','font-size':'14px'}),
    style={'margin-left':'45%','padding-top':'30px'}),
    html.Div(id='output1')
  ])