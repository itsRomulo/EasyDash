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
 

import json
from urllib.request import urlopen

import sys
sys.path.insert(1, 'C:/EasyDash/App'),
import montaGraficoVendas as vendasGraf

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
#fig4 = px.choropleth_mapbox(df4, geojson=geojson, color="Bergeron",
 #                          locations="district", featureidkey="properties.district",
  #                         center={"lat": 45.5517, "lon": -73.7073},
   #                        mapbox_style="carto-positron", zoom=9)

df5 = px.data.stocks(indexed=True)-1
fig5 = px.area(df5, facet_col="company", facet_col_wrap=2)

df6 = px.data.tips()
fig6 = px.histogram(df6, x="total_bill")

fig7 = px.choropleth(locations=["CA", "TX", "NY"], locationmode="USA-states", color=[1,2,3], scope="usa")

def map_graph():
    with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
        Brazil = json.load(response) # Javascrip object notation 

        state_id_map = {}
        for feature in Brazil ['features']:
            feature['id'] = feature['properties']['name']
            state_id_map[feature['properties']['sigla']] = feature['id']

        brazil = pd.read_csv('brazil.csv')

        fig = px.choropleth(
        brazil, #soybean database
        locations = "Estado", #define the limits on the map/geography
        geojson = Brazil, #shape information
        color = "Vendas", #defining the color of the scale through the database
        hover_name = "Estado", #the information in the box
        hover_data =["Vendas","Longitude","Latitude"],
        #title of the map
        #animation_frame = "ano" #creating the application based on the year
        )
        fig.update_geos(fitbounds = "locations", visible = False)
        return fig

fig6 = map_graph()





linha  = dbc.Row(dbc.Card())
pulalinha = html.Br()





vT,sL,mM,cP,mP = vendasGraf.montaIndicadores()
vT = int(vT)
vT = '{0:,}'.format(vT).replace(',','.')
vT = 'R$ '+vT+',00'

sL = int(sL)
sL = '{0:,}'.format(sL).replace(',','.')
sL = 'R$ '+sL+',00'

mM = format(mM).replace('.',',')
mM = mM + '%'

cP = str(cP)

mP = format(mP).replace('.',',')
mP = 'R$ ' +mP
Primeiras_Informacoes = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(''+vT+'', className="card-title"),
                    html.P(
                        "Valor Total de Vendas",
                        
                        className="card-text",
                    ),
                   
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(''+sL+'', className="card-title"),
                    html.P(
                        "Lucro Total",
                        
                        className="card-text")
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(''+mM+'', className="card-title"),
                    html.P(
                        "Margem de Lucro",
                        
                        className="card-text")
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(''+cP+'', className="card-title"),
                    html.P(
                        "Quantidade de Pedidos",
                        
                        className="card-text")
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(''+mP+'', className="card-title"),
                    html.P(
                        "Valor Médio de Pedidos",
                        
                        className="card-text")
                ]
            )
        ),
    ]
)

fig= vendasGraf.montaGraficoVxA()
fig2=vendasGraf.montaGraficoVxM()
fig3=vendasGraf.montaGraficoVxS()
fig4=vendasGraf.montaGraficoVxD()
fig5=vendasGraf.montaGraficoVxC()
fig6=vendasGraf.montaGraficoVxR()

linha1_grafico = dbc.CardGroup(
    [
        dbc.Card(
            
            dbc.CardBody(
                [
                    html.H5("Vendas x Ano", className="card-title"),
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
                    html.H5("Vendas x Mês", className="card-title"),
                     dcc.Graph(
                    id='example-graph7',
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
                    html.H5("Vendas x Semana", className="card-title"),
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
                    html.H5("Vendas x Dia", className="card-title"),
                     dcc.Graph(
                    id='example-graph8',
                    figure=fig4
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
                    html.H5("Vendas x Canal", className="card-title"),
                     dcc.Graph(
                    id='example-graph4',
                    figure=fig5
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
                    figure=fig6
                ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            )
        )
        
    ]
)

linha3_grafico = dbc.CardGroup(
    [
        dbc.Card(
            
            dbc.CardBody(
                [
                    html.H5("Vendas x Vendedor", className="card-title"),
                     dcc.Graph(
                    id='example-graph9',
                    figure=fig
                    ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            )
        ),
        
        
    ]
)




layout =html.Div([Primeiras_Informacoes, linha1_grafico, linha2_grafico]) 

