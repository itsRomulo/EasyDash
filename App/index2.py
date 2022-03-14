import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
from turtle import color, right
import dash_core_components as dcc

from dash.dependencies import Input, Output

from dash_bootstrap_components._components.Navbar import Navbar

# Autenticacao
import dash_auth

from Dados import consulta_bd

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import vendas, produto, home, notfound, regiao, regiao_prod

import montaGraficoVendas as vGV
import montaGraficoPedidos

import sys
sys.path.insert(1, 'C:/EasyDash')
import pFuncoes as fun

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

dados = fun.json_reader('C:\\EasyDash\\App\\auth.json')
dados_auth=dados['result']
montaAuth={}
cont = 0

for dado in dados_auth:
    montaAuth.update({dado['user']:dado['password']})

autenticacao = dash_auth.BasicAuth(app,montaAuth)

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

def preencheDropDownANO(sqlAno):
    ano = fun.consulta_bd(sqlAno)
    df_ano = pd.DataFrame(ano, columns=['Ano'])
    return df_ano


def preencheDropDownMES(sqlMes):
    mes = fun.consulta_bd(sqlMes)
    df_mes = pd.DataFrame(mes, columns=['Mes'])
    
    return df_mes 


def preencheDropDownDIA(sqlDia):
    dia = fun.consulta_bd(sqlDia)
    df_dia = pd.DataFrame(dia, columns=['Dia'])
    return df_dia

