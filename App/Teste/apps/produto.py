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

fig = go.Figure()

fig.add_trace(go.Bar(
    x=["Camisas", "Camisetas", "Bermudas", "Tênis"],
    y=[3, 2, 1, 4]
))

fig.update_layout(
    #autosize=False,
    # width=500,
    # height=500,
    yaxis=dict(
        #title_text="Y-axis Title",
        #ticktext=["Very long label", "long label", "3", "label"],
        tickvals=[1, 2, 3, 4],
        tickmode="array",
        #titlefont=dict(size=30),
    )
)

# fig.update_yaxes(automargin=True)

# fig.show()
#fig = px.bar(df, x="Produto", y="Quantidade", color="Cidade", barmode="group")

fig2 = pedidoGraf.montaGraficoTop10()
# fig2 = go.Figure(go.Bar(
#             x=[20, 14, 23, 30, 6, 27, 18, 9, 20, 13],
#             y=['Camisas', 'Bermudas', 'Tênis', 'Camisetas', 'Cueca', 'Chinelo', 'Boné', 'Perfume', 'Relógio', 'Mochila'],
#             orientation='h'))
#fig2 = px.pie(df2, values='tip', names='day')

labels = ['Nike','Adidas','Lacoste','Outros']
values = [4500, 4000, 1053, 500]

fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                             insidetextorientation='radial'
                            )])

#fig = px.line(df3, x="year", y="lifeExp", title='Life expectancy in Canada')

fig4 = px.choropleth_mapbox(df4, geojson=geojson, color="Bergeron",
                           locations="district", featureidkey="properties.district",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="carto-positron", zoom=9)


linha  = dbc.Row(dbc.Card())
pulalinha = html.Br()


cP, pC, pM = pedidoGraf.montaIndicadores()
cP = str(cP)

Primeiras_Informacoes = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3( cP, className="card-title"),
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
                    html.H3(pC, className="card-title"),
                    html.P(
                        "Principal Categoria Vendida",
                        
                        className="card-text")
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(pM, className="card-title"),
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
                    html.H5("Vendas por categoria", className="card-title"),
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
                [   html.H5("Top 10 produtos", className="card-title"),
                     dcc.Graph(
                    id='example-graph4',
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



linha2_grafico = dbc.CardGroup(
    [
        dbc.Card(
            
            dbc.CardBody(
                [
                    html.H5("Vendas por marca", className="card-title"),
                    dcc.Graph(
                    id='example-graph3',
                    figure=fig3
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
                    html.H5("Produtos por Região", className="card-title"),
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


layout =html.Div([Primeiras_Informacoes, linha1_grafico, linha2_grafico]) 

