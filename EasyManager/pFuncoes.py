#====================================================================================================
# Bibliotecas
import pandas as pd
import numpy as np
import json
import openpyxl
import psycopg2
from datetime import date

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
caminhoParam = 'C:\\EasyDash\\00Entrada\\parameters.json'
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
                         port=port_bd )
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