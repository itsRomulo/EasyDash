import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from turtle import color, right
import dash_core_components as dcc

from dash.dependencies import Input, Output

from dash_bootstrap_components._components.Navbar import Navbar

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import vendas, produto, home, notfound, regiao, regiao_prod

import montaGraficoVendas
import montaGraficoPedidos

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                    options=['2022', '2021', '2020', '2019'],
                    value=[],
            ),
                ],
                    label="Ano",
                ),

            ]),

            html.Br(),

            dbc.Nav([  
                
                dbc.DropdownMenu(
                 children=[   
                dcc.Checklist(
                    options=['Janeiro', 'Fevereiro', 'Março', 'Abril'],
                    value=[],
                ),
                ],
                    label="Mês",
                ),
            ]),

            html.Br(),

            dbc.Nav([
                dbc.DropdownMenu(
                 children=[   
                dcc.Checklist(
                    options=['1', '2', '3', '4', '5', '6'],
                    value=[],
                ),
                ],
                    label="Dia",
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


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])

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