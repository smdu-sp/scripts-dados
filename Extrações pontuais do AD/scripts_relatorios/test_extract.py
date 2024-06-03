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
        attributes = ['id', 'protocolo', 'processo', 'data_autuacao', 'assunto', 'situacao', 'sql', 'incra',
                      'area_publica', 'proprietario', 'endereco', 'subprefeitura', 'distrito', 'categoria',
                      'subcategoria', 'area_total_objeto', 'blocos', 'pavimentos', 'unidades', 'sist_origem',
                      'data_extracao']

        data_container = {i: None for i in attributes}

        data_line = []

        loc = self.get_attrb_localizacao(flat=True)

        # DATA CONTAINER
        # Processo
        data_container['id'] = self.get_id()
        data_container['protocolo'] = self.get_ad()
        data_container['processo'] = self.get_sei()[0]
        data_container['data_autuacao'] = self.get_sei()[1]
        data_container['assunto'] = self.get_requerimento()
        data_container['situacao'] = self.get_status()
        # Localização
        data_container['sql'] = loc['sql']
        data_container['incra'] = loc['incra']
        data_container['area_publica'] = loc['area_p']
        data_container['endereco'] = loc['endereco']
        data_container['subprefeitura'] = loc['subprefeitura']
        data_container['distrito'] = loc['distrito']
        # Envolvidos
        data_container['proprietario'] = None
        # obra
        data_container['categoria'] = None  # self.get_tipo_uso()
        data_container['subcategoria'] = None  # self.get_subcategoria()
        data_container['area_total_objeto'] = None
        data_container['blocos'] = None
        data_container['pavimentos'] = None
        data_container['unidades'] = None

        data_container['sistema_origem'] = 'Aprova Digital'
        data_container['data_extracao'] = self.TODAY

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
        file_path = f'{dir_raw_data}/bi_balanco_processo_raw.csv'

        remove_file(file_path)

        cursor = self.collection.find(
            {
                '_id': ObjectId('62cf29bd1f29480009bc9cf1'),
                'timeline': {'$exists': True},
                'sei': {'$exists': True}
            },
            {
                'nP': 1,
                'sei.created_at_iso': 1,
                'sei.txtCodigoProcedimentoFormatado': 1,
                'config_metadata.title': 1,
                'last_version': 1
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
