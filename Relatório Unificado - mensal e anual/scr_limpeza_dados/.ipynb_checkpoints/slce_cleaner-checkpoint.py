# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 14:39:46 2023

@author: d850398
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import copy

# Limpa os dados extraídos

class SlceTableCleaner():
    
    def __init__(self):
        
        data_autal = datetime.now()
        self.TODAY = data_autal.strftime('%Y.%m.%d')
        
        self.data_extracao = self.TODAY # ou data manual
    
    def table_reader(self, filename):
        
        with open(filename, 'r') as strange_file:
            file = strange_file.read()
            
        strange_symbol = file[3]
        cleaned_file = file.replace(strange_symbol, '')

        soup = BeautifulSoup(cleaned_file, 'html.parser')
        
        table_container = [[i.text for i in row.find_all('td')] for row in soup.find_all('tr')]

        return pd.DataFrame(table_container[1:], columns=table_container[0])
        
    
    def clean_slce_tabela_principal(self):
        #####################################################
        ######## Limpando dados da planilha principal #######
        #####################################################
        slce_main = self.table_reader('files/arquivo/slce_principal_raw.xls')
        
        # <<<<< padronizando nomes de colunas >>>>>
        slce_main.columns = ['n_processo', 'data_autuacao', 'assunto', 'coord_atual', 'status']
        
        # <<<<< criando a coluna de data de extração >>>>>
        data = [self.data_extracao for i in range(slce_main.shape[0])]
        
        slce_main['data_extracao'] = data
        
        slce_main.to_csv('files/slce_principal.csv', encoding='latin-1', sep=';', index=False)
              
   
    def clean_slce_tabela_despachos(self):    
        ######################################################
        ####### Limpando dados da planilha de despachos ######
        ######################################################
        slce_despachos = self.table_reader('files/arquivo/slce_despachos_raw.xls')
        
        # <<<<< padronizando nomes de colunas >>>>>
        slce_despachos.columns = ['n_processo', 'deferido', 'data_despacho', 'coord_despacho', 'situacao']
        
        # Transformando valores de string vazios ('') em NaN
        slce_despachos.replace('', np.nan, inplace=True)
        
        # <<<<< excluindo processos sem data de deferimento >>>>>
        slce_despachos = slce_despachos.query("data_despacho.notnull()")
        
        # <<<<< criando a coluna de data de extração >>>>>
        data = [self.data_extracao for i in range(slce_despachos.shape[0])]
        slce_despachos['data_extracao'] = data
    
        slce_despachos.to_csv('files/slce_despachos.csv', encoding='latin-1', sep=';', index=False)
        
    
    def clean_slce_tabela_comuniqueses(self):       
        #############################################################
        ####### Filtrando dados da planilha de comunique-ses ########
        #############################################################
        slce_comuniqueses = self.table_reader('files/arquivo/slce_comuniqueses_raw.xls')
        
        # <<<<< padronizando nomes de colunas >>>>>
        slce_comuniqueses.columns = ['n_processo', 'data_comuniquese', 'coord_comuniquese']
        
        
        # <<<<< criando a coluna de data de extração >>>>>
        data = [self.data_extracao for i in range(slce_comuniqueses.shape[0])]
        slce_comuniqueses['data_extracao'] = data
    
        slce_comuniqueses.to_csv('files/slce_comuniqueses.csv', encoding='latin-1', sep=';', index=False)
        
        
    def clean_table(self):
        #<<<<< Limpando tabelas do AD>>>>>>
        self.clean_slce_tabela_principal()
        print("Tabela principal do SLCe criada com sucesso!")
        self.clean_slce_tabela_despachos()
        print("Tabela de despachos do SLCe criada com sucesso!")
        self.clean_slce_tabela_comuniqueses()
        print("Tabela de comuniqueses do SLCe criada com sucesso!")

    
if __name__ == '__main__':
    SlceTableCleaner().clean_table()