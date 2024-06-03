import json
import logging  # Debug

from su_constructor import remove_file
from su_connection import connection
import os
import re

class TableExtract():

    def __init__(self, env='prod'):
        super().__init__()

        self.collection = connection(env, 'setor')
        self.file_path = ''

        self.corrected_dict = {
            'pesehab_saopaulosp': ['PARHIS'],
            'pesehabfim_saopaulosp': ['PARHIS'],
            'pesalaapoioparhis_saopaulosp': ['PARHIS'],
            'pecap_saopaulosp': ['CAP'],
            'pecapord_saopaulosp': ['CAP'],
            'pecancelado_saopaulosp': ['CAP']
        }

    def table_creator(self):
        """Itera sobre os dados e salva o resultado em arquivo csv

        :return: <void>
        """
        # Absolute path para o diretório atual
        dir_atual = os.path.abspath(os.path.dirname(__file__))

        # Apagando arquivo ANTIGO, se houver
        self.file_path = f'{dir_atual}/j_sector_names.json'
        remove_file(self.file_path)

        cursor = self.collection.find({}, {'nome': 1, 'tag': 1})

        data_container = {}
        for n, item in enumerate(cursor):
            logging.info(f'{n} > {item.get("_id")}')
            nome_raw = item['nome']
            tag = item['tag']
            re_pattern = r'\b[A-Z]{2,}\b'  # 2 letras maiusculas consecutivas
            if tag in self.corrected_dict.keys():
                nome = self.corrected_dict[tag]
            else:
                nome = re.findall(re_pattern, nome_raw)
            nome = nome[0] if nome else ''
            data_container[tag] = nome

        with open('j_sector_names.json', 'w') as json_file:
            json.dump(data_container, json_file, indent=4)


if __name__ == '__main__':
    TableExtract().table_creator()
