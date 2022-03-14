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


fig= vendasGraf.montaGraficoVxA('select sum(cast(valor_produto as float)), substring(data_venda, 7, 4) from historico_2jr GROUP BY substring(data_venda, 7, 4) ORDER BY substring(data_venda, 7, 4) ASC')
fig2=vendasGraf.montaGraficoVxM('select sum(cast(valor_produto as float)), substring(data_venda, 4, 2) from historico_2jr GROUP BY substring(data_venda, 4, 2)  ORDER BY substring(data_venda, 4, 2) ASC')

sql_sem1 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '01' and '07' and substring(data_venda, 7, 4) = '2022' and substring(data_venda, 4, 2) = '03'"
sql_sem2 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '08' and '15' and substring(data_venda, 7, 4) = '2022' and substring(data_venda, 4, 2) = '03'"
sql_sem3 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '16' and '22' and substring(data_venda, 7, 4) = '2022' and substring(data_venda, 4, 2) = '03'"
sql_sem4 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '23' and '31' and substring(data_venda, 7, 4) = '2022' and substring(data_venda, 4, 2) = '03'"
  
fig3=vendasGraf.montaGraficoVxS(sql_sem1, sql_sem2, sql_sem3, sql_sem4)


fig4=vendasGraf.montaGraficoVxD("select data_venda, sum(cast(valor_produto as float)) from historico_2jr where substring(data_venda, 7, 4) = '2021' and substring(data_venda, 4, 2) = '03' group by data_venda")

sql_internet = "select count(cod_vendedor) FROM historico_2jr where cod_vendedor = '1'"
sql_lojafisica = "select count(cod_vendedor) FROM historico_2jr where cod_vendedor <> '1'"
fig5=vendasGraf.montaGraficoVxC(sql_internet, sql_lojafisica)


linha1_grafico = dbc.CardGroup(
    [
        dbc.Card(
            
            dbc.CardBody(
                [
                    html.H5("Vendas x Ano (R$)", className="card-title"),
                     dcc.Graph(
                    id='VxA',
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
                    html.H5("Vendas x Mês (R$)", className="card-title"),
                     dcc.Graph(
                    id='VxM',
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
                    html.H5("Vendas x Semana (R$)", className="card-title"),
                    dcc.Graph(
                    id='VxS',
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
                    html.H5("Vendas x Dia (R$)", className="card-title"),
                     dcc.Graph(
                    id='VxD',
                    figure=fig4
                    ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            )
        ),
        
        
    ]
)



linha3_grafico = dbc.CardGroup(
    [
        dbc.Card(
            
            dbc.CardBody(
                [
                    html.H5("Vendas x Canal(Qtd)", className="card-title"),
                     dcc.Graph(
                    id='VxC',
                    figure=fig5
                    ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            )
        ),
        
        
    ]
)

linha5_grafico = dbc.CardGroup(
    [
        dbc.Card(
            
            dbc.CardBody(
                [
                    html.H5("Vendas x Vendedor", className="card-title"),
                     dcc.Graph(
                    id='VxV',
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




layout =html.Div([Primeiras_Informacoes, linha1_grafico, linha2_grafico, linha3_grafico]) 

