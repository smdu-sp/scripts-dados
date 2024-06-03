import copy
import logging  # Debug
import warnings  # silenciar o aviso de descontinuidade do pandas.append()
from su_constructor import FullAd, output_csv, remove_file  # contrutor basico de planilhas
from su_connection import connection
import os
import json
import pandas as pd
from bson.objectid import ObjectId

warnings.simplefilter(action='ignore', category=FutureWarning)  # Silenciando os warning de append do pandas
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TableExtract(FullAd):
    """Cria a planilha principal completa. Herda da classe FullAd que faz o processamento dos dados em json
    extraídos do sistema"""

    def __init__(self, env='prod'):
        super().__init__()

        self.collection = connection(env)

    def tabela(self):

        # Criando atributos (colunas) e atribuindo a estes o valor None (nulo)
        attributes = ['id', 'n_processo', 'assunto', 'sql', 'incra', 'area_publica']

        data_container = {i: None for i in attributes}

        data_line = []

        loc = self.get_attrb_localizacao(flat=False)
        sql_value = loc['sql']
        incra_value = loc['incra']
        area_p_value = loc['area_p']
        # DATA CONTAINER
        data_container['id'] = self.get_id()
        data_container['n_processo'] = self.get_sei()[0]
        data_container['assunto'] = self.get_requerimento()

        if isinstance(sql_value, str) or isinstance(incra_value, str) or isinstance(area_p_value, str):
            data_container['sql'] = sql_value
            data_container['incra'] = incra_value
            data_container['area_publica'] = area_p_value
            data_line.append(copy.deepcopy(data_container))
            return data_line

        if isinstance(sql_value, list) or isinstance(incra_value, list) or isinstance(area_p_value, list):
            for n, i in enumerate(range(max(len(sql_value), len(incra_value), len(area_p_value)))):
                data_container['sql'] = sql_value[n] if sql_value else None
                data_container['incra'] = incra_value[n] if incra_value else None
                data_container['area_publica'] = area_p_value[n] if area_p_value else None
                data_line.append(copy.deepcopy(data_container))
        else:
            data_line.append(data_container)

        return data_line

    def table_creator(self):
        """Itera sobre os dados e salva o resultado em arquivo csv

        :return: <void>
        """
        # Absolute path para o diretório atual
        dir_atual = os.path.abspath(os.path.dirname(__file__))
        # Absolute path para o diretório irmão onde os arquivos serão criados
        dir_raw_data = os.path.abspath(os.path.join(dir_atual, '..', 'arquivos_extracao'))
        logging.info(f'Extraindo documentos para {dir_raw_data}')

        # Apagando planilha ANTIGA, se houver
        file_path = f'{dir_raw_data}/bi_contribuintes_raw.csv'

        remove_file(file_path)

        assuntos_excluidos = [
            'Apostilamento',
            'Alvará de implantação de Estação Rádio-Base'
        ]
        with open('j_title_id.json', 'r') as json_file:
            title_id = json.load(json_file)

        cursor = self.collection.find(
            {
                'sei': {'$exists': True},
                'timeline': {'$exists': True},
                # 'config_metadata.id': {"$nin": [title_id[i] for i in assuntos_excluidos]}
            },
            {
                'sei': 1,
                'config_metadata.title': 1,
                'last_version': 1
            }
        ).batch_size(100)

        dados_extracao = []
        for n, item in enumerate(cursor):
            logging.info(f'{n} > {item.get("_id")}')

            self.data = item
            data_line = self.tabela()
            for i in data_line:
                output_csv(i, file_path)


if __name__ == '__main__':
    TableExtract().table_creator()
