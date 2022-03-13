import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
from turtle import color, right
import dash_core_components as dcc

from dash.dependencies import Input, Output

from dash_bootstrap_components._components.Navbar import Navbar

# Autenticacao
import dash_auth
from Dados import consulta_bd

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import vendas, produto, home, notfound, regiao, regiao_prod

import montaGraficoVendas
import montaGraficoPedidos

import sys
sys.path.insert(1, 'C:/EasyDash')
import pFuncoes as fun

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

dados = fun.json_reader('C:\\EasyDash\\App\\auth.json')
dados_auth=dados['result']
montaAuth={}
cont = 0

for dado in dados_auth:
    montaAuth.update({dado['user']:dado['password']})

autenticacao = dash_auth.BasicAuth(app,montaAuth)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 50,
    "left": 10,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#ffffff",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "rem",
    "padding": "2rem 1rem",
}

nav_link1 = {
    "color": "white",
    "textAlign": "right",
    "fontSize": 15,
    "marginLeft": "600",
    "backgroundColor": "black",
}

nav_link2 = {
    "color": "white",
    "textAlign": "right",
    "fontSize": 15,
    "marginRight": "50",
    "backgroundColor": "black",
}

nav_name = {
    "color": "white",
    "textAlign": "left",
    "fontSize": 18,
    "margin": "auto",
    "fontFamily": "cursive",
    #"backgroundColor": "red",
}

nav_item_00 = dbc.NavLink('Home', href='/')
nav_item_01 = dbc.NavLink('Vendas', href='/apps/vendas') 
nav_item_02 = dbc.NavLink('Produtos', href='/apps/produto')
nav_item_03 = dbc.NavLink('Região', href='/apps/regiao')

navbar = dbc.Navbar(dbc.Container(
         [
             html.A(
                 # Use row and col to control vertical alignment of logo / brand
                 dbc.Row(
                     [
                         #dbc.Col(html.Img(src='/assets/EasyDash.png', height="20px")),
                         dbc.Col(dbc.NavbarBrand("2JR Multimarcas", className="ms-2", style=nav_name)),
                        
                     ],
                     align="center",
                     className="g-0",
                    
                 ),
                 href="/",
                 style={"textDecoration": "none"},
             ),
             dbc.Nav([
                                               nav_item_00,nav_item_01,nav_item_02, nav_item_03
                                             ],
                                             
                                             className="ms-auto",
                                             navbar=True,
                                            ),
         
            
         ]
     ),
     color="primary",
     dark=True
    
)

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

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), navbar, sidebar, content])


@app.callback(
    Output("page-content", "children"), 
    Input("url", "pathname") )

def display_page(pathname):
    
    if pathname == '/apps/vendas':
        return vendas.layout
    if pathname == '/apps/produto':
        return produto.layout
    if pathname == '/apps/regiao':
        return regiao.layout
    if pathname == '/apps/regiao_prod':
        return regiao_prod.layout
    if pathname == '/':
        return home.layout
    else:
        return notfound.layout



@app.callback(
    Output(component_id='DropDownMes', component_property='children'), 
    Input(component_id='DropDownAno' , component_property='value')
    )

def changedAno(value):
    
    nAno = (len(value))
    montaSql = 'SELECT distinct(substring(data_venda, 4, 2)) FROM public.historico_2jr'
    if (nAno > 0):
        montaSql += ' where '
    else: 
        montaSql = 'SELECT distinct(substring(data_venda, 4, 2)) FROM public.historico_2jr'    
    for i in range(0, nAno):
        if (i != nAno-1): 
            montaSql +=  "substring(data_venda, 7, 4) = '"+value[i]+"' or "
        else:
            montaSql += "substring(data_venda, 7, 4) = '"+value[i]+"' order by substring(data_venda, 4, 2)  ASC"
    mes = preencheDropDownMES(montaSql) 
    mesesdisponiveis = dcc.Checklist(

                                
                   mes['Mes'],
                   mes['Mes'].values, id = 'DropDownMesCarregado'
              
                ),
    return mesesdisponiveis




@app.callback(
    Output(component_id='DropDownDia', component_property='children'),  
    [Input(component_id='DropDownMesCarregado', component_property='value'),
    Input(component_id='DropDownAno', component_property='value')],
    )

def changedMes(dMes, dAno):
    nMes = len(dMes)
    nAno = len(dAno)
    montaSql = 'SELECT distinct(substring(data_venda, 1, 2)) FROM public.historico_2jr'
    if (nAno > 0):
        montaSql += ' where '
    else: 
        montaSql = 'SELECT distinct(substring(data_venda, 1, 2)) FROM public.historico_2jr'    
    for i in range(0, nAno):
        if (i != nAno-1): 
            montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
        else:
            montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"'"
    
    if (nMes > 0):
        if(nAno == 0):
            diasdisponiveis = ''
            return diasdisponiveis 
        else:
            montaSql += ' and '
            for m in range(0, nMes):
                if (m != nMes-1): 
                    montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                else:
                    montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"' order by (substring(data_venda, 1, 2)) asc"
    dia = preencheDropDownDIA(montaSql) 
    diasdisponiveis = dcc.Checklist(

                                
                   dia['Dia'],
                   dia['Dia'].values, id = 'DropDownDiaCarregado'
              
                ),
    return diasdisponiveis
    # nMes = (len(value))
    # montaSql = 'SELECT distinct(substring(data_venda, 1, 2)) FROM public.historico_2jr'
    # if (nMes > 0):
    #     montaSql += ' where '
    # else: 
    #     montaSql = 'SELECT distinct(substring(data_venda, 1, 2)) FROM public.historico_2jr'    
    # for i in range(0, nMes):
    #     if (i != nMes-1): 
    #         montaSql +=  "substring(data_venda, 4, 2) = '"+value[i]+"' or "
    #     else:
    #         montaSql += "substring(data_venda, 4, 2) = '"+value[i]+"' order by substring(data_venda, 1, 2)  ASC"
    # print(montaSql)
    # dia = preencheDropDownMES(montaSql) 
    # diasdisponiveis = dcc.Checklist(

                                
    #                dia['Dia'],
    #                dia['Dia'].values, id = 'DropdownDiaCarregado'
              
    #         ),
    # return diasdisponiveis

# def render_page_content(pathname):
#     if pathname == "/":
#         return home.layout
#     elif pathname == "/page-1":
#         return html.P("This is the content of page 1. Yay!")
#     elif pathname == "/page-2":
#         return html.P("Oh cool, this is page 2!")
#     # If the user tries to reach a different page, return a 404 message
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#     )


if __name__ == "__main__":
    app.run_server(port=8888)