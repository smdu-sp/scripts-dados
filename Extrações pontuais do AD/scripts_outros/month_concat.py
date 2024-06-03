import pandas as pd
import os
import glob


dir_atual = os.getcwd()
padrao = os.path.join(dir_atual, 'dom' + '*.csv')

nomes_arquivos = glob.glob(padrao)

df_list = [pd.read_csv(i, sep=';') for i in nomes_arquivos]

df_final = pd.concat(df_list)

df_final.to_csv('dom_concat.csv', sep=';', index=False)