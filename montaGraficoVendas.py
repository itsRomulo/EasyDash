import psycopg2

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
    rows = cur.fetchall() 
    for row in rows:
        row = str(row[0])
        registros = {'ValorTotal':''+row+''}
        
    con.close()
    return registros



sql_vendaTotal = 'SELECT sum(cast(valor as float)) FROM vendas;'
sql_somaLucro = 'SELECT sum(cast(lucro as float)) FROM vendas;'
sql_mediaMargem = 'select cast(avg((cast(lucro as float) * 100)/(cast(custo as float))) as numeric(15,2)) from vendas'
sql_contaPedidos = 'select count(distinct(cod_venda)) from vendas'
sql_medioPedidos = 'select cast((sum(cast(valor as float)))/(count(distinct(cod_venda))) as numeric (10,2)) from vendas'
#conecta_bd()
resSelect = consulta_bd(sql_medioPedidos)

#valor = resSelect["cod_venda"]
print(resSelect['ValorTotal'])


