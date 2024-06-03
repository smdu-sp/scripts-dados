import pandas as pd
import os
from datetime import datetime  # Adcionar coluna data_atual

# Absolute path para o diretório atual
dir_atual = os.getcwd()
# Absolute path para o diretório irmão onde os arquivos serão criados
dir_raw_data = os.path.abspath(os.path.join(dir_atual, '', 'dat_raw')) ## para desenvolvimento '..' _> voltar um dir
dir_cleaned_data = os.path.abspath(os.path.join(dir_atual, '', 'dat_clean'))

dados = pd.read_csv(f'{dir_raw_data}/sissel_despachos_raw.csv', sep=';', encoding='latin-1')

dados['P_ANO_AUTC_PCSS'] = dados['P_ANO_AUTC_PCSS'].astype(str).apply(lambda x: x[12:16])

dados['P_COD_NRO_PCSS'] = dados['P_COD_NRO_PCSS'].astype(str).apply(lambda x: x[12:x.find(")") - 1])

dados['P_COD_DIGI_PCSS'] = dados['P_COD_DIGI_PCSS'].astype(str).apply(lambda x: x[12:13])

dados['P_COD_NRO_PCSS']= dados['P_COD_NRO_PCSS'].astype(str).str.zfill(7)

dados['n_processo'] = (dados['P_ANO_AUTC_PCSS'].astype(str) + '-' + dados['P_COD_NRO_PCSS'].astype(str) + '-' +
                       dados['P_COD_DIGI_PCSS'].astype(str))

dados.drop(['P_ANO_AUTC_PCSS','P_COD_NRO_PCSS','P_COD_DIGI_PCSS'], axis=1, inplace=True)

#if dados['n_processo'].str.len().nunique() == 1:
#    print("Todos os valores na nr_process têm o mesmo comprimento.")
#else:
#    print("Os valores na coluna1 têm comprimentos diferentes.")

today = datetime.now().strftime('%Y.%m.%d')

dados['data_extracao'] = today

dados.to_csv(f'{dir_cleaned_data}/sissel_despachos.csv', index=False, sep=';')

print('SISSEL_CLEAN - Dados do SISSEL despachos limpos com sucesso')

# # Limpando Comuniqueses do SISSEL

dados1 = pd.read_csv(f'{dir_raw_data}/sissel_comuniqueses_raw.csv', sep=';', encoding='latin-1')

dados1['P_COD_NRO_PCSS']= dados1['P_COD_NRO_PCSS'].astype(str).str.zfill(7)

dados1['n_processo'] = (dados1['P_ANO_AUTC_PCSS'].astype(str) + '-' + dados1['P_COD_NRO_PCSS'].astype(str) + '-' +
                        dados1['P_COD_DIGI_PCSS'].astype(str))

dados1.drop(['P_ANO_AUTC_PCSS','P_COD_NRO_PCSS','P_COD_DIGI_PCSS'], axis=1, inplace=True)

# Gravanda data de extração
dados1['data_extracao'] = today

dados1.to_csv(f'{dir_cleaned_data}/sissel_comuniqueses.csv', index=False, sep=';')

print('SISSEL_CLEAN - Dados do SISSEL comuniqueses limpos com sucesso')