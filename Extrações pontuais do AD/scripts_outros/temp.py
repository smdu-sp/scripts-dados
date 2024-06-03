import requests

url = 'https://api.producao-sp.portaldolicenciamentosp.com.br/events/regrasPdf/print/6363d8d2cb6ad00008c0304d?template=SaopauloSP/alvara_execucao_edificacao_nova_v4.html&function=processComplete&type=url&validLink=https://www.portaldolicenciamentosp.com.br/consulta/process/view/saopaulosp/22344-22-SP-ALV/zd6vvsne&title=Alvará&devolverDados=false'

response = requests.get(url)

print(response.text)