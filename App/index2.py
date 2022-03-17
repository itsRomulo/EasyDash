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
import montaGraficoPedidos as vGP

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
def input_output_vendas(dAno, dMes, dDia):
    def updateVxA(dAno, dMes, dDia):
        
        nMes = len(dMes)
        nAno = len(dAno)
        montaSql = "select sum(cast(valor_produto as float)), substring(data_venda, 7, 4) from historico_2jr"
        #where substring(data_venda, 7, 4) = '2021' GROUP BY substring(data_venda, 7, 4) ORDER BY substring(data_venda, 7, 4) ASC"
        if (nAno > 0):
            montaSql += ' where '
        else: 
            montaSql = 'select sum(cast(valor_produto as float)), substring(data_venda, 7, 4) from historico_2jr'    
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
            montaSql += ' where ('
        else: 
            montaSql = 'SELECT distinct(substring(data_venda, 1, 2)) FROM public.historico_2jr'    
        for i in range(0, nAno):
            if (i != nAno-1): 
                montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
            else:
                montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"

        if (nMes > 0):
            if(nAno == 0):
                diasdisponiveis = ''
                return diasdisponiveis 
            else:
                montaSql += ' and ('
                for m in range(0, nMes):
                    if (m != nMes-1): 
                        montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                    else:
                        montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"') GROUP BY substring(data_venda, 4, 2)  ORDER BY substring(data_venda, 4, 2) ASC"  

        
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
        
        fig = vGV.montaGraficoVxC(montaSql, montaSql2)
        return fig 

    VxA = updateVxA(dAno, dMes, dDia)
    VxM = updateVxM(dAno, dMes, dDia) 
    VxD = updateVxD(dAno, dMes, dDia) 
    VxC = updateVxC(dAno, dMes, dDia)
    #VxR = updateVxR(dAno, dMes, dDia)  
    
    return VxA, VxM, VxD, VxC
     

@app.callback(

    Output(component_id='IndicadorValorTotalVendas', component_property='children'),
    Output(component_id='IndicadorLucroTotal', component_property='children'),
    Output(component_id='IndicadorMargemLucro', component_property='children'),
    Output(component_id='IndicadorQuantidadePedidos', component_property='children'),
    Output(component_id='IndicadorValorMedio', component_property='children'),     
    Input(component_id='DropDownAno', component_property='value'),
    Input(component_id='DropDownMesCarregado', component_property='value'),
    Input(component_id='DropDownDiaCarregado', component_property='value'),

)

def updateIndicadoresVendas(dAno, dMes, dDia):

        nMes = len(dMes)
        nAno = len(dAno)
        montaSql = "SELECT sum(cast(valor_produto as float)) FROM historico_2jr"
        montaSql2 = "SELECT sum(cast(lucro_venda as float)) FROM historico_2jr"
        montaSql3 = "select cast(avg((cast(lucro_venda as float) * 100)/(cast(custo_produto as float))) as numeric(15,2)) from historico_2jr"
        montaSql4 = "select count(distinct(cod_venda)) from historico_2jr"
        montaSql5 = "select cast((sum(cast(valor_produto as float)))/(count(distinct(cod_venda))) as numeric (10,2)) from historico_2jr"
        if (nAno > 0):
            montaSql += ' where ('
            montaSql2 += ' where ('
            montaSql3 += ' where ('
            montaSql4 += ' where ('
            montaSql5 += ' where ('
        else: 
            montaSql = "SELECT sum(cast(valor_produto as float)) FROM historico_2jr"
            montaSql2 = "SELECT sum(cast(lucro_venda as float)) FROM historico_2jr"
            montaSql3 = "select cast(avg((cast(lucro_venda as float) * 100)/(cast(custo_produto as float))) as numeric(15,2)) from historico_2jr"
            montaSql4 = "select count(distinct(cod_venda)) from historico_2jr"
            montaSql5 = "select cast((sum(cast(valor_produto as float)))/(count(distinct(cod_venda))) as numeric (10,2)) from historico_2jr"   
        for i in range(0, nAno):
            if (i != nAno-1): 
                montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
                montaSql2 +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
                montaSql3 +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
                montaSql4 +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
                montaSql5 +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
                
            else:
                montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"
                montaSql2 += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"
                montaSql3 += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"
                montaSql4 += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"
                montaSql5 += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"
                

        if (nMes > 0):
            if(nAno == 0):
                diasdisponiveis = ''
                return diasdisponiveis 
            else:
                montaSql += ' and ('
                montaSql2 += ' and ('
                montaSql3 += ' and ('
                montaSql4 += ' and ('
                montaSql5 += ' and ('
                
                for m in range(0, nMes):
                    if (m != nMes-1): 
                        montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                        montaSql2 +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                        montaSql3 +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                        montaSql4 +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                        montaSql5 +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                        
                    else:
                        montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"')"
                        montaSql2 += "substring(data_venda, 4, 2) = '"+dMes[m]+"')"
                        montaSql3 += "substring(data_venda, 4, 2) = '"+dMes[m]+"')"
                        montaSql4 += "substring(data_venda, 4, 2) = '"+dMes[m]+"')"
                        montaSql5 += "substring(data_venda, 4, 2) = '"+dMes[m]+"')"
                          
        print()
        vT,sL,mM,cP,mP = vGV.montaIndicadores(montaSql, montaSql2, montaSql3, montaSql4, montaSql5)
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

        return  vT,sL,mM,cP,mP



