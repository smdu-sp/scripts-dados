import copy
import logging  # Debug
import warnings  # silenciar o aviso de descontinuidade do pandas.append()
from su_constructor import FullAd, output_csv, remove_file   # contrutor basico de planilhas
from su_connection import connection
import os
import pandas as pd
from bson.objectid import ObjectId

warnings.simplefilter(action='ignore', category=FutureWarning) # Silenciando os warning de append do pandas
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TableExtract(FullAd):
    """Cria a planilha principal completa. Herda da classe FullAd que faz o processamento dos dados em json
    extraídos do sistema"""

    def __init__(self, env='prod'):
        super().__init__()

        self.collection = connection(env)

    def tabela(self):

        # Criando atributos (colunas) e atribuindo a estes o valor None (nulo)
        attributes = ['id', 'protocolo', 'n_processo', 'taxa_nome', 'valor', 'arrecadado', 'data_validade']

        data_container = {i: None for i in attributes}

        data_line = []

        # DATA CONTAINER
        data_container['id'] = self.get_id()
        data_container['protocolo'] = self.get_ad()
        data_container['n_processo'] = self.get_sei()[0]

        tax_node = self.data.get('taxas')
        data_node = tax_node.get('data') if tax_node else []

        for item in data_node:
            data_container['arrecadado'] = self.get_arrecadado(item)
            data_container['data_validade'] = self.get_data_validade(item)

            reclass_node = item.get('reclassificacoes')
            for reclass in reclass_node:
                data_container['taxa_nome'] = self.get_taxa_nome(reclass)
                data_container['valor'] = self.get_valor_principal(reclass)
                data_line.append(copy.deepcopy(data_container))

        return data_line

    def table_creator(self):

        # Absolute path para o diretório atual
        dir_atual = os.path.abspath(os.path.dirname(__file__))
        # Absolute path para o diretório irmão onde os arquivos serão criados
        dir_raw_data = os.path.abspath(os.path.join(dir_atual, '..', 'arquivos_extracao'))
        logging.info(f'Extraindo documentos para {dir_raw_data}')

        file_path = f'{dir_raw_data}/ad_taxas.csv'

        remove_file(file_path)

        cursor = self.collection.find(
            {},
            {
                "taxas.data": 1,
                "nP": 1,
                "sei.txtCodigoProcedimentoFormatado": 1
            }
        ).batch_size(500)

        dados_extracao = []
        for n, item in enumerate(cursor):
            logging.info(f'{n} > {item.get("_id")}')

            self.data = item
            data_line = self.tabela()
            for i in data_line:
                dados_extracao.append(i)

        df = pd.DataFrame(dados_extracao)
        df['valor'] = df['valor'].apply(lambda x: round(x, 2))
        df.to_csv(file_path, sep=';', decimal=',', encoding='ANSI', index=False)


if __name__ == '__main__':
    TableExtract().table_creator()
