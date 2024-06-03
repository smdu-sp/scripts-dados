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

    def tabela(self):
        # Criando atributos (colunas) e atribuindo a estes o valor None (nulo)
        attributes = ['n_processo', 'data_comuniquese', 'coord_comuniquese', 'quem_comunicou']

        data_container = {i: None for i in attributes}

        data_line = []

        comuniqueses = self.get_comuniqueses()

        if not comuniqueses:
            return data_line

        # DATA CONTAINER
        data_container['n_processo'] = self.get_sei()[0]

        for i in comuniqueses:
            data_container['data_comuniquese'] = self.find_value('date', i)
            data_container['coord_comuniquese'] = self.find_value('sector', i, 'from')
            data_container['quem_comunicou'] = self.find_value('name', i, 'from')

            data_line.append(copy.deepcopy(data_container))

        return data_line

    def table_creator(self):
        """Itera sobre os dados e salva o resultado em arquivo csv

        :return: <void>
        """
        # Absolute path para o diretório atual
        dir_atual = os.path.abspath(os.path.dirname(__file__))
        # Absolute path para o diretório irmão onde os arquivos serão criados
        dir_raw_data = os.path.abspath(os.path.join(dir_atual, '..', '..', 'relatorio_unificado', 'dat_raw'))
        logging.info(f'Extraindo documentos para {dir_raw_data}')

        # Apagando planilha ANTIGA, se houver
        file_path = f'{dir_raw_data}/ad_comuniqueses_raw.csv'

        remove_file(file_path)

        cursor = self.collection.find(
            {
                'timeline': {'$exists': True},
                'sei': {'$exists': True}
            },
            {
                'timeline': 1,
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
