import plotly as plt
import plotly.express as px
import json
from urllib.request import urlopen
import pandas as pd


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
    title = "Vendas x Região", #title of the map
    #animation_frame = "ano" #creating the application based on the year
    )
    fig.update_geos(fitbounds = "locations", visible = False)
    fig.show()
