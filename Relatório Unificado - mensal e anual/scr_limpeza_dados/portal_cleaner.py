import pandas as pd
import os
import glob
from datetime import datetime

# Absolute path para o diretório atual
dir_atual = os.getcwd()
# Absolute path para o diretório irmão onde os arquivos serão criados
dir_raw_data = os.path.abspath(os.path.join(dir_atual, '', 'dat_raw'))
dir_cleaned_data = os.path.abspath(os.path.join(dir_atual, '', 'dat_clean'))

print (dir_atual)
print (dir_raw_data)
print (dir_cleaned_data)

nome_arquivo_raiz = "portal_card-produtividade"

padrao_nome_arquivo = os.path.join(dir_raw_data, nome_arquivo_raiz + "*.xlsx")

nomes_arquivos = glob.glob(padrao_nome_arquivo)

dfs = []

for nome_arquivo in nomes_arquivos:
    df = pd.read_excel(nome_arquivo)
    dfs.append(df)

soma = 0

for i in dfs:
    soma += i.shape[0]
    print(i.shape[0])

print(soma)

df_final = pd.concat(dfs, ignore_index=True)

df_final = df_final.drop(['UsuarioExecutorTarefa','ResultadoTarefa'], axis=1)

# # Criando Planilha de Despachos

desp_filter = ['Despacho de Indeferimento Comum','Despacho de Deferimento Comum']
portal_despachos = df_final.query("TipoDocumentoEmitidoTarefa.isin(@desp_filter)")
portal_despachos.head(10)

portal_despachos = portal_despachos.rename(columns={'Protocolo': 'n_protocolo', 'Processo': 'n_processo',
                                                    'TipoDocumentoEmitidoTarefa': 'despacho',
                                                    'DataUltimaAtualizacao': 'data_despacho'})
portal_despachos.head(10)

portal_despachos['coord_despacho'] = 'GTEC'
portal_despachos.head(10)

today = datetime.now().strftime('%Y.%m.%d')

portal_despachos['data_extracao'] = today
portal_despachos.head(10)

df_final.TipoDocumentoEmitidoTarefa.unique()

comun_filter = ['Comunique-se','Comunique-se complementar']
portal_comuniqueses = df_final.query("TipoDocumentoEmitidoTarefa.isin(@comun_filter)")
portal_comuniqueses.head(10)

portal_comuniqueses = portal_comuniqueses.drop(['TipoDocumentoEmitidoTarefa'], axis=1)
portal_comuniqueses.head(10)

portal_comuniqueses = portal_comuniqueses.rename(columns={'Protocolo': 'n_protocolo', 'Processo': 'n_processo',
                                                          'DataUltimaAtualizacao': 'data_comuniquese'})
portal_comuniqueses.head(10)

portal_comuniqueses['coord_comuniquese'] = 'GTEC'
portal_comuniqueses.head(10)

portal_comuniqueses['data_extracao'] = today
portal_comuniqueses.head(10)

# # Salvando Arquivos

portal_despachos.to_csv(f'{dir_cleaned_data}/portal_despachos.csv', index=False, sep=';')
print('PORTAL_CLEANER - Tabela de despachos exportada com sucesso')

portal_comuniqueses.to_csv(f'{dir_cleaned_data}/portal_comuniqueses.csv', index=False, sep=';')
print('PORTAL_CLEANER - Tabela de comuniqueses exportada com sucesso')
