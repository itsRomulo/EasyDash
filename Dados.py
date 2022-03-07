#====================================================================================================
# Bibliotecas
import pandas as pd
import numpy as np
import json
import openpyxl
import psycopg2
from datetime import date
import pFuncoes as fun

#===================================================================================================== 
# Funções globais
def json_reader(file):
    with open(file, 'r', encoding='utf8') as f:
        return json.load(f)

#-----------------------------------------------------------------------------------------------------
def diamesano():
    data_atual = date.today()
    data= data_atual.strftime('%d%m%Y')
    return data

#===================================================================================================== 
# Dados (Entrada)
caminhoParam = '.\\00Entrada\\parameters.json'
param        = json_reader(caminhoParam)
arqOrigem    = param['dados']['originPath']+diamesano()+'_2JR_Multimarcas.xlsx'

# Banco de dados
host_bd      = param['bancodedados']['host']
database_bd  = param['bancodedados']['database']
user_bd      = param['bancodedados']['user']
password_bd  = param['bancodedados']['password']
port_bd      = param['bancodedados']['port']
tblStage     = param['bancodedados']['tblStage']
tblHistorico = param['bancodedados']['tblHistorico']
tblER        = param['bancodedados']['tblER']

#===================================================================================================== 
# Funções para o programa
#-----------------------------------------------------------------------------------------------------
def excel_reader(file):
    df = pd.read_excel(file)
    return df

def conecta_bd():
  con = psycopg2.connect(host=host_bd , 
                         database=database_bd,
                         user=user_bd, 
                         password=password_bd,
                         port=port_bd)
  return con

def inserir_bd(sql):
    con = conecta_bd()
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        con.rollback()
        cur.close()
        return 1
    cur.close()

def truncate(table):
    con = conecta_bd()
    cur = con.cursor()
    try:
        cur.execute("TRUNCATE TABLE %s" % table)
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        con.rollback()
        cur.close()
        return 1
    cur.close()

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

#===================================================================================================== 
# Função Principal
def Main():
    df = excel_reader('./00Entrada/'+diamesano()+'_2JR_Multimarcas.xlsx') # lendo xlsx origem
    for col in df: #renomeando colunas
        ncol = col.replace(' ','_')
        df.rename(columns = {col: ncol}, inplace = True)
        if ncol != 'Data':
            df[ncol] = df[ncol].astype(str)

    df['Data']=df['Data'].dt.strftime('%d/%m/%Y')

    truncate(tblStage)
    truncate(tblHistorico)

    for i in df.index:
        sql = "INSERT INTO public."+tblStage+"(data_venda, cod_venda, cod_produto, cod_vendedor, nome_vendedor, categoria_produto, marca_produto, modelo_produto, valor_produto, custo_produto, lucro_venda, cod_cliente, nome_cliente, idade_cliente, uf_venda, sexo_cliente)"
        sql+= "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'); " % (df['Data'][i], df['Codigo_da_Venda'][i], df['Codigo_do_produto'][i], df['codigo_do_vendedor'][i], df['nome_do_vendedor'][i], df['Categoria'][i], df['Marca'][i], df['Modelo'][i], df['Valor'][i], df['Custo'][i], df['Lucro'][i], df['codigo_cliente'][i], df['nome_do_cliente'][i], df['idade'][i], df['UF'][i], df['Sexo'][i])
        inserir_bd(sql)

    # Verifica se tem registros na Stage
    sql = "SELECT count(*) FROM public."+tblStage+";"
    resposta = consulta_bd(sql)
    df_bd = pd.DataFrame(resposta, columns=['quantidade'])
    qtdReg = df_bd['quantidade'][0]
    

    # Verifica a data da Stage
    sql = "SELECT distinct data_venda FROM public."+tblStage+";"
    resstg = consulta_bd(sql)
    df_datas_stg = pd.DataFrame(resstg, columns=['data'])
    dt_stg=[]
    for i in df_datas_stg.index:
        dt_stg.append(df_datas_stg['data'][i])
    
    
    
    # Verifica a data do Historico
    sql = "SELECT distinct data_venda FROM public."+tblHistorico+" "
    if len(dt_stg) > 0:
        sql+= "where "
        cont=0
        for i in dt_stg:
            cont += 1
            if len(dt_stg) == cont:
                sql+= "data_venda = '"+i+"'"
            else:
                sql+= "data_venda = '"+i+"' or "
    sql+=";"
    reshist = consulta_bd(sql)

    if qtdReg > 0:
        if len(reshist) == 0:
            # Verifica a data da Stage
            sql = "SELECT data_venda, cod_venda, cod_produto, cod_vendedor, nome_vendedor, categoria_produto, marca_produto, modelo_produto, valor_produto, custo_produto, lucro_venda, cod_cliente, nome_cliente, idade_cliente, uf_venda, sexo_cliente FROM public."+tblStage+";"
            resSel = consulta_bd(sql)
            df_sel = pd.DataFrame(resSel, columns=['Data','Codigo_da_Venda','Codigo_do_produto','codigo_do_vendedor','nome_do_vendedor','Categoria','Marca','Modelo','Valor','Custo','Lucro','codigo_cliente','nome_do_cliente','idade','UF','Sexo'])

            for i in df_sel.index:
                sql = "INSERT INTO public."+tblHistorico+"(data_venda, cod_venda, cod_produto, cod_vendedor, nome_vendedor, categoria_produto, marca_produto, modelo_produto, valor_produto, custo_produto, lucro_venda, cod_cliente, nome_cliente, idade_cliente, uf_venda, sexo_cliente)"
                sql+= "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'); " % (df['Data'][i], df['Codigo_da_Venda'][i], df['Codigo_do_produto'][i], df['codigo_do_vendedor'][i], df['nome_do_vendedor'][i], df['Categoria'][i], df['Marca'][i], df['Modelo'][i], df['Valor'][i], df['Custo'][i], df['Lucro'][i], df['codigo_cliente'][i], df['nome_do_cliente'][i], df['idade'][i], df['UF'][i], df['Sexo'][i])
                inserir_bd(sql)
        else:
            print('ERRO - Data da Stage já possui no Histórico.')
    else:
        print('ERRO - A tabela Stage está vazia.')
    
if __name__ == "__main__":
	Main()