@app.callback(
    Output(component_id='VxCat', component_property='figure'),
    Output(component_id='VxMarca', component_property='figure'),
    Output(component_id='Top10', component_property='figure'),
    Input(component_id='DropDownAno', component_property='value'),
    Input(component_id='DropDownMesCarregado', component_property='value'),
    Input(component_id='DropDownDiaCarregado', component_property='value'),
    
    )
def input_output_produtos(dAno, dMes, dDia):
    def updateVxCat(dAno, dMes, dDia):
        
        nMes = len(dMes)
        nAno = len(dAno)
        montaSql = "SELECT count(categoria_produto), categoria_produto FROM historico_2jr"
        # GROUP BY categoria_produto HAVING COUNT(categoria_produto) > 1 ORDER BY count(categoria_produto) DESC"
        if (nAno > 0):
            montaSql += ' where ('
        else: 
            montaSql = 'SELECT count(categoria_produto), categoria_produto FROM historico_2jr'    
        for i in range(0, nAno):
            if (i != nAno-1): 
                montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
            else:
                montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"') GROUP BY categoria_produto HAVING COUNT(categoria_produto) > 1 ORDER BY count(categoria_produto) DESC"
    
        
        fig = vGP.montaGraficoVendasCategoria(montaSql)
        return fig

    def updateVxMarca(dAno, dMes, dDia):
        
        nMes = len(dMes)
        nAno = len(dAno)
        montaSql = 'SELECT count(marca_produto), marca_produto FROM historico_2jr'
        if (nAno > 0):
            montaSql += ' where ('
        else: 
            montaSql = 'SELECT count(marca_produto), marca_produto FROM historico_2jr'    
        for i in range(0, nAno):
            if (i != nAno-1): 
                montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
            else:
                montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"

        if (nMes > 0):
            if(nAno == 0):
                diasdisponiveis = ''
                return diasdisponiveis 
            else:
                montaSql += ' and ('
                for m in range(0, nMes):
                    if (m != nMes-1): 
                        montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                    else:
                        montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"') GROUP BY marca_produto HAVING COUNT(marca_produto) > 1 ORDER BY count(marca_produto) DESC"  

        print(montaSql)
        print("----")
        fig = vGP.montaGraficoVendasMarca(montaSql)
        return fig                      

    def updateTop10(dAno, dMes, dDia):
        nMes = len(dMes)
        nAno = len(dAno)
        montaSql = 'SELECT count(modelo_produto), modelo_produto, marca_produto FROM historico_2jr'
        if (nAno > 0):
            montaSql += ' where ('
        else: 
            montaSql = 'SELECT count(modelo_produto), modelo_produto, marca_produto FROM historico_2jr'    
        for i in range(0, nAno):
            if (i != nAno-1): 
                montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
            else:
                montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"

        if (nMes > 0):
            if(nAno == 0):
                diasdisponiveis = ''
                return diasdisponiveis 
            else:
                montaSql += ' and ('
                for m in range(0, nMes):
                    if (m != nMes-1): 
                        montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                    else:
                        montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"') GROUP BY modelo_produto, marca_produto HAVING COUNT(modelo_produto) > 1 ORDER BY count(modelo_produto) DESC"  

        
        fig = vGP.montaGraficoTop10(montaSql)
        return fig 

    

    VxCat = updateVxCat(dAno, dMes, dDia)
    VxMarca = updateVxMarca(dAno, dMes, dDia) 
    Top10 = updateTop10(dAno, dMes, dDia) 
    
    #VxR = updateVxR(dAno, dMes, dDia)  
    
    return VxCat, VxMarca, Top10


