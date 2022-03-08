import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import sys
sys.path.insert(1, 'C:/EasyDash')
import pFuncoes as fun

def montaIndicadores():

    sql_contaProdutos = 'select count(cod_venda) from historico_2jr'
    sql_principalCategoria = 'SELECT count(categoria_produto), categoria_produto FROM historico_2jr GROUP BY categoria_produto HAVING COUNT(categoria_produto) > 1 ORDER BY count(categoria_produto) DESC'
    sql_principalMarca = 'SELECT count(marca_produto), marca_produto FROM historico_2jr GROUP BY marca_produto HAVING COUNT(marca_produto) > 1 ORDER BY count(marca_produto) DESC'

#conecta_bd()
    contaProdutos = fun.consulta_bd(sql_contaProdutos)
    principalCategoria = fun.consulta_bd(sql_principalCategoria)
    principalMarca = fun.consulta_bd(sql_principalMarca)

    df_cP = pd.DataFrame(contaProdutos, columns=['Qtd'])
    qtd_cP = df_cP['Qtd'][0]

    df_pC = pd.DataFrame(principalCategoria, columns=['Qtd', 'Categoria'])
    qtd_pC = df_pC['Categoria'][0]

    df_pM = pd.DataFrame(principalMarca, columns=['Qtd', 'Marca'])
    qtd_pM = df_pM['Marca'][0]

    return qtd_cP, qtd_pC, qtd_pM

def montaGraficoVendasCategoria():
    sql_vendCat = 'SELECT count(categoria_produto), categoria_produto FROM historico_2jr GROUP BY categoria_produto HAVING COUNT(categoria_produto) > 1 ORDER BY count(categoria_produto) DESC'

    vendCat =  fun.consulta_bd(sql_vendCat)

    df_vC = pd.DataFrame(vendCat, columns=['Qtd', 'Categoria'])

    fig = px.bar(df_vC, x='Categoria', y='Qtd')

    return fig

def montaGraficoTop10():
    sql_top10 = 'SELECT count(modelo_produto), modelo_produto, marca_produto FROM historico_2jr GROUP BY modelo_produto, marca_produto HAVING COUNT(modelo_produto) > 1 ORDER BY count(modelo_produto) DESC'

    top10 = fun.consulta_bd(sql_top10)

    df_tP = pd.DataFrame(top10, columns=['Qtd', 'Modelo', 'Marca'])

    fig = go.Figure(go.Bar(
            x=[df_tP['Qtd'][9], df_tP['Qtd'][8], df_tP['Qtd'][7], df_tP['Qtd'][6], df_tP['Qtd'][5], df_tP['Qtd'][4], df_tP['Qtd'][3], df_tP['Qtd'][2], df_tP['Qtd'][1], df_tP['Qtd'][0]],
            y=[df_tP['Marca'][9] +' - ' +df_tP['Modelo'][9], df_tP['Marca'][8] +' - ' +df_tP['Modelo'][8], df_tP['Marca'][7] +' - ' +df_tP['Modelo'][7], df_tP['Marca'][6] +' - ' +df_tP['Modelo'][6], df_tP['Marca'][5] +' - ' +df_tP['Modelo'][5], df_tP['Marca'][4] +' - ' +df_tP['Modelo'][4], df_tP['Marca'][3] +' - ' +df_tP['Modelo'][3], df_tP['Marca'][2] +' - ' +df_tP['Modelo'][2], df_tP['Marca'][1] +' - ' +df_tP['Modelo'][1], df_tP['Marca'][0] +' - ' +df_tP['Modelo'][0]],
            orientation='h'))

    return fig

def montaGraficoVendasMarca():
    sql_vendMarca = 'SELECT count(marca_produto), marca_produto FROM historico_2jr GROUP BY marca_produto HAVING COUNT(marca_produto) > 1 ORDER BY count(marca_produto) DESC'

    vendMarca = fun.consulta_bd(sql_vendMarca)

    df_vM = pd.DataFrame(vendMarca, columns=['Quantidade', 'Marca'])

    df_vM['Marca'][9] = 'Outros'
    linhas = df_vM.shape[0]


    for i in range(10, linhas):
        #print(i)
        df_vM['Quantidade'][9] = df_vM['Quantidade'][i]+df_vM['Quantidade'][9]

        df_vM['Quantidade'][i] = ''

        df_vM['Marca'][i] = ''

    labels = [df_vM['Marca']]

    values = [df_vM['Quantidade']]

    fig = px.pie(df_vM, values='Quantidade', names='Marca')

    #

    return fig

# montaGraficoVendasMarca()