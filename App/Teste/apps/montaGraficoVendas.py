from operator import index
import psycopg2
import pandas as pd
import plotly.express as px

def conecta_bd():
  con = psycopg2.connect(host="localhost", 
                         database="tcc",
                         user="postgres", 
                         password="256980Jf",
                         port="5432")
  return con


def consulta_bd(sql):
    con = conecta_bd()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    registros = []
    for rec in recset:
        registros.append(rec)
    
    con.close()
    return registros

def montaIndicadores():
  sql_vendaTotal = 'SELECT sum(cast(valor_produto as float)) FROM historico_2jr;'
  sql_somaLucro = 'SELECT sum(cast(lucro_venda as float)) FROM historico_2jr;'
  sql_mediaMargem = 'select cast(avg((cast(lucro_venda as float) * 100)/(cast(custo_produto as float))) as numeric(15,2)) from historico_2jr'
  sql_contaPedidos = 'select count(distinct(cod_venda)) from historico_2jr'
  sql_medioPedidos = 'select cast((sum(cast(valor_produto as float)))/(count(distinct(cod_venda))) as numeric (10,2)) from historico_2jr'
#conecta_bd()
  vendaTotal = consulta_bd(sql_vendaTotal)
  somaLucro = consulta_bd(sql_somaLucro)
  mediaMargem = consulta_bd(sql_mediaMargem)
  contaPedidos = consulta_bd(sql_contaPedidos)
  medioPedidos = consulta_bd(sql_medioPedidos)

  df_vT = pd.DataFrame(vendaTotal, columns=['Valor Total'])
  df_sL = pd.DataFrame(somaLucro, columns=['Valor Total'])
  df_mM = pd.DataFrame(mediaMargem, columns=['Valor Total'])
  df_cP = pd.DataFrame(contaPedidos, columns=['Valor Total'])
  df_mP = pd.DataFrame(medioPedidos, columns=['Valor Total'])

  
  return df_vT['Valor Total'][0], df_sL['Valor Total'][0],df_mM['Valor Total'][0],df_cP['Valor Total'][0],df_mP['Valor Total'][0]

# vendasInternet = consulta_bd("select count(cod_vendedor) FROM historico_2jr where cod_vendedor = '1'")
# vendasFisica = consulta_bd("select count(cod_vendedor) FROM historico_2jr where cod_vendedor <> '1'")


# # This dataframe has 244 lines, but 4 distinct values for `day`
# #d = {'canal':['Internet','Loja Física'], 'qtd':[50,40]
# vI = int(vendasInternet['ValorTotal'])
# vF = int(vendasFisica['ValorTotal'])
# lst = [["Internet",+vI],["Loja Fisica",+vF]] 
# df = pd.DataFrame(lst, columns = ['Canal','qtd'])
# fig = px.pie(df, values='qtd', names='Canal')
# fig.show()


