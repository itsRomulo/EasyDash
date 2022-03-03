import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import vendas, produto, estoque


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Video Games|', href='/apps/vendas'),
        dcc.Link('Other Products', href='/apps/estoque'),
        dcc.Link('Other', href='/apps/produto'),
        
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/vendas':
        return vendas.layout
    if pathname == '/apps/produto':
        return produto.layout
    if pathname == '/apps/estoque':
        return estoque.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
