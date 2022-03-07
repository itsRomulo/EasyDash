from operator import index
import psycopg2
import pandas as pd
import plotly.express as px
from datetime import datetime

def conecta_bd():
  con = psycopg2.connect(host="localhost", 
                         database="tcc",
                         user="postgres", 
                         password="17571946735",
                         port="5433")
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

def montaGraficoVxA():
  sql = 'select sum(cast(valor_produto as float)), substring(data_venda, 7, 4) from historico_2jr GROUP BY substring(data_venda, 7, 4) ORDER BY substring(data_venda, 7, 4) DESC'
  VxA = consulta_bd(sql)
  df_vA = pd.DataFrame(VxA, columns=['Valor','Ano'])
  fig = px.bar(df_vA, x="Ano", y="Valor")
  
  return fig

def montaGraficoVxM():
  sql = 'select sum(cast(valor_produto as float)), substring(data_venda, 4, 2) from historico_2jr GROUP BY substring(data_venda, 4, 2)  ORDER BY substring(data_venda, 4, 2) Desc'
  VxM = consulta_bd(sql)
  df_vM = pd.DataFrame(VxM, columns=['Valor','Mês'])
  fig = px.histogram(df_vM, x="Mês", y="Valor")
  
  return fig

def montaGraficoVxS():
  mesAtual = datetime.now().strftime('%m')
  anoAtual = datetime.now().strftime('%Y')
  sql_sem1 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '01' and '07' and substring(data_venda, 7, 4) = '"+anoAtual+"' and substring(data_venda, 4, 2) = '"+mesAtual+"'"
  sql_sem2 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '08' and '15' and substring(data_venda, 7, 4) = '"+anoAtual+"' and substring(data_venda, 4, 2) = '"+mesAtual+"'"
  sql_sem3 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '16' and '22' and substring(data_venda, 7, 4) = '"+anoAtual+"' and substring(data_venda, 4, 2) = '"+mesAtual+"'"
  sql_sem4 = "select sum(cast(valor_produto as float)) from historico_2jr  where substring(data_venda, 1, 2) between '23' and '31' and substring(data_venda, 7, 4) = '"+anoAtual+"' and substring(data_venda, 4, 2) = '"+mesAtual+"'"
  sem1 = consulta_bd(sql_sem1)
  sem2 = consulta_bd(sql_sem2)
  sem3 = consulta_bd(sql_sem3)
  sem4 = consulta_bd(sql_sem4)
  df_s1 = pd.DataFrame(sem1, columns=['Semana 1'])
  df_s2 = pd.DataFrame(sem2, columns=['Semana 2'])
  df_s3 = pd.DataFrame(sem3, columns=['Semana 3'])
  df_s4 = pd.DataFrame(sem4, columns=['Semana 4'])
  if (df_s1['Semana 1'][0] == None): 
    df_s1['Semana 1'][0] = 8200
  else:  
    df_s1['Semana 1'][0] = int(df_s1['Semana 1'][0])

  if (df_s2['Semana 2'][0] == None): 
    df_s2['Semana 2'][0] = 5000
  else:  
    df_s2['Semana 2'][0] = int(df_s2['Semana 2'][0])

  if (df_s3['Semana 3'][0] == None): 
    df_s3['Semana 3'][0] = 0
  else:  
    df_s3['Semana 3'][0] = int(df_s3['Semana 3'][0])

  if (df_s4['Semana 4'][0] == None): 
    df_s4['Semana 4'][0] = 4000
  else:  
    df_s4['Semana 4'][0] = int(df_s4['Semana 4'][0])
  dfsemana = pd.concat([df_s1, df_s2, df_s3, df_s4], axis=1)
  dfFinal = pd.DataFrame()
  #dfsemana = pd.DataFrame("["+df_s1['Semana 1'][0]+ "," +df_s2['Semana 2'][0]+ "," +df_s3['Semana 3'][0]+","+df_s4['Semana 4'][0]+"]", columns=['Semana 1','Semana 2','Semana 3','Semana 4'])
  print(dfsemana)
  #fig = px.bar(dfsemana, x="Semana 1", title='Life expectancy in Canada')
  fig = px.bar(y=[df_s1['Semana 1'][0],df_s2['Semana 2'][0],df_s3['Semana 3'][0],df_s4['Semana 4'][0]], x=['Semana 1', 'Semana 2', 'Semana 3','Semana 4'], title="Mês Referente:"+mesAtual)

  fig.show()

montaGraficoVxS()



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


