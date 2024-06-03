# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 14:39:46 2023

@author: d850398

Limpa os dados extraídos para o SLCe
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import os

data_atual = datetime.now()
TODAY = data_atual.strftime('%Y.%m.%d')
data_extracao = TODAY  # ou data manual

# Absolute path para o diretório atual
dir_atual = os.getcwd()
# Absolute path para o diretório irmão onde os arquivos serão criados
dir_raw_data = os.path.abspath(os.path.join(dir_atual, '', 'dat_raw'))  ## para desenvolvimento '..' _> voltar um dir
dir_cleaned_data = os.path.abspath(os.path.join(dir_atual, '', 'dat_clean'))
    

def table_reader(filename):
    
    with open(filename, 'r') as strange_file:
        file = strange_file.read()
        
    strange_symbol = file[3]
    cleaned_file = file.replace(strange_symbol, '')

    soup = BeautifulSoup(cleaned_file, 'html.parser')
    
    table_container = [[i.text for i in row.find_all('td')] for row in soup.find_all('tr')]

    return pd.DataFrame(table_container[1:], columns=table_container[0])


def clean_slce_tabela_principal():
    # ################################################### #
    # ####### Limpando dados da planilha principal ###### #
    # ################################################### #
    print('Lendo dados da tabela principal')
    slce_main = table_reader(f'{dir_raw_data}/slce_principal_raw.xls')
    
    # <<<<< padronizando nomes de colunas >>>>>
    slce_main.columns = ['n_processo', 'data_autuacao', 'assunto', 'coord_atual', 'status', 'n_protocolo']
    
    # <<<<< criando a coluna de data de extração >>>>>
    data = [data_extracao for i in range(slce_main.shape[0])]
    
    slce_main['data_extracao'] = data
    
    slce_main.to_csv(f'{dir_cleaned_data}/slce_principal.csv', encoding='latin-1', sep=';', index=False)
    
    
def clean_slce_tabela_despachos():
    # #################################################### #
    # ###### Limpando dados da planilha de despachos ##### #
    # #################################################### #
    print('Lendo dados da tabela de despachos')
    slce_despachos = table_reader(f'{dir_raw_data}/slce_despachos_raw.xls')
    
    # <<<<< padronizando nomes de colunas >>>>>
    slce_despachos.columns = ['n_processo', 'assunto', 'deferido', 'data_despacho', 'coord_despacho', 'situacao',
                              'n_protocolo']
    
    # Transformando valores de string vazios ('') em NaN
    slce_despachos.replace('', np.nan, inplace=True)
    
    # <<<<< excluindo processos sem data de deferimento >>>>>
    slce_despachos = slce_despachos.query("data_despacho.notnull()")
    
    # <<<<< criando a coluna de data de extração >>>>>
    data = [data_extracao for i in range(slce_despachos.shape[0])]
    slce_despachos['data_extracao'] = data

    slce_despachos.to_csv(f'{dir_cleaned_data}/slce_despachos.csv', encoding='latin-1', sep=';', index=False)


def clean_slce_tabela_comuniqueses():       
    # ########################################################### #
    # ###### Filtrando dados da planilha de comunique-ses ####### #
    # ########################################################### #
    print('Lendo dados da tabela de comunique-ses')
    slce_comuniqueses = table_reader(f'{dir_raw_data}/slce_comuniqueses_raw.xls')

    # Para tratar erro da Ana Candida
    slce_comuniqueses = slce_comuniqueses.replace('SMUL/DERPP/CAEPP', 'SMUL/CAEPP/DERPP')

    # <<<<< padronizando nomes de colunas >>>>>
    slce_comuniqueses.columns = ['n_processo', 'data_comuniquese', 'coord_comuniquese', 'n_protocolo']

    # <<<<< criando a coluna de data de extração >>>>>
    data = [data_extracao for i in range(slce_comuniqueses.shape[0])]
    slce_comuniqueses['data_extracao'] = data

    slce_comuniqueses.to_csv(f'{dir_cleaned_data}/slce_comuniqueses.csv', encoding='latin-1', sep=';', index=False)


def clean_table():
    clean_slce_tabela_principal()
    print("SLCE_CLEAN - Tabela principal do SLCe criada com sucesso!")
    clean_slce_tabela_despachos()
    print("SLCE_CLEAN - Tabela de despachos do SLCe criada com sucesso!")
    clean_slce_tabela_comuniqueses()
    print("SLCE_CLEAN - Tabela de comuniqueses do SLCe criada com sucesso!")

    
if __name__ == '__main__':
    clean_table()