@app.callback(

    Output(component_id='IndicadorProdutoVendido', component_property='children'),
    Output(component_id='IndicadorCategoriaVendida', component_property='children'),
    Output(component_id='IndicadorMarcaVendida', component_property='children'),    
    Input(component_id='DropDownAno', component_property='value'),
    Input(component_id='DropDownMesCarregado', component_property='value'),
    Input(component_id='DropDownDiaCarregado', component_property='value'),

)

def updateIndicadoresProdutos(dAno, dMes, dDia):

        nMes = len(dMes)
        nAno = len(dAno)
        montaSql = "select count(cod_venda) from historico_2jr"
        montaSql2 = "SELECT count(categoria_produto), categoria_produto FROM historico_2jr "
        montaSql3 = "SELECT count(marca_produto), marca_produto FROM historico_2jr"
        
        if (nAno > 0):
            montaSql += ' where ('
            montaSql2 += ' where ('
            montaSql3 += ' where ('
            
        else: 
            montaSql = "select count(cod_venda) from historico_2jr"
            montaSql2 = "SELECT count(categoria_produto), categoria_produto FROM historico_2jr GROUP BY categoria_produto HAVING COUNT(categoria_produto) > 1 ORDER BY count(categoria_produto) DESC"
            montaSql3 = "SELECT count(marca_produto), marca_produto FROM historico_2jr GROUP BY marca_produto HAVING COUNT(marca_produto) > 1 ORDER BY count(marca_produto) DESC"
        
        for i in range(0, nAno):
            if (i != nAno-1): 
                montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
                montaSql2 +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
                montaSql3 +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
                
                
            else:
                montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"
                montaSql2 += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"
                montaSql3 += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"
                
                

        if (nMes > 0):
            if(nAno == 0):
                diasdisponiveis = ''
                return diasdisponiveis 
            else:
                montaSql += ' and ('
                montaSql2 += ' and ('
                montaSql3 += ' and ('
                
                
                for m in range(0, nMes):
                    if (m != nMes-1): 
                        montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                        montaSql2 +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                        montaSql3 +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                        
                        
                    else:
                        montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"')"
                        montaSql2 += "substring(data_venda, 4, 2) = '"+dMes[m]+"') GROUP BY categoria_produto HAVING COUNT(categoria_produto) > 1 ORDER BY count(categoria_produto) DESC"
                        montaSql3 += "substring(data_venda, 4, 2) = '"+dMes[m]+"') GROUP BY marca_produto HAVING COUNT(marca_produto) > 1 ORDER BY count(marca_produto) DESC"
                        
                          
        print()
        cP, pC, pM =vGP.montaIndicadores(montaSql, montaSql2, montaSql3)
        cP = str(cP)

       

        return  cP, pC, pM



