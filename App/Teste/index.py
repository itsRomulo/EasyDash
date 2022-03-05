from turtle import color, right
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Navbar import Navbar

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import vendas, produto, home, notfound

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

nav_item_01 = dbc.NavLink('Vendas', href='/apps/vendas') 
nav_item_02 = dbc.NavLink('Produtos', href='/apps/produto')

navbar = dbc.Navbar(dbc.Container(
         [
             html.A(
                 # Use row and col to control vertical alignment of logo / brand
                 dbc.Row(
                     [
                         dbc.Col(html.Img(src='/assets/EasyDash.png', height="20px")),
                         dbc.Col(dbc.NavbarBrand("2JR Multimarcas", className="ms-2", style=nav_name)),
                        
                     ],
                     align="center",
                     className="g-0",
                    
                 ),
                 href="/",
                 style={"textDecoration": "none"},
             ),
             dbc.Nav([
                                               nav_item_01,nav_item_02
                                             ],
                                             
                                             className="ms-auto",
                                             navbar=True,
                                            ),
         
            
         ]
     ),
     color="primary",
     dark=True
    
)





app.layout = html.Div([navbar, 
     dcc.Location(id='url', refresh=False),
    #  html.Div([
         
        
    #      dbc.NavLink('Video Games|', href='/apps/vendas'),
        
    #      dbc.NavLink('Other', href='/apps/produto'),
        
    # ], className="row"),
     html.Div(id='page-content', children=[])

    
 ])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/vendas':
        return vendas.layout
    if pathname == '/apps/produto':
        return produto.layout
    if pathname == '/':
        return home.layout
    else:
        return notfound.layout


if __name__ == '__main__':
    app.run_server(debug=False)