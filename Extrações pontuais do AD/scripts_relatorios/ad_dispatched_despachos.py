import copy
import logging  # Debug
import warnings  # silenciar o aviso de descontinuidade do pandas.append()
from su_constructor import FullAd, output_csv, remove_file, date_reader  # contrutor basico de planilhas
from su_connection import connection
import os
from datetime import datetime
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
        attributes = ['id', 'protocolo', 'processo', 'assunto', 'despacho', 'data_publicacao',
                      'documento_sei', 'coord_despacho', 'documento', 'cat_uso', 'data_extracao']

        data_container = {i: None for i in attributes}

        data_line = []

        dispatched = self.get_dispatched_depachos()

        if not dispatched:
            return data_line

        # DATA CONTAINER
        data_container['id'] = self.get_id()
        data_container['protocolo'] = self.get_ad()
        data_container['processo'] = self.get_sei()[0]
        data_container['assunto'] = self.get_requerimento()
        data_container['cat_uso'] = self.get_subcategoria()
        data_container['data_extracao'] = self.TODAY

        for i in dispatched:
            data_container['documento_sei'] = i.get('numDocumento')
            data_container['data_publicacao'] = date_reader(i.get('datPublicacao'))
            data_container['despacho'] = i.get('txtTipoDocumento')
            data_container['coord_despacho'] = self.get_coord_by_publi(data_container['data_publicacao'])
            if data_container['despacho'].lower() == 'despacho deferido' and data_container['data_publicacao']:
                data_container['documento'] = self.get_ad()

            data_line.append(copy.deepcopy(data_container))

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
        file_path = f'{dir_raw_data}/ad_dispatched_despachos.csv'

        remove_file(file_path)

        cursor = self.collection.find(
            {
                # '_id': ObjectId('5f80e88ca72d15000770838e'),
                'sei.dispatchedDocuments': {'$exists': True},
            },
            {
                'nP': 1,
                'timeline': 1,
                'last_version': 1,
                'sei.created_at_iso': 1,
                'config_metadata.title': 1,
                'sei.dispatchedDocuments': 1,
                'sei.txtCodigoProcedimentoFormatado': 1,
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