@app.callback(
    Output(component_id='VxR', component_property='figure'),
    Input(component_id='DropDownAno', component_property='value'),
    Input(component_id='DropDownMesCarregado', component_property='value'),
    Input(component_id='DropDownDiaCarregado', component_property='value'),
)
def output_mapa_regiao(dAno, dMes, dDia):
    print(f'Query 1: \n{dAno} \n\n Query 2: \n {dMes} \n\nQuery 3:  {dDia}\n\n')
    def updateVxR(dAno, dMes, dDia):
            nMes = len(dMes)
            nAno = len(dAno)
            montaSql = "SELECT Substring(data_venda,7,4) as ano,uf_venda, case when uf_venda =  'RO' then 'Rondônia' when uf_venda =  'AC' then 'Acre' when uf_venda =  'AM' then 'Amazonas' when uf_venda =  'RR' then 'Roraima' when uf_venda =  'PA' then 'Pará' when uf_venda =  'AP' then 'Amapá' when uf_venda =  'TO' then 'Tocantins' when uf_venda =  'MA' then 'Maranhão' when uf_venda =  'PI' then 'Piauí' when uf_venda =  'CE' then 'Ceará' when uf_venda =  'RN' then 'Rio Grande do Norte' when uf_venda =  'PB' then 'Paraíba' when uf_venda =  'PE' then 'Pernambuco'	when uf_venda =  'AL' then 'Alagoas'	when uf_venda =  'SE' then 'Sergipe'	when uf_venda =  'BA' then 'Bahia'	when uf_venda =  'MG' then 'Minas Gerais'	when uf_venda =  'ES' then 'Espírito Santo'	when uf_venda =  'RJ' then 'Rio de Janeiro'	when uf_venda =  'SP' then 'São Paulo'	when uf_venda =  'PR' then 'Paraná'	when uf_venda =  'SC' then 'Santa Catarina'	when uf_venda =  'RS' then 'Rio Grande do Sul'	when uf_venda =  'MS' then 'Mato Grosso do Sul'	when uf_venda =  'MT' then 'Mato Grosso'	when uf_venda =  'GO' then 'Goiás'	when uf_venda =  'DF' then 'Distrito Federal'	end as estado,sum(cast(valor_produto as float)) as vendas,case when uf_venda =  'RO' then '-11474053'	when uf_venda =  'AC' then '-949865'	when uf_venda =  'AM' then '-3976318'	when uf_venda =  'RR' then '2148823'	when uf_venda =  'PA' then '-4239015'	when uf_venda =  'AP' then '2406605'	when uf_venda =  'TO' then '-9596869'	when uf_venda =  'MA' then '-4042'	when uf_venda =  'PI' then '-6995318'	when uf_venda =  'CE' then '-4354732'	when uf_venda =  'RN' then '-5607038'	when uf_venda =  'PB' then '-6950165'	when uf_venda =  'PE' then '-8140122'	when uf_venda =  'AL' then '-9521841'	when uf_venda =  'SE' then '-8263146'	when uf_venda =  'BA' then '-12197327'	when uf_venda =  'MG' then '-18824095'	when uf_venda =  'ES' then '-19768337'	when uf_venda =  'RJ' then '-227641' when uf_venda =  'SP' then '-22763116'	when uf_venda =  'PR' then '-24722653'	when uf_venda =  'SC' then '-27257104'	when uf_venda =  'RS' then '-30055067'	when uf_venda =  'MS' then '-20616023'	when uf_venda =  'MT' then '-13434091'	when uf_venda =  'GO' then '-168529'	when uf_venda =  'DF' then '-15858437'	end as longitude,case when uf_venda =  'RO' then '-62226545'	when uf_venda =  'AC' then '-69629581'	when uf_venda =  'AM' then '-64399382'	when uf_venda =  'RR' then '-61412437'	when uf_venda =  'PA' then '-52218322'	when uf_venda =  'AP' then '-51428199'	when uf_venda =  'TO' then '-48201864'	when uf_venda =  'MA' then '-45107216' when uf_venda =  'PI' then '-41807852'	when uf_venda =  'CE' then '-39712723'	when uf_venda =  'RN' then '-368261'	when uf_venda =  'PB' then '-35588089'	when uf_venda =  'PE' then '-37779227'	when uf_venda =  'AL' then '-36039082'	when uf_venda =  'SE' then '-35510823'	when uf_venda =  'BA' then '-40191427'	when uf_venda =  'MG' then '-440345'	when uf_venda =  'ES' then '-403565'	when uf_venda =  'RJ' then '-421726'	when uf_venda =  'SP' then '-479046'	when uf_venda =  'PR' then '-5109548' when uf_venda =  'SC' then '-49879454'	when uf_venda =  'RS' then '-52387882'	when uf_venda =  'MS' then '-55095124'	when uf_venda =  'MT' then '-55501919'	when uf_venda =  'GO' then '-511050'	when uf_venda =  'DF' then '-47596956'	end as latitude FROM public.historico_2jr"
            if (nAno > 0):
                montaSql += ' where ('
            else: 
                montaSql = "SELECT Substring(data_venda,7,4) as ano,uf_venda, case when uf_venda =  'RO' then 'Rondônia' when uf_venda =  'AC' then 'Acre' when uf_venda =  'AM' then 'Amazonas' when uf_venda =  'RR' then 'Roraima' when uf_venda =  'PA' then 'Pará' when uf_venda =  'AP' then 'Amapá' when uf_venda =  'TO' then 'Tocantins' when uf_venda =  'MA' then 'Maranhão' when uf_venda =  'PI' then 'Piauí' when uf_venda =  'CE' then 'Ceará' when uf_venda =  'RN' then 'Rio Grande do Norte' when uf_venda =  'PB' then 'Paraíba' when uf_venda =  'PE' then 'Pernambuco'	when uf_venda =  'AL' then 'Alagoas'	when uf_venda =  'SE' then 'Sergipe'	when uf_venda =  'BA' then 'Bahia'	when uf_venda =  'MG' then 'Minas Gerais'	when uf_venda =  'ES' then 'Espírito Santo'	when uf_venda =  'RJ' then 'Rio de Janeiro'	when uf_venda =  'SP' then 'São Paulo'	when uf_venda =  'PR' then 'Paraná'	when uf_venda =  'SC' then 'Santa Catarina'	when uf_venda =  'RS' then 'Rio Grande do Sul'	when uf_venda =  'MS' then 'Mato Grosso do Sul'	when uf_venda =  'MT' then 'Mato Grosso'	when uf_venda =  'GO' then 'Goiás'	when uf_venda =  'DF' then 'Distrito Federal'	end as estado,sum(cast(valor_produto as float)) as vendas,case when uf_venda =  'RO' then '-11474053'	when uf_venda =  'AC' then '-949865'	when uf_venda =  'AM' then '-3976318'	when uf_venda =  'RR' then '2148823'	when uf_venda =  'PA' then '-4239015'	when uf_venda =  'AP' then '2406605'	when uf_venda =  'TO' then '-9596869'	when uf_venda =  'MA' then '-4042'	when uf_venda =  'PI' then '-6995318'	when uf_venda =  'CE' then '-4354732'	when uf_venda =  'RN' then '-5607038'	when uf_venda =  'PB' then '-6950165'	when uf_venda =  'PE' then '-8140122'	when uf_venda =  'AL' then '-9521841'	when uf_venda =  'SE' then '-8263146'	when uf_venda =  'BA' then '-12197327'	when uf_venda =  'MG' then '-18824095'	when uf_venda =  'ES' then '-19768337'	when uf_venda =  'RJ' then '-227641' when uf_venda =  'SP' then '-22763116'	when uf_venda =  'PR' then '-24722653'	when uf_venda =  'SC' then '-27257104'	when uf_venda =  'RS' then '-30055067'	when uf_venda =  'MS' then '-20616023'	when uf_venda =  'MT' then '-13434091'	when uf_venda =  'GO' then '-168529'	when uf_venda =  'DF' then '-15858437'	end as longitude,case when uf_venda =  'RO' then '-62226545'	when uf_venda =  'AC' then '-69629581'	when uf_venda =  'AM' then '-64399382'	when uf_venda =  'RR' then '-61412437'	when uf_venda =  'PA' then '-52218322'	when uf_venda =  'AP' then '-51428199'	when uf_venda =  'TO' then '-48201864'	when uf_venda =  'MA' then '-45107216' when uf_venda =  'PI' then '-41807852'	when uf_venda =  'CE' then '-39712723'	when uf_venda =  'RN' then '-368261'	when uf_venda =  'PB' then '-35588089'	when uf_venda =  'PE' then '-37779227'	when uf_venda =  'AL' then '-36039082'	when uf_venda =  'SE' then '-35510823'	when uf_venda =  'BA' then '-40191427'	when uf_venda =  'MG' then '-440345'	when uf_venda =  'ES' then '-403565'	when uf_venda =  'RJ' then '-421726'	when uf_venda =  'SP' then '-479046'	when uf_venda =  'PR' then '-5109548' when uf_venda =  'SC' then '-49879454'	when uf_venda =  'RS' then '-52387882'	when uf_venda =  'MS' then '-55095124'	when uf_venda =  'MT' then '-55501919'	when uf_venda =  'GO' then '-511050'	when uf_venda =  'DF' then '-47596956'	end as latitude FROM public.historico_2jr  group by uf_venda, Substring(data_venda,7,4);"  
            for i in range(0, nAno):
                if (i != nAno-1): 
                    montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
                else:
                    montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"

            if (nMes > 0):
                if(nAno == 0):
                    diasdisponiveis = ''
                    return diasdisponiveis 
                else:
                    montaSql += ' and ('
                    for m in range(0, nMes):
                        if (m != nMes-1): 
                            montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                        else:
                            montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"') group by uf_venda, Substring(data_venda,7,4);"  

            print("---------------")
            print(montaSql)
            print("---------------")
        
            fig = vGV.montaGraficoVxR(montaSql)
            return fig 

    VxR = updateVxR(dAno, dMes, dDia)
    
    return VxR

