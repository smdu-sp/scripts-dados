import copy
import logging  # Debug
import warnings  # silenciar o aviso de descontinuidade do pandas.append()
from su_constructor import FullAd, output_csv, remove_file  # contrutor basico de planilhas
from su_connection import connection
import os
from bson.objectid import ObjectId  # Debug

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
        attributes = ['n_processo', 'assunto', 'despacho', 'data_despacho', 'coord_despacho', 'quem_despachou',
                      'data_extracao']

        data_container = {i: None for i in attributes}

        data_line = []

        despachos = self.get_def_indef()

        if not despachos:
            return data_line

        # DATA CONTAINER
        # data_container['id'] = self.get_id()
        data_container['n_processo'] = self.get_sei()[0]
        data_container['assunto'] = self.get_requerimento()
        data_container['data_extracao'] = self.TODAY
        for i in despachos:
            data_container['despacho'] = self.find_value('action', i)
            data_container['data_despacho'] = self.find_value('date', i)
            data_container['coord_despacho'] = self.find_value('sector', i, 'from')
            data_container['quem_despachou'] = self.find_value('name', i, 'from')

            data_line.append(copy.deepcopy(data_container))

        return data_line

    def table_creator(self):
        """Itera sobre os dados e salva o resultado em arquivo csv

        :return: <void>
        """
        # Absolute path para o diretório atual
        dir_atual = os.path.abspath(os.path.dirname(__file__))
        # Absolute path para o diretório irmão onde os arquivos serão criados
        # dir_raw_data = os.path.abspath(os.path.join(dir_atual, '..', 'arquivos_extracao'))
        dir_raw_data = os.path.abspath(os.path.join(dir_atual, '..', '..', 'relatorio_unificado', 'dat_raw'))
        logging.info(f'Extraindo documentos para {dir_raw_data}')

        # Apagando planilha ANTIGA, se houver
        file_path = f'{dir_raw_data}/ad_despachos_raw.csv'

        remove_file(file_path)

        cursor = self.collection.find(
            {
                # '_id': ObjectId('5f7b90fb8489f50008c684e8'),
                'timeline': {'$exists': True},
                'sei': {'$exists': True}
            },
            {
                'nP': 1,
                'timeline': 1,
                'config_metadata.title': 1,
                'sei.dispatchedDocuments': 1,
                'sei.txtCodigoProcedimentoFormatado': 1
            }
        ).batch_size(200)

        for n, item in enumerate(cursor):
            logging.info(f'{n} > {item.get("_id")}')

            self.data = item
            data_line = self.tabela()
            for i in data_line:
                output_csv(i, file_path)


if __name__ == '__main__':
    TableExtract().table_creator()
