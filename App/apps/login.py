import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State

layout = html.Div([
    html.H4("Usuário", style={'margin-left':'30%','padding':'10px', 'margin-top':'60px',
    'font-size':'16px','border-color':'#a0a3a2'
    }), 
    html.Div(
    dcc.Input(id="user", type="text", placeholder="Digite o usuário",className="inputbox1",
    style={'margin-left':'30%','width':'450px','height':'45px',
    'font-size':'16px','border-width':'1px','border-color':'#a0a3a2'
    }),
    ),
    html.H4("Senha", style={'margin-left':'30%','width':'450px','height':'45px','padding':'10px', 'margin-top':'20px',
    'font-size':'16px','border-width':'1px','border-color':'#a0a3a2'
    }),
    html.Div(
    dcc.Input(id="password", type="password", placeholder="Digite a senha",className="inputbox2",
    style={'margin-left':'30%','width':'450px','height':'45px',
    'font-size':'16px','border-width':'1px','border-color':'#a0a3a2',
    }),
    ),
    html.Div(
    html.Button('Entrar', id='verify', n_clicks=0, style={'border-width':'1px','font-size':'14px', 'border-radius': '25px'}),
    style={'margin-left':'40%','padding-top':'30px'}),
    html.Div(id='output1')
  ])