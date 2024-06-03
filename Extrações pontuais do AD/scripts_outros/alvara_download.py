import os
import pandas as pd
import requests
import copy
import json


def remove_file(*file_path):

    for file in file_path:
        if os.path.exists(file):
            os.remove(file)


dir_atual = os.path.abspath(os.path.dirname(__file__))
# Absolute path para o diretório irmão onde os arquivos serão criados
file_path = os.path.abspath(os.path.join(dir_atual, '..', 'arquivos_extracao', 'alvara_download'))


df = pd.read_csv(file_path + '\\link_alvaras.csv', sep=';', encoding='latin-1')

df_filtro_doc = df[:]

#tabela.to_excel(file_path + r'\aprova_digital.xlsx', index=False)

# Documentos a serem extraídos
links_download = list(zip(df_filtro_doc['link'], df_filtro_doc['np']))

#remove_file('link_alvaras.csv')

# Download documentos
url_api = "https://api.pdfs.portaldolicenciamentosp.com.br/pdfs/print/"
headers = {
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijk5ODk0YTMwNWMxOTFlNTI2N2EyODc0ZmI0MWIwMTcwOWMxNTBmNWUifQ.eyJzdWIiOiJhdXRoMHw2MWUxOWUzYjI2OTUxZjAwMDkwZjA3MGQiLCJpYXQiOjE3MTExMTQ1NDYsImV4cCI6MTcxMTE1MDU0NiwiYXVkIjpbImh0dHBzOi8vYXBpLnByb2R1Y2FvLXNwLnBvcnRhbGRvbGljZW5jaWFtZW50b3NwLmNvbS5ici9hdXRoL2FwaS92Mi8iLCJodHRwczovL2FwaS5wcm9kdWNhby1zcC5wb3J0YWxkb2xpY2VuY2lhbWVudG9zcC5jb20uYnIvYXV0aC91c2VyaW5mbyJdLCJpc3MiOiJodHRwczovL2FwaS5wcm9kdWNhby1zcC5wb3J0YWxkb2xpY2VuY2lhbWVudG9zcC5jb20uYnIvYXV0aC8ifQ.lo0khRZxAnFsNKShtF2DO_VBwwjG_nCZhYkF3HBDV2nc-cUj2Y1MjpE5XlFUWtd0Iv9wpShseb03gDsXfbJi6O5rKAv91oH_9hDX7pGrIwodjrdFJZbokXS73neG89iJ1mW6izMv56qbdVI5w_KQU1Dv5Qa9uNCxdF-GMOLX76c"
}

#links_download = [('https://api.producao-sp.portaldolicenciamentosp.com.br/events/regrasPdf/print/602e893b530b770008bbb60a?template=SaopauloSP/alvara_aprovacao_edificacao_nova_v3.html&function=processComplete&type=url&validLink=https://www.portaldolicenciamentosp.com.br/consulta/process/view/saopaulosp/1351-21-SP-SAO/1cs0&title=Alvar�&devolverDados=false', '1351-21-SP-SAO')]

for link, alv in links_download:
    payload = {
        "url": link
    }

    response = requests.post(url_api, json=payload, headers=headers)
    url_download = json.loads(response.text)['url']

    response_file = requests.get(url_download)

    with open(file_path + f'\\documentos\\{alv}.pdf', 'wb') as arquivo:
        # Escreve o conteúdo do PDF no arquivo local
        arquivo.write(response_file.content)

    if os.path.exists(file_path + f'\\documentos\\{alv}.pdf'):
        print(f'Documento {alv} criado')
    else:
        print(f'ERRO {alv}')

