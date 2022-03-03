import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Navbar import Navbar
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
df2 = px.data.tips()
df3 = px.data.gapminder().query("country=='Canada'")

df4 = px.data.election()
geojson = px.data.election_geojson()


fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig2 = px.pie(df2, values='tip', names='day')
fig3 = px.line(df3, x="year", y="lifeExp", title='Life expectancy in Canada')
fig4 = px.choropleth_mapbox(df4, geojson=geojson, color="Bergeron",
                           locations="district", featureidkey="properties.district",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="carto-positron", zoom=9)

navbar = dbc.Navbar(dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        #dbc.Col(html.Img(src=EASYDASH, height="40px")),
                        dbc.Col(dbc.NavbarBrand("2JR Multimarcas", className="ms-2")),
                        
                    ],
                    align="center",
                    className="g-0",
                    
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            # dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            # dbc.Collapse(
                
            #     id="navbar-collapse",
            #     is_open=False,
            #     navbar=True,
                
            # ),
            dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        ]
    ),
    color="primary",
    dark=True
    
)

linha  = dbc.Row(dbc.Card())
pulalinha = html.Br()



dropdown1 = dcc.Dropdown(id='dia_semana_mes_ano',
                         options=[
                             {'label':'Todo período', 'value':'All'},
                             {'label':'Dia', 'value':'dia'},
                             {'label':'Semana', 'value':'semana'},
                             {'label':'Meses', 'value':'meses'},
                             {'label':'Ano', 'value':'ano'}
                         ],
                         value='All'
                         
                        )

dropdown2 = dcc.Dropdown(id='dia_semana_mes_ano2',
                         options=[
                             {'label':'Todo período', 'value':'All'}
                             
                         ],
                         value='All'
                        )


row_dropdown = dbc.Row(
    [
         dbc.Col(dropdown1, width=6),
        dbc.Col(dropdown2, width=6),
        
    ]
     
)


Primeiras_Informacoes = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("R$ 27.420,10", className="card-title"),
                    html.P(
                        "Lucro Total",
                        
                        className="card-text",
                    ),
                   
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("8.954", className="card-title"),
                    html.P(
                        "Quantidade de Vendas",
                        
                        className="card-text")
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("R$ 200,00", className="card-title"),
                    html.P(
                        "Valor Médio de Venda",
                        
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
                    html.H5("Lucro x Ano", className="card-title"),
                     dcc.Graph(
                    id='example-graph6',
                    figure=fig
                ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Vendas x Ano", className="card-title"),
                    dcc.Graph(
                    id='example-graph3',
                    figure=fig3
                ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            )
        )
        
    ]
)



linha2_grafico = dbc.CardGroup(
    [
        dbc.Card(
            
            dbc.CardBody(
                [
                    html.H5("Vendas x Canal", className="card-title"),
                     dcc.Graph(
                    id='example-graph4',
                    figure=fig2
                    ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Vendas x Região", className="card-title"),
                    dcc.Graph(
                    id='example-graph5',
                    figure=fig4
                ),
                    dbc.Button(
                        "Click here", className="mt-auto"
                    ),
                ]
            )
        )
        
    ]
)




layout =html.Div([navbar, Primeiras_Informacoes, linha1_grafico, linha2_grafico]) 

