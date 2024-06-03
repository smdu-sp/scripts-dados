import copy
import logging  # Debug
import warnings  # silenciar o aviso de descontinuidade do pandas.append()
from su_constructor import FullAd, output_csv, remove_file  # contrutor basico de planilhas
from su_connection import connection
import os
from bson.objectid import ObjectId

warnings.simplefilter(action='ignore', category=FutureWarning)  # Silenciando os warning de append do pandas
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TableExtract(FullAd):
    """Cria a planilha principal completa. Herda da classe FullAd que faz o processamento dos dados em json
    extraídos do sistema"""

    def __init__(self, env='prod'):
        super().__init__()

        self.collection = connection(env)
        self.file_path = ''

    def tabela(self):

        # Criando atributos (colunas) e atribuindo a estes o valor None (nulo)
        attributes = ['id', 'n_processo', 'assunto', 'setor_atual', 'status', 'sistema']

        data_container = {i: None for i in attributes}

        data_line = []

        # DATA CONTAINER
        data_container['id'] = self.get_id()
        data_container['n_processo'] = self.get_sei()[0]
        data_container['assunto'] = self.get_requerimento()
        data_container['setor_atual'] = self.get_coord_entradas(self.div_all_names, 'atual')
        data_container['status'] = self.get_status()
        data_container['sistema'] = 'Aprova Digital'

        data_line.append(data_container)
        return data_line

    def table_creator(self):
        """Itera sobre os dados e salva o resultado em arquivo csv

        :return: <void>
        """
        # Absolute path para o diretório atual
        dir_atual = os.path.abspath(os.path.dirname(__file__))
        # Absolute path para o diretório irmão onde os arquivos serão criados
        dir_raw_data = os.path.abspath(os.path.join(dir_atual, '../..', 'arquivos_extracao'))
        logging.info(f'Extraindo documentos para {dir_raw_data}')

        # Apagando planilha ANTIGA, se houver
        self.file_path = f'{dir_raw_data}/bi_setores.csv'

        remove_file(self.file_path)

        cursor = self.collection.find(
            {
                'timeline': {'$exists': True},
                'sei': {'$exists': True}
            },
            {
                'sei.txtCodigoProcedimentoFormatado': 1,
                'config_metadata.title': 1,
                'timeline': 1,
                'last_version': 1
            }
        ).batch_size(200)

        for n, item in enumerate(cursor):
            logging.info(f'{n} > {item.get("_id")}')

            self.data = item
            data_line = self.tabela()
            for i in data_line:
                output_csv(i, self.file_path)


if __name__ == '__main__':
    TableExtract().table_creator()
