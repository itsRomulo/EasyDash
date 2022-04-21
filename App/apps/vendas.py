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
import index

import json
from urllib.request import urlopen

import sys
sys.path.insert(1, 'C:/EasyDash/App'),
import montaGraficoVendas as vendasGraf




linha  = dbc.Row(dbc.Card())
pulalinha = html.Br()



sql_vendaTotal = 'SELECT sum(cast(valor_produto as float)) FROM historico_2jr;'
sql_somaLucro = 'SELECT sum(cast(lucro_venda as float)) FROM historico_2jr;'
sql_mediaMargem = 'select cast(avg((cast(lucro_venda as float) * 100)/(cast(custo_produto as float))) as numeric(15,2)) from historico_2jr'
sql_contaPedidos = 'select count(distinct(cod_venda)) from historico_2jr'
sql_medioPedidos = 'select cast((sum(cast(valor_produto as float)))/(count(distinct(cod_venda))) as numeric (10,2)) from historico_2jr'

vT,sL,mM,cP,mP = vendasGraf.montaIndicadores(sql_vendaTotal, sql_somaLucro, sql_mediaMargem, sql_contaPedidos, sql_medioPedidos)
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
                    html.H3(children=[''+vT+''], className="card-title", id = 'IndicadorValorTotalVendas'),
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
                    html.H3(children=[''+sL+''], className="card-title", id = 'IndicadorLucroTotal'),
                    html.P(
                        "Lucro Total",
                        
                        className="card-text")
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(children=[''+mM+''], className="card-title", id = 'IndicadorMargemLucro'),
                    html.P(
                        "Margem de Lucro",
                        
                        className="card-text")
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(children=[''+cP+''], className="card-title", id = 'IndicadorQuantidadePedidos'),
                    html.P(
                        "Quantidade de Pedidos",
                        
                        className="card-text")
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(children=[''+mP+''], className="card-title", id = 'IndicadorValorMedio'),
                    html.P(
                        "Valor Médio de Pedidos",
                        
                        className="card-text")
                ]
            )
        ),
    ]
)


fig= vendasGraf.montaGraficoVxA('select sum(cast(valor_produto as float)), substring(data_venda, 7, 4) from historico_2jr GROUP BY substring(data_venda, 7, 4) ORDER BY substring(data_venda, 7, 4) ASC')
fig2=vendasGraf.montaGraficoVxM('select sum(cast(valor_produto as float)) as valor, substring(data_venda, 4, 2) as mes, substring(data_venda, 7, 4) as ano from historico_2jr GROUP BY substring(data_venda, 4, 2), substring(data_venda, 7, 4) ORDER BY substring(data_venda, 4, 2) ASC, substring(data_venda, 7, 4) ASC')

sql_sem1 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '01' and '07' and substring(data_venda, 7, 4) = '2022' and substring(data_venda, 4, 2) = '03'"
sql_sem2 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '08' and '15' and substring(data_venda, 7, 4) = '2022' and substring(data_venda, 4, 2) = '03'"
sql_sem3 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '16' and '22' and substring(data_venda, 7, 4) = '2022' and substring(data_venda, 4, 2) = '03'"
sql_sem4 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '23' and '31' and substring(data_venda, 7, 4) = '2022' and substring(data_venda, 4, 2) = '03'"
  
fig3=vendasGraf.montaGraficoVxS(sql_sem1, sql_sem2, sql_sem3, sql_sem4, "03", "2022")


fig4=vendasGraf.montaGraficoVxD("select data_venda, sum(cast(valor_produto as float)) from historico_2jr where substring(data_venda, 7, 4) = '2021' and substring(data_venda, 4, 2) = '03' group by data_venda")

sql_internet = "select count(cod_vendedor) FROM historico_2jr where cod_vendedor = '1'"
sql_lojafisica = "select count(cod_vendedor) FROM historico_2jr where cod_vendedor <> '1'"
fig5=vendasGraf.montaGraficoVxC(sql_internet, sql_lojafisica)


# linha1_grafico = dbc.CardGroup(
#     [
#         dbc.Card(
#             children=[
#             dbc.CardBody(
#                 [ 
#                     html.H5("Vendas x Ano (R$)", className="card-title"),
#                      dcc.Graph(
#                     id='VxA',
#                     figure=fig
#                 ),
#                     dbc.Button(
#                         "Exportar", className="mt-auto"
#                     ),
#                 ]
#             ) 
#             ], id = "CardVxA"
#         ),       
#     ]
# )

# linha2_grafico = dbc.CardGroup(
#     [
#         dbc.Card(
#             children=[
#             dbc.CardBody(
#                 [
#                     html.H5("Vendas x Mês (R$)", className="card-title"),
#                      dcc.Graph(
#                     id='VxM',
#                     figure=fig2
#                 ),
#                     dbc.Button(
#                         "Exportar", className="mt-auto"
#                     ),
#                 ]
#             )
#             ], id='CardVxM',
#         ),
        
        
#     ]
# )

# linha3_grafico = dbc.CardGroup(
#     [ 
#         dbc.Card(
#             children=[
#             dbc.CardBody(
#                 [
#                     html.H5("Vendas x Semana (R$)", className="card-title"),
#                     dcc.Graph(
#                     id='VxS',
#                     figure=fig3
#                 ),
#                     dbc.Button(
#                         "Exportar", className="mt-auto"
#                     ),
#                 ]
#             ) ], id='CardVxS',
#         )
        
        
#     ]
# )



# linha4_grafico = dbc.CardGroup(
#     [
#         dbc.Card(
            
#             dbc.CardBody(
#                 [
#                     html.H5("Vendas x Dia (R$)", className="card-title"),
#                      dcc.Graph(
#                     id='VxD',
#                     figure=fig4
#                     ),
#                     dbc.Button(
#                         "Exportar", className="mt-auto"
#                     ),
#                 ]
#             )
#         ),
        
        
#     ]
# )



# linha5_grafico = dbc.CardGroup(
#     [
#         dbc.Card(
            
#             dbc.CardBody(
#                 [
#                     html.H5("Vendas x Canal(Qtd)", className="card-title"),
#                      dcc.Graph(
#                     id='VxC',
#                     figure=fig5
#                     ),
#                     dbc.Button(
#                         "Exportar", className="mt-auto"
#                     ),
#                 ]
#             )
#         ),
        
        
#     ]
# )

# linha6_grafico = dbc.CardGroup(
#     [
#         dbc.Card(
            
            
#         ),
        
        
#     ]
# )



grafico1 = dbc.CardGroup(
    [
        dbc.Card(
            children=[
            dbc.CardBody(
                [ 
                    html.H5("Gráfico 1", className="card-title", id='titGraph1'),
                     dcc.Graph(
                    id='graph1',
                    figure=fig
                ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            ) 
            ], id = "Card1"
        ),       
    ]
)

grafico2 = dbc.CardGroup(
    [
        dbc.Card(
            children=[
            dbc.CardBody(
                [ 
                    html.H5("Gráfico 2", className="card-title", id='titGraph2'),
                     dcc.Graph(
                    id='graph2',
                    figure=fig
                ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            ) 
            ], id = "Card2"
        ),       
    ]
)

grafico3 = dbc.CardGroup(
    [
        dbc.Card(
            children=[
            dbc.CardBody(
                [ 
                    html.H5("Gráfico 3", className="card-title", id='titGraph3'),
                     dcc.Graph(
                    id='graph3',
                    figure=fig
                ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            ) 
            ], id = "Card3"
        ),       
    ]
)


layout =html.Div([index.sidebar, Primeiras_Informacoes, grafico1,grafico2,grafico3]) 

