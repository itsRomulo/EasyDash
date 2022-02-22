#====================================================================================================
# Bibliotecas
import pandas as pd
import numpy as np
import json
import openpyxl
import psycopg2

#===================================================================================================== 
# Dados (Entrada)
param = '.\\00Entrada\\parameters.json'

#===================================================================================================== 
# Funções globais
def json_reader(file):
    with open(file, 'r', encoding='utf8') as f:
        return json.load(f)

#===================================================================================================== 
# Funções para o programa
#-----------------------------------------------------------------------------------------------------
def excel_reader(file):
    df = pd.read_excel(file)
    return df

#===================================================================================================== 
# Função Principal
def Main():
    parametros=json_reader(param)
    print(parametros["originPath"])
    df = excel_reader(parametros['originPath'])
    print(df)
    
if __name__ == "__main__":
	Main()