@app.callback(
    Output(component_id='PxR', component_property='figure'),
    Input(component_id='DropDownAno', component_property='value'),
    Input(component_id='DropDownMesCarregado', component_property='value'),
    Input(component_id='DropDownDiaCarregado', component_property='value'),
)
def output_mapa_regiao_prod(dAno, dMes, dDia):
    
    def updatePxR(dAno, dMes, dDia):
        nMes = len(dMes)
        nAno = len(dAno)
        montaSql = "SELECT ano, uf_venda, estado, categoria_produto, cnt, longitude, latitude FROM (SELECT Substring(data_venda, 7, 4) AS ano, categoria_produto, uf_venda, COUNT(*) as cnt, CASE WHEN uf_venda = 'RO' THEN 'Rondônia' WHEN uf_venda = 'AC' THEN 'Acre' WHEN uf_venda = 'AM' THEN 'Amazonas' WHEN uf_venda = 'RR' THEN 'Roraima' WHEN uf_venda = 'PA' THEN 'Pará' WHEN uf_venda = 'AP' THEN 'Amapá' WHEN uf_venda = 'TO' THEN 'Tocantins' WHEN uf_venda = 'MA' THEN 'Maranhão' WHEN uf_venda = 'PI' THEN 'Piauí' WHEN uf_venda = 'CE' THEN 'Ceará' WHEN uf_venda = 'RN' THEN 'Rio Grande do Norte' WHEN uf_venda = 'PB' THEN 'Paraíba' WHEN uf_venda = 'PE' THEN 'Pernambuco' WHEN uf_venda = 'AL' THEN 'Alagoas' WHEN uf_venda = 'SE' THEN 'Sergipe' WHEN uf_venda = 'BA' THEN 'Bahia' WHEN uf_venda = 'MG' THEN 'Minas Gerais' WHEN uf_venda = 'ES' THEN 'Espírito Santo' WHEN uf_venda = 'RJ' THEN 'Rio de Janeiro' WHEN uf_venda = 'SP' THEN 'São Paulo' WHEN uf_venda = 'PR' THEN 'Paraná' WHEN uf_venda = 'SC' THEN 'Santa Catarina' WHEN uf_venda = 'RS' THEN 'Rio Grande do Sul' WHEN uf_venda = 'MS' THEN 'Mato Grosso do Sul' WHEN uf_venda = 'MT' THEN 'Mato Grosso' WHEN uf_venda = 'GO' THEN 'Goiás' WHEN uf_venda = 'DF' THEN 'Distrito Federal' END AS estado, CASE WHEN uf_venda = 'RO' THEN '-11474053' WHEN uf_venda = 'AC' THEN '-949865' WHEN uf_venda = 'AM' THEN '-3976318' WHEN uf_venda = 'RR' THEN '2148823' WHEN uf_venda = 'PA' THEN '-4239015' WHEN uf_venda = 'AP' THEN '2406605' WHEN uf_venda = 'TO' THEN '-9596869' WHEN uf_venda = 'MA' THEN '-4042' WHEN uf_venda = 'PI' THEN '-6995318' WHEN uf_venda = 'CE' THEN '-4354732' WHEN uf_venda = 'RN' THEN '-5607038' WHEN uf_venda = 'PB' THEN '-6950165' WHEN uf_venda = 'PE' THEN '-8140122' WHEN uf_venda = 'AL' THEN '-9521841' WHEN uf_venda = 'SE' THEN '-8263146' WHEN uf_venda = 'BA' THEN '-12197327' WHEN uf_venda = 'MG' THEN '-18824095' WHEN uf_venda = 'ES' THEN '-19768337' WHEN uf_venda = 'RJ' THEN '-227641' WHEN uf_venda = 'SP' THEN '-22763116' WHEN uf_venda = 'PR' THEN '-24722653' WHEN uf_venda = 'SC' THEN '-27257104' WHEN uf_venda = 'RS' THEN '-30055067' WHEN uf_venda = 'MS' THEN '-20616023' WHEN uf_venda = 'MT' THEN '-13434091' WHEN uf_venda = 'GO' THEN '-168529' WHEN uf_venda = 'DF' THEN '-15858437' END AS longitude, CASE WHEN uf_venda = 'RO' THEN '-62226545' WHEN uf_venda = 'AC' THEN '-69629581' WHEN uf_venda = 'AM' THEN '-64399382' WHEN uf_venda = 'RR' THEN '-61412437' WHEN uf_venda = 'PA' THEN '-52218322' WHEN uf_venda = 'AP' THEN '-51428199' WHEN uf_venda = 'TO' THEN '-48201864' WHEN uf_venda = 'MA' THEN '-45107216' WHEN uf_venda = 'PI' THEN '-41807852' WHEN uf_venda = 'CE' THEN '-39712723' WHEN uf_venda = 'RN' THEN '-368261' WHEN uf_venda = 'PB' THEN '-35588089' WHEN uf_venda = 'PE' THEN '-37779227' WHEN uf_venda = 'AL' THEN '-36039082' WHEN uf_venda = 'SE' THEN '-35510823' WHEN uf_venda = 'BA' THEN '-40191427' WHEN uf_venda = 'MG' THEN '-440345' WHEN uf_venda = 'ES' THEN '-403565' WHEN uf_venda = 'RJ' THEN '-421726' WHEN uf_venda = 'SP' THEN '-479046' WHEN uf_venda = 'PR' THEN '-5109548' WHEN uf_venda = 'SC' THEN '-49879454' WHEN uf_venda = 'RS' THEN '-52387882' WHEN uf_venda = 'MS' THEN '-55095124' WHEN uf_venda = 'MT' THEN '-55501919' WHEN uf_venda = 'GO' THEN '-511050' WHEN uf_venda = 'DF' THEN '-47596956' END AS latitude, ROW_NUMBER() OVER (PARTITION BY uf_venda ORDER BY COUNT(*) DESC) as seqnum FROM public.historico_2jr"
        if (nAno > 0):
            montaSql += ' where ('
        else: 
            montaSql = "SELECT ano, uf_venda, estado, categoria_produto, cnt, longitude, latitude FROM (SELECT Substring(data_venda, 7, 4) AS ano, categoria_produto, uf_venda, COUNT(*) as cnt, CASE WHEN uf_venda = 'RO' THEN 'Rondônia' WHEN uf_venda = 'AC' THEN 'Acre' WHEN uf_venda = 'AM' THEN 'Amazonas' WHEN uf_venda = 'RR' THEN 'Roraima' WHEN uf_venda = 'PA' THEN 'Pará' WHEN uf_venda = 'AP' THEN 'Amapá' WHEN uf_venda = 'TO' THEN 'Tocantins' WHEN uf_venda = 'MA' THEN 'Maranhão' WHEN uf_venda = 'PI' THEN 'Piauí' WHEN uf_venda = 'CE' THEN 'Ceará' WHEN uf_venda = 'RN' THEN 'Rio Grande do Norte' WHEN uf_venda = 'PB' THEN 'Paraíba' WHEN uf_venda = 'PE' THEN 'Pernambuco' WHEN uf_venda = 'AL' THEN 'Alagoas' WHEN uf_venda = 'SE' THEN 'Sergipe' WHEN uf_venda = 'BA' THEN 'Bahia' WHEN uf_venda = 'MG' THEN 'Minas Gerais' WHEN uf_venda = 'ES' THEN 'Espírito Santo' WHEN uf_venda = 'RJ' THEN 'Rio de Janeiro' WHEN uf_venda = 'SP' THEN 'São Paulo' WHEN uf_venda = 'PR' THEN 'Paraná' WHEN uf_venda = 'SC' THEN 'Santa Catarina' WHEN uf_venda = 'RS' THEN 'Rio Grande do Sul' WHEN uf_venda = 'MS' THEN 'Mato Grosso do Sul' WHEN uf_venda = 'MT' THEN 'Mato Grosso' WHEN uf_venda = 'GO' THEN 'Goiás' WHEN uf_venda = 'DF' THEN 'Distrito Federal' END AS estado, CASE WHEN uf_venda = 'RO' THEN '-11474053' WHEN uf_venda = 'AC' THEN '-949865' WHEN uf_venda = 'AM' THEN '-3976318' WHEN uf_venda = 'RR' THEN '2148823' WHEN uf_venda = 'PA' THEN '-4239015' WHEN uf_venda = 'AP' THEN '2406605' WHEN uf_venda = 'TO' THEN '-9596869' WHEN uf_venda = 'MA' THEN '-4042' WHEN uf_venda = 'PI' THEN '-6995318' WHEN uf_venda = 'CE' THEN '-4354732' WHEN uf_venda = 'RN' THEN '-5607038' WHEN uf_venda = 'PB' THEN '-6950165' WHEN uf_venda = 'PE' THEN '-8140122' WHEN uf_venda = 'AL' THEN '-9521841' WHEN uf_venda = 'SE' THEN '-8263146' WHEN uf_venda = 'BA' THEN '-12197327' WHEN uf_venda = 'MG' THEN '-18824095' WHEN uf_venda = 'ES' THEN '-19768337' WHEN uf_venda = 'RJ' THEN '-227641' WHEN uf_venda = 'SP' THEN '-22763116' WHEN uf_venda = 'PR' THEN '-24722653' WHEN uf_venda = 'SC' THEN '-27257104' WHEN uf_venda = 'RS' THEN '-30055067' WHEN uf_venda = 'MS' THEN '-20616023' WHEN uf_venda = 'MT' THEN '-13434091' WHEN uf_venda = 'GO' THEN '-168529' WHEN uf_venda = 'DF' THEN '-15858437' END AS longitude, CASE WHEN uf_venda = 'RO' THEN '-62226545' WHEN uf_venda = 'AC' THEN '-69629581' WHEN uf_venda = 'AM' THEN '-64399382' WHEN uf_venda = 'RR' THEN '-61412437' WHEN uf_venda = 'PA' THEN '-52218322' WHEN uf_venda = 'AP' THEN '-51428199' WHEN uf_venda = 'TO' THEN '-48201864' WHEN uf_venda = 'MA' THEN '-45107216' WHEN uf_venda = 'PI' THEN '-41807852' WHEN uf_venda = 'CE' THEN '-39712723' WHEN uf_venda = 'RN' THEN '-368261' WHEN uf_venda = 'PB' THEN '-35588089' WHEN uf_venda = 'PE' THEN '-37779227' WHEN uf_venda = 'AL' THEN '-36039082' WHEN uf_venda = 'SE' THEN '-35510823' WHEN uf_venda = 'BA' THEN '-40191427' WHEN uf_venda = 'MG' THEN '-440345' WHEN uf_venda = 'ES' THEN '-403565' WHEN uf_venda = 'RJ' THEN '-421726' WHEN uf_venda = 'SP' THEN '-479046' WHEN uf_venda = 'PR' THEN '-5109548' WHEN uf_venda = 'SC' THEN '-49879454' WHEN uf_venda = 'RS' THEN '-52387882' WHEN uf_venda = 'MS' THEN '-55095124' WHEN uf_venda = 'MT' THEN '-55501919' WHEN uf_venda = 'GO' THEN '-511050' WHEN uf_venda = 'DF' THEN '-47596956' END AS latitude, ROW_NUMBER() OVER (PARTITION BY uf_venda ORDER BY COUNT(*) DESC) as seqnum FROM public.historico_2jr WHERE Substring(data_venda, 7, 4) = '2022' GROUP BY categoria_produto, uf_venda, Substring(data_venda, 7, 4) ) ct WHERE seqnum = 1"  
        for i in range(0, nAno):
            if (i != nAno-1): 
                montaSql +=  "substring(data_venda, 7, 4) = '"+dAno[i]+"' or "
            else:
                montaSql += "substring(data_venda, 7, 4) = '"+dAno[i]+"')"
        if (nMes > 0):
            if(nAno == 0):
                diasdisponiveis = ''
                return diasdisponiveis 
            else:
                montaSql += ' and ('
                for m in range(0, nMes):
                    if (m != nMes-1): 
                        montaSql +=  "substring(data_venda, 4, 2) = '"+dMes[m]+"' or "
                    else:
                        montaSql += "substring(data_venda, 4, 2) = '"+dMes[m]+"') GROUP BY categoria_produto, uf_venda, Substring(data_venda, 7, 4) ) ct WHERE seqnum = 1;" 
        print("---------------")
        print(montaSql)
        print("---------------")
    
        fig = vGP.montaGraficoProdutosRegiao(montaSql)
        return fig 
    PxR = updatePxR(dAno, dMes, dDia)
    return PxR




@app.callback(
    Output(component_id='CardVxA', component_property='children'),
    
    Input(component_id='DropDownAno', component_property='value'),
    
)
def TelaVxA(dAno):
    
    def cardVxA(dAno):
        
        nAno = len(dAno)
        if nAno == 1:
            
            return ''
            
        else: 
            cardVxA = dbc.CardBody(
                [ 
                    html.H5("Vendas x Ano (R$)", className="card-title"),
                     dcc.Graph(
                    id='VxA',
                    figure=''
                ),
                    dbc.Button(
                        "Exportar", className="mt-auto"
                    ),
                ]
            ) 
            
            return cardVxA
    
    

    cardVxA = cardVxA(dAno)
   

    return cardVxA





if __name__ == "__main__":
    app.run_server(port=8888)



 