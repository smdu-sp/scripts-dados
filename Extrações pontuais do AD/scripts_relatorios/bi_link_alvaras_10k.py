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


    @staticmethod
    def dispatched_sorted(dispatched):

        def extrair_timestamp(obj):
            return obj.get('datPublicacao')

        ord_dispatched = sorted(dispatched, key=extrair_timestamp)
        return ord_dispatched


    @staticmethod
    def is_ednova(assunto):
        return 'nova' in assunto.lower()

    @staticmethod
    def is_resid(uso):
        usos_resid = 'HIS', 'EHIS', 'HMP', 'HIS1', 'R2h', 'R2v', 'R1'
        for i in uso.split(','):
            if i.strip() in usos_resid:
                return True
        else:
            return False

    @staticmethod
    def is_10k(area):
        return area >= 10000 or area == 0

    @staticmethod
    def is_2022(publi):
        publi_date = datetime.strptime(publi, '%d/%m/%Y')
        limit = datetime(2023, 1, 1)
        return publi_date < limit


    def tabela(self):
        # Criando atributos (colunas) e atribuindo a estes o valor None (nulo)
        # Nomes fora do pradrão para compatibilizar com a extração da prodam
        attributes = ['nº do Processo', 'Código Assunto', 'Código Aditivo', 'Assunto', 'Interessados',
                      'Categoria de Uso', 'Área total da construção', 'Status do despacho',
                      'Data de publicação do Despacho', 'nº do Alvará', 'Data de Emissão do Alvará',
                      'id', 'cod_valid', 'is_resid', 'is_ednova', 'is_10k', 'is_2022', 'template', 'link']

        data_container = {i: None for i in attributes}

        data_line = []

        templates = self.get_templates()
        dispatched = self.get_dispatched_depachos()
        dispatched = [i for i in dispatched if 'despacho' in i['txtTipoDocumento'].lower()]
        dispatched = self.dispatched_sorted(dispatched)

        if not templates:
            return data_line

        if not dispatched:
            return data_line

        ajuste_dia = 24 * 60 * 60 * 1000
        # DATA CONTAINER
        data_container['nº do Processo'] = self.get_sei()[0]
        data_container['Assunto'] = self.get_requerimento()
        data_container['Interessados'] = self.get_proprietario()
        data_container['Categoria de Uso'] = self.get_subcategoria()
        data_container['Área total da construção'] = round(self.get_construida_total() or 0, 2)
        data_container['Status do despacho'] = dispatched[-1]['txtTipoDocumento']
        data_container['Data de publicação do Despacho'] = date_reader(str(int(dispatched[-1].get('datPublicacao')) + ajuste_dia))
        data_container['nº do Alvará'] = self.get_ad() if ('despacho deferido' in
                                                           data_container['Status do despacho'].lower() and
                                                           data_container['Data de publicação do Despacho']) else None

        data_container['Data de Emissão do Alvará'] = data_container['Data de publicação do Despacho'] if (
            data_container['nº do Alvará']) else None

        # Alvará
        data_container['id'] = self.get_id()
        data_container['is_resid'] = self.is_resid(data_container['Categoria de Uso'])
        data_container['is_ednova'] = self.is_ednova(data_container['Assunto'])
        data_container['is_10k'] = self.is_10k(data_container['Área total da construção'])
        data_container['is_2022'] = self.is_2022(data_container['Data de publicação do Despacho'])
        data_container['cod_valid'] = self.get_codvalid()

        for i in templates:
            data_container['template'] = i

            string_alv = 'https://api.producao-sp.portaldolicenciamentosp.com.br/events/regrasPdf/print/{0}?template={1}&function=processComplete&type=url&validLink=https://www.portaldolicenciamentosp.com.br/consulta/process/view/saopaulosp/{2}/{3}&title={4}&devolverDados=false'
            data_container['link'] = string_alv.format(data_container['id'], data_container['template'],
                                                       data_container['nº do Alvará'], data_container['cod_valid'],
                                                       'Alvará')

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

        cursor = self.collection.find(
            {
                # '_id': ObjectId('5fa412ed999f470008a675b0'),
                'timeline': {'$exists': True},
                'sei.dispatchedDocuments': {'$exists': True},
                'config_metadata.templates': {'$exists': True}
            },
            {
                'nP': 1,
                'timeline': 1,
                'last_version': 1,
                'cod_valid': 1,
                'config_metadata.title': 1,
                'config_metadata.templates': 1,
                'sei.dispatchedDocuments': 1,
                'sei.txtCodigoProcedimentoFormatado': 1,
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
