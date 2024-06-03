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
        # Nomes fora do pradrão para compatibilizar com a extração da prodam
        attributes = ['id', 'np', 'cod_valid', 'template', 'text_button', 'link']

        data_container = {i: None for i in attributes}

        data_line = []

        templates = self.get_templates()

        if not templates:
            return data_line

        ajuste_dia = 24 * 60 * 60 * 1000
        # DATA CONTAINER
        data_container['id'] = self.get_id()
        data_container['np'] = self.get_ad()
        data_container['cod_valid'] = self.get_codvalid()

        for i in templates:
            data_container['template'] = i[0]
            data_container['text_button'] = i[1]

            string_alv = 'https://api.producao-sp.portaldolicenciamentosp.com.br/events/regrasPdf/print/{0}?template={1}&function=processComplete&type=url&validLink=https://www.portaldolicenciamentosp.com.br/consulta/process/view/saopaulosp/{2}/{3}&title={4}&devolverDados=false'
            data_container['link'] = string_alv.format(data_container['id'], data_container['template'],
                                                       data_container['np'], data_container['cod_valid'],
                                                       data_container['text_button'])

            data_line.append(copy.deepcopy(data_container))

        return data_line

    def table_creator(self):
        """Itera sobre os dados e salva o resultado em arquivo csv

        :return: <void>
        """
        # Absolute path para o diretório atual
        dir_atual = os.path.abspath(os.path.dirname(__file__))
        # Absolute path para o diretório irmão onde os arquivos serão criados
        dir_raw_data = os.path.abspath(os.path.join(dir_atual, '..', 'arquivos_extracao', 'alvara_download'))
        logging.info(f'Extraindo documentos para {dir_raw_data}')

        file_path = f'{dir_raw_data}/link_alvaras.csv'
        # Apagando planilha ANTIGA, se houver
        remove_file(file_path)

        ids_list = [
            ObjectId('6227c249dac310000966b457'),
            ObjectId('62559c95757f6600092ef71e'),
            ObjectId('629e3128c64d3700093d3d01'),
            ObjectId('65257ac76e52cb000854d180'),
            ObjectId('63162f62d81f190009776c73'),
            ObjectId('638f5345d6ef4f0008ed619f'),
            ObjectId('620acd9d3c44390009c77892'),
            ObjectId('6463d840c68a3300083794f9'),
            ObjectId('63d97b3eee07460008b71ae3'),
            ObjectId('63dbcd8e72bd4f00082bc833'),
            ObjectId('63dbe31f6f2ca4000844adfe'),
            ObjectId('64887c61f8565a00081fb1e3'),
            ObjectId('656dcbd946eb190008789e24'),
            ObjectId('6050e059db0d7d00083da351'),
            ObjectId('613b7257533e41000781730b'),
            ObjectId('629f8b89f4517b0009600912'),
            ObjectId('62e2e3b81181fe00062ac9f4'),
            ObjectId('637531be0da10700083bd2e3'),
            ObjectId('6009ddffea70b60008c96bc6'),
            ObjectId('6449752d9ddded000831201d'),
            ObjectId('62015c92dd4bc70009ba1638'),
            ObjectId('64f0e5efa387df00089261e2'),
            ObjectId('639892ee314e670008c616ba'),
            ObjectId('6495f9c16ae85800081c5107'),
            ObjectId('656624bab7c2760008c3111e'),
            ObjectId('604ac355b6e822000844f43a'),
            ObjectId('63a44dd7396e6e000853ab30'),
            ObjectId('62f2696e40f6c6000913fb98'),
            ObjectId('64ac547d3601280008967193'),
            ObjectId('64ef7dd3f05c4800086eea8f'),
            ObjectId('65cf9847a8e7950008f7f431'),
            ObjectId('627ad7b49f2fd70009704d76'),
            ObjectId('644ad38d7c3ae800083c63b3'),
            ObjectId('65fb2772a36018000844129d'),
            ObjectId('634eb234ddf010000995c393'),
            ObjectId('60fb23b58eb08c00087deb08'),
            ObjectId('628fb6a65f70b300092ad7bd'),
            ObjectId('642b074dd88cb6000862fa41'),
            ObjectId('6537fe6897045900084a25cc'),
            ObjectId('61390ae3c9697300095a0e5d'),
            ObjectId('636e702b4add2e0008823969'),
            ObjectId('612d51378f763f000a04a4ff'),
            ObjectId('65562cdff234af0008ac0e16'),
            ObjectId('655f540d6ddd5c000832762d'),
            ObjectId('65b411a89c67d50008cf0542'),
            ObjectId('62699c26c222ae0009e8df8a'),
            ObjectId('65526bce0cbe1500083abba4'),
            ObjectId('639b96192e603600083fc883'),
            ObjectId('64e66c881d984e0008997146'),
            ObjectId('65ef130b0a967d0008461ef1'),
            ObjectId('627edb13d903a90009af48b2'),
            ObjectId('6160ae47c40dfc0008a11580'),
            ObjectId('64c29cb91555e10008f329ca'),
            ObjectId('65f20253526baa0008ddd36d'),
            ObjectId('637e4376c8d4330008c68595'),
            ObjectId('64f0c7054086560008ef2039'),
            ObjectId('65414eb7f6d47b0008266dbf'),
            ObjectId('602eb6c35e009000082dd7b4'),
            ObjectId('601dcc1075d45d0009fcb1f5'),
            ObjectId('6361798e30dfc0000988834c'),
            ObjectId('635ae08c2d81df00099dfb45'),
            ObjectId('60cbb35669ab790009712577'),
            ObjectId('6113f5d9be3db50009c7949a'),
            ObjectId('620c074bd342320009cbe093'),
            ObjectId('636d5f8d2791df00081c2474'),
            ObjectId('6385062effce1a0008c295bc'),
            ObjectId('64550c9a8f6cd00008b4b621'),
            ObjectId('65a930930cb7f600086c85e1'),
            ObjectId('60ca69f18fe7f30008f52c54'),
            ObjectId('60ca116ed8d6040009f5adb3'),
            ObjectId('60bfb1eb88fe480008faf3cf'),
            ObjectId('60c7aa7c5ca1980008a90ca3'),
            ObjectId('60ca443a97ef9a000991acff'),
            ObjectId('60819bafc8b71b000884de1e'),
            ObjectId('60ca5cfed0c09c00099b8a4c'),
            ObjectId('60c7ba085dc2d90009fed231'),
            ObjectId('60e5dac749dc5f00085ba90f'),
            ObjectId('60915e0594573600081321e6'),
            ObjectId('6081e1233d8ba700098ac9be'),
            ObjectId('60bfc05be1d4a10008b1fd7f'),
            ObjectId('60c22320d6bd47000934908a'),
            ObjectId('60e5e331695fb3000894ed4a'),
            ObjectId('60cba41358359a000711f330'),
            ObjectId('60c79cafa500f30009f0ab77')
        ]

        np_list = [
            "6697-21-SP-ALV",
            "8514-21-SP-AUT",
            "14747-22-SP-CER",
            "23763-22-SP-ALV",
            "28775-23-SP-AUT",
            "34716-23-SP-ALV",
            "4881-21-SP-CER",
            "28906-23-SP-ALV",
            "11239-22-SP-ALV",
        ]

        cursor = self.collection.find(
            {
                # 'nP': {'$in': np_list}
                '_id': {'$in': ids_list}
            },
            {
                'nP': 1,
                'cod_valid': 1,
                'config_metadata.templates': 1,
            }
        ).batch_size(100)

        for n, item in enumerate(cursor):
            logging.info(f'{n} > {item.get("_id")}')

            self.data = item
            data_line = self.tabela()
            for i in data_line:
                output_csv(i, file_path)


if __name__ == '__main__':
    TableExtract().table_creator()
