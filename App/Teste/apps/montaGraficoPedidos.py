import psycopg2
import pandas as pd

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
    sql_contaProdutos = 'select count(cod_venda) from historico_2jr'
    sql_principalCategoria = 'SELECT count(categoria_produto), categoria_produto FROM historico_2jr GROUP BY categoria_produto HAVING COUNT(categoria_produto) > 1 ORDER BY count(categoria_produto) DESC' 
    sql_principalMarca = 'SELECT count(marca_produto), marca_produto FROM historico_2jr GROUP BY marca_produto HAVING COUNT(marca_produto) > 1 ORDER BY count(marca_produto) DESC'

#conecta_bd()
    contaProdutos = consulta_bd(sql_contaProdutos)
    principalCategoria = consulta_bd(sql_principalCategoria)
    principalMarca = consulta_bd(sql_principalMarca)

    df_cP = pd.DataFrame(contaProdutos, columns=['Qtd'])
    qtd_cP = df_cP['Qtd'][0]

    df_pC = pd.DataFrame(principalCategoria, columns=['Qtd', 'Categoria'])
    qtd_pC = df_pC['Categoria'][0]

    df_pM = pd.DataFrame(principalMarca, columns=['Qtd', 'Marca'])
    qtd_pM = df_pM['Marca'][0]

    return qtd_cP, qtd_pC, qtd_pM