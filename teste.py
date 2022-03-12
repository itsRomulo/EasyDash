from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    dcc.Dropdown(
        id = 'dropdown',
   options=[
       {'label': 'New York City', 'value': 'NYC'},
       {'label': 'Montreal', 'value': 'MTL'},
       {'label': 'San Francisco', 'value': 'SF'},
   ],
   value='MTL'
)
])

@app.callback(

    Output(component_id='example-graph', component_property='figure'),
    Input(component_id='dropdown' , component_property='value')

)

def changeDropDown(value):
    if value == 'NYC':
        fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
        return fig



if __name__ == '__main__':
    app.run_server(debug=True)