sqlAno = 'SELECT distinct(substring(data_venda, 7, 4)) FROM public.historico_2jr order by substring(data_venda, 7, 4) ASC;'
sqlMes = 'SELECT distinct(substring(data_venda, 4, 2)) FROM public.historico_2jr order by substring(data_venda, 4, 2) ASC;'
sqlDia = 'SELECT distinct(substring(data_venda, 1, 2)) FROM public.historico_2jr order by substring(data_venda, 1, 2) ASC;'
ano = preencheDropDownANO(sqlAno)   
mes = preencheDropDownMES(sqlMes) 
dia = preencheDropDownDIA(sqlDia)


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
                    
                    ano['Ano'],
                    ano['Ano'].values, id = "DropDownAno",
            ), 
                ],
                    label="Ano", 
                ),

            ]),

            html.Br(),

            dbc.Nav([  
                
                dbc.DropdownMenu( id = "DropDownMes",
                 children=[],
                    label="Mês",
                ),
            ]),

            html.Br(),

            dbc.Nav([
                dbc.DropdownMenu(
                 children=[   
                dcc.Checklist(
                    dia['Dia'],
                    dia['Dia'].values, 
                ),
                ],
                    label="Dia", id = "DropDownDia"
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


@app.callback(
    Output("page-content", "children"), 
    Input("url", "pathname") )

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



@app.callback(
    Output(component_id='DropDownMes', component_property='children'), 
    Input(component_id='DropDownAno' , component_property='value')
    )

def changedAno(value):
    
    nAno = (len(value))
    montaSql = 'SELECT distinct(substring(data_venda, 4, 2)) FROM public.historico_2jr'
    if (nAno > 0):
        montaSql += ' where '
    else: 
        montaSql = 'SELECT distinct(substring(data_venda, 4, 2)) FROM public.historico_2jr'    
    for i in range(0, nAno):
        if (i != nAno-1): 
            montaSql +=  "substring(data_venda, 7, 4) = '"+value[i]+"' or "
        else:
            montaSql += "substring(data_venda, 7, 4) = '"+value[i]+"' order by substring(data_venda, 4, 2)  ASC"
    mes = preencheDropDownMES(montaSql) 
    mesesdisponiveis = dcc.Checklist(

                                
                   mes['Mes'],
                   mes['Mes'].values, id = 'DropDownMesCarregado'
              
                ),
    return mesesdisponiveis




@app.callback(
    Output(component_id='DropDownDia', component_property='children'),  
    [Input(component_id='DropDownMesCarregado', component_property='value'),
    Input(component_id='DropDownAno', component_property='value')],
    )

def changedMes(dMes, dAno):
    nMes = len(dMes)
    nAno = len(dAno)
    montaSql = 'SELECT distinct(substring(data_venda, 1, 2)) FROM public.historico_2jr'
    if (nAno > 0):
        montaSql += ' where '
    else: 
        montaSql = 'SELECT distinct(substring(data_venda, 1, 2)) FROM public.historico_2jr'    
    for i in range(0, nAno):
        if (i != nAno-1): 
            montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
        else:
            montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"'"
    
    if (nMes > 0):
        if(nAno == 0):
            diasdisponiveis = ''
            return diasdisponiveis 
        else:
            montaSql += ' and '
            for m in range(0, nMes):
                if (m != nMes-1): 
                    montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                else:
                    montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"' order by (substring(data_venda, 1, 2)) asc"
    dia = preencheDropDownDIA(montaSql) 
    diasdisponiveis = dcc.Checklist(

                                
                   dia['Dia'],
                   dia['Dia'].values, id = 'DropDownDiaCarregado'
              
                ),
    return diasdisponiveis




@app.callback(
    Output(component_id='VxA', component_property='figure'),
    Output(component_id='VxM', component_property='figure'),
    Output(component_id='VxD', component_property='figure'),
    Output(component_id='VxC', component_property='figure'),    
    Input(component_id='DropDownAno', component_property='value'),
    Input(component_id='DropDownMesCarregado', component_property='value'),
    Input(component_id='DropDownDiaCarregado', component_property='value'),
    
    )
def input_output(dAno, dMes, dDia):
    def updateVxA(dAno, dMes, dDia):
        
        nMes = len(dMes)
        nAno = len(dAno)
        montaSql = "select sum(cast(valor_produto as float)), substring(data_venda, 7, 4) from historico_2jr"
        #where substring(data_venda, 7, 4) = '2021' GROUP BY substring(data_venda, 7, 4) ORDER BY substring(data_venda, 7, 4) ASC"
        if (nAno > 0):
            montaSql += ' where '
        else: 
            montaSql = 'SELECT distinct(substring(data_venda, 1, 2)) FROM public.historico_2jr'    
        for i in range(0, nAno):
            if (i != nAno-1): 
                montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
            else:
                montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"' GROUP BY substring(data_venda, 7, 4) ORDER BY substring(data_venda, 7, 4) ASC"
    
        
        fig = vGV.montaGraficoVxA(montaSql)
        return fig

    def updateVxM(dAno, dMes, dDia):
        
        nMes = len(dMes)
        nAno = len(dAno)
        montaSql = 'select sum(cast(valor_produto as float)), substring(data_venda, 4, 2) from historico_2jr'
        if (nAno > 0):
            montaSql += ' where '
        else: 
            montaSql = 'SELECT distinct(substring(data_venda, 1, 2)) FROM public.historico_2jr'    
        for i in range(0, nAno):
            if (i != nAno-1): 
                montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
            else:
                montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"'"

        if (nMes > 0):
            if(nAno == 0):
                diasdisponiveis = ''
                return diasdisponiveis 
            else:
                montaSql += ' and '
                for m in range(0, nMes):
                    if (m != nMes-1): 
                        montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                    else:
                        montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"' GROUP BY substring(data_venda, 4, 2)  ORDER BY substring(data_venda, 4, 2) ASC"  

        
        fig = vGV.montaGraficoVxM(montaSql)
        return fig                      

    def updateVxD(dAno, dMes, dDia):
        nMes = len(dMes)
        nAno = len(dAno)
        montaSql = 'select data_venda, sum(cast(valor_produto as float)) from historico_2jr'
        if (nAno > 0):
            montaSql += ' where '
        else: 
            montaSql = 'select data_venda, sum(cast(valor_produto as float)) from historico_2jr'    
        for i in range(0, nAno):
            if (i != nAno-1): 
                montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
            else:
                montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"'"

        if (nMes > 0):
            if(nAno == 0):
                diasdisponiveis = ''
                return diasdisponiveis 
            else:
                montaSql += ' and '
                for m in range(0, nMes):
                    if (m != nMes-1): 
                        montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                    else:
                        montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"' GROUP BY data_venda  ORDER BY data_venda ASC"  

        
        fig = vGV.montaGraficoVxD(montaSql)
        return fig 

    def updateVxC(dAno, dMes, dDia):
        print(dAno)
        print(dMes)
        print(dDia)
        nMes = len(dMes)
        nAno = len(dAno)
        montaSql = "select count(cod_vendedor) FROM historico_2jr where cod_vendedor = '1' and ("
        montaSql2 = "select count(cod_vendedor) FROM historico_2jr where cod_vendedor <> '1' and ("
        
        if (nAno > 0):
            pass
        else: 
            montaSql = "select count(cod_vendedor) FROM historico_2jr where cod_vendedor = '1'"
            montaSql2 = "select count(cod_vendedor) FROM historico_2jr where cod_vendedor <> '1'"   
        for i in range(0, nAno):
            if (i != nAno-1): 
                montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
                montaSql2 +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
            else:
                montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"
                montaSql2 += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"

        if (nMes > 0):
            if(nAno == 0):
                diasdisponiveis = ''
                return diasdisponiveis 
            else:
                montaSql += ' and ('
                montaSql2 += ' and ('
                for m in range(0, nMes):
                    if (m != nMes-1): 
                        montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                        montaSql2 +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                    else:
                        montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"')"
                        montaSql2 += "substring(data_venda, 4, 2) = '"+dMes[m]+"')"   
        print("---------------")
        print(montaSql)
        print("---------------")
        print(montaSql2)
        print("---------------")
        fig = vGV.montaGraficoVxC(montaSql, montaSql2)
        return fig 

    # def updateVxR(dAno, dMes, dDia):
    #     nMes = len(dMes)
    #     nAno = len(dAno)
    #     montaSql = "SELECT Substring(data_venda,7,4) as ano,uf_venda, case when uf_venda =  'RO' then 'Rondônia' when uf_venda =  'AC' then 'Acre' when uf_venda =  'AM' then 'Amazonas' when uf_venda =  'RR' then 'Roraima' when uf_venda =  'PA' then 'Pará' when uf_venda =  'AP' then 'Amapá' when uf_venda =  'TO' then 'Tocantins' when uf_venda =  'MA' then 'Maranhão' when uf_venda =  'PI' then 'Piauí' when uf_venda =  'CE' then 'Ceará' when uf_venda =  'RN' then 'Rio Grande do Norte' when uf_venda =  'PB' then 'Paraíba' when uf_venda =  'PE' then 'Pernambuco'	when uf_venda =  'AL' then 'Alagoas'	when uf_venda =  'SE' then 'Sergipe'	when uf_venda =  'BA' then 'Bahia'	when uf_venda =  'MG' then 'Minas Gerais'	when uf_venda =  'ES' then 'Espírito Santo'	when uf_venda =  'RJ' then 'Rio de Janeiro'	when uf_venda =  'SP' then 'São Paulo'	when uf_venda =  'PR' then 'Paraná'	when uf_venda =  'SC' then 'Santa Catarina'	when uf_venda =  'RS' then 'Rio Grande do Sul'	when uf_venda =  'MS' then 'Mato Grosso do Sul'	when uf_venda =  'MT' then 'Mato Grosso'	when uf_venda =  'GO' then 'Goiás'	when uf_venda =  'DF' then 'Distrito Federal'	end as estado,sum(cast(valor_produto as float)) as vendas,case when uf_venda =  'RO' then '-11474053'	when uf_venda =  'AC' then '-949865'	when uf_venda =  'AM' then '-3976318'	when uf_venda =  'RR' then '2148823'	when uf_venda =  'PA' then '-4239015'	when uf_venda =  'AP' then '2406605'	when uf_venda =  'TO' then '-9596869'	when uf_venda =  'MA' then '-4042'	when uf_venda =  'PI' then '-6995318'	when uf_venda =  'CE' then '-4354732'	when uf_venda =  'RN' then '-5607038'	when uf_venda =  'PB' then '-6950165'	when uf_venda =  'PE' then '-8140122'	when uf_venda =  'AL' then '-9521841'	when uf_venda =  'SE' then '-8263146'	when uf_venda =  'BA' then '-12197327'	when uf_venda =  'MG' then '-18824095'	when uf_venda =  'ES' then '-19768337'	when uf_venda =  'RJ' then '-227641' when uf_venda =  'SP' then '-22763116'	when uf_venda =  'PR' then '-24722653'	when uf_venda =  'SC' then '-27257104'	when uf_venda =  'RS' then '-30055067'	when uf_venda =  'MS' then '-20616023'	when uf_venda =  'MT' then '-13434091'	when uf_venda =  'GO' then '-168529'	when uf_venda =  'DF' then '-15858437'	end as longitude,case when uf_venda =  'RO' then '-62226545'	when uf_venda =  'AC' then '-69629581'	when uf_venda =  'AM' then '-64399382'	when uf_venda =  'RR' then '-61412437'	when uf_venda =  'PA' then '-52218322'	when uf_venda =  'AP' then '-51428199'	when uf_venda =  'TO' then '-48201864'	when uf_venda =  'MA' then '-45107216' when uf_venda =  'PI' then '-41807852'	when uf_venda =  'CE' then '-39712723'	when uf_venda =  'RN' then '-368261'	when uf_venda =  'PB' then '-35588089'	when uf_venda =  'PE' then '-37779227'	when uf_venda =  'AL' then '-36039082'	when uf_venda =  'SE' then '-35510823'	when uf_venda =  'BA' then '-40191427'	when uf_venda =  'MG' then '-440345'	when uf_venda =  'ES' then '-403565'	when uf_venda =  'RJ' then '-421726'	when uf_venda =  'SP' then '-479046'	when uf_venda =  'PR' then '-5109548' when uf_venda =  'SC' then '-49879454'	when uf_venda =  'RS' then '-52387882'	when uf_venda =  'MS' then '-55095124'	when uf_venda =  'MT' then '-55501919'	when uf_venda =  'GO' then '-511050'	when uf_venda =  'DF' then '-47596956'	end as latitude FROM public.historico_2jr"
    #     if (nAno > 0):
    #         montaSql += ' where '
    #     else: 
    #         montaSql = "SELECT Substring(data_venda,7,4) as ano,uf_venda, case when uf_venda =  'RO' then 'Rondônia' when uf_venda =  'AC' then 'Acre' when uf_venda =  'AM' then 'Amazonas' when uf_venda =  'RR' then 'Roraima' when uf_venda =  'PA' then 'Pará' when uf_venda =  'AP' then 'Amapá' when uf_venda =  'TO' then 'Tocantins' when uf_venda =  'MA' then 'Maranhão' when uf_venda =  'PI' then 'Piauí' when uf_venda =  'CE' then 'Ceará' when uf_venda =  'RN' then 'Rio Grande do Norte' when uf_venda =  'PB' then 'Paraíba' when uf_venda =  'PE' then 'Pernambuco'	when uf_venda =  'AL' then 'Alagoas'	when uf_venda =  'SE' then 'Sergipe'	when uf_venda =  'BA' then 'Bahia'	when uf_venda =  'MG' then 'Minas Gerais'	when uf_venda =  'ES' then 'Espírito Santo'	when uf_venda =  'RJ' then 'Rio de Janeiro'	when uf_venda =  'SP' then 'São Paulo'	when uf_venda =  'PR' then 'Paraná'	when uf_venda =  'SC' then 'Santa Catarina'	when uf_venda =  'RS' then 'Rio Grande do Sul'	when uf_venda =  'MS' then 'Mato Grosso do Sul'	when uf_venda =  'MT' then 'Mato Grosso'	when uf_venda =  'GO' then 'Goiás'	when uf_venda =  'DF' then 'Distrito Federal'	end as estado,sum(cast(valor_produto as float)) as vendas,case when uf_venda =  'RO' then '-11474053'	when uf_venda =  'AC' then '-949865'	when uf_venda =  'AM' then '-3976318'	when uf_venda =  'RR' then '2148823'	when uf_venda =  'PA' then '-4239015'	when uf_venda =  'AP' then '2406605'	when uf_venda =  'TO' then '-9596869'	when uf_venda =  'MA' then '-4042'	when uf_venda =  'PI' then '-6995318'	when uf_venda =  'CE' then '-4354732'	when uf_venda =  'RN' then '-5607038'	when uf_venda =  'PB' then '-6950165'	when uf_venda =  'PE' then '-8140122'	when uf_venda =  'AL' then '-9521841'	when uf_venda =  'SE' then '-8263146'	when uf_venda =  'BA' then '-12197327'	when uf_venda =  'MG' then '-18824095'	when uf_venda =  'ES' then '-19768337'	when uf_venda =  'RJ' then '-227641' when uf_venda =  'SP' then '-22763116'	when uf_venda =  'PR' then '-24722653'	when uf_venda =  'SC' then '-27257104'	when uf_venda =  'RS' then '-30055067'	when uf_venda =  'MS' then '-20616023'	when uf_venda =  'MT' then '-13434091'	when uf_venda =  'GO' then '-168529'	when uf_venda =  'DF' then '-15858437'	end as longitude,case when uf_venda =  'RO' then '-62226545'	when uf_venda =  'AC' then '-69629581'	when uf_venda =  'AM' then '-64399382'	when uf_venda =  'RR' then '-61412437'	when uf_venda =  'PA' then '-52218322'	when uf_venda =  'AP' then '-51428199'	when uf_venda =  'TO' then '-48201864'	when uf_venda =  'MA' then '-45107216' when uf_venda =  'PI' then '-41807852'	when uf_venda =  'CE' then '-39712723'	when uf_venda =  'RN' then '-368261'	when uf_venda =  'PB' then '-35588089'	when uf_venda =  'PE' then '-37779227'	when uf_venda =  'AL' then '-36039082'	when uf_venda =  'SE' then '-35510823'	when uf_venda =  'BA' then '-40191427'	when uf_venda =  'MG' then '-440345'	when uf_venda =  'ES' then '-403565'	when uf_venda =  'RJ' then '-421726'	when uf_venda =  'SP' then '-479046'	when uf_venda =  'PR' then '-5109548' when uf_venda =  'SC' then '-49879454'	when uf_venda =  'RS' then '-52387882'	when uf_venda =  'MS' then '-55095124'	when uf_venda =  'MT' then '-55501919'	when uf_venda =  'GO' then '-511050'	when uf_venda =  'DF' then '-47596956'	end as latitude FROM public.historico_2jr"  
    #     for i in range(0, nAno):
    #         if (i != nAno-1): 
    #             montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
    #         else:
    #             montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"'"

    #     if (nMes > 0):
    #         if(nAno == 0):
    #             diasdisponiveis = ''
    #             return diasdisponiveis 
    #         else:
    #             montaSql += ' and '
    #             for m in range(0, nMes):
    #                 if (m != nMes-1): 
    #                     montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
    #                 else:
    #                     montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"'  group by uf_venda, Substring(data_venda,7,4)"  

    #     print("---------------")
    #     print(montaSql)
    #     print("---------------")
       
    #     fig = vGV.montaGraficoVxR(montaSql)
    #     return fig 

    VxA = updateVxA(dAno, dMes, dDia)
    VxM = updateVxM(dAno, dMes, dDia) 
    VxD = updateVxD(dAno, dMes, dDia) 
    VxC = updateVxC(dAno, dMes, dDia)
    #VxR = updateVxR(dAno, dMes, dDia)  

    return VxA, VxM, VxD, VxC
     
     
# where Substring(data_venda,7,4) = '2022' group by uf_venda, Substring(data_venda,7,4);
#select data_venda, sum(cast(valor_produto as float)) from historico_2jr
#  where substring(data_venda, 7, 4) = '2021' and substring(data_venda, 4, 2) = '03' group by data_venda
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