import copy
import json
import logging  # Debug
import warnings  # silenciar o aviso de descontinuidade do pandas.append()
from su_constructor import remove_file  # contrutor basico de planilhas
from su_connection import connection
import os
import re
from bson.objectid import ObjectId

warnings.simplefilter(action='ignore', category=FutureWarning)  # Silenciando os warning de append do pandas
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TableExtract():
    """Cria a planilha principal completa. Herda da classe FullAd que faz o processamento dos dados em json
    extraídos do sistema"""

    def __init__(self, env='prod'):
        super().__init__()

        self.collection = connection(env, 'process')
        self.file_path = ''

    def table_creator(self):
        """Itera sobre os dados e salva o resultado em arquivo csv

        :return: <void>
        """
        # Absolute path para o diretório atual
        dir_atual = os.path.abspath(os.path.dirname(__file__))

        # Apagando planilha ANTIGA, se houver
        self.file_path = f'{dir_atual}/title_id.json'
        remove_file(self.file_path)

        cursor = self.collection.find({}, {'config_metadata.title': 1, 'config_metadata.id': 1})

        data_container = {}
        for n, item in enumerate(cursor):
            logging.info(f'{n} > {item.get("_id")}')

            assunto_id = item['config_metadata']['id']
            assunto_title = item['config_metadata']['title']
            data_container[assunto_title] = assunto_id

        with open(self.file_path, 'w') as json_file:
            json.dump(data_container, json_file, indent=4)


if __name__ == '__main__':
    TableExtract().table_creator()
