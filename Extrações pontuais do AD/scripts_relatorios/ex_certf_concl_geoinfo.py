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
        attributes = ['n_processo', 'assunto', 'status', 'data_deferimento', 'tipo_de_localizacao', 'localizacao',
                      'endereco', 'cep', 'categoria_uso', 'numero_documento', 'certf_conclusao_tipo',
                      'area_objeto_certf_concl']

        data_container = {i: None for i in attributes}

        data_line = []

        if self.get_def_indef():
            if self.get_status() == 'deferido':

                loc = self.get_attrb_localizacao(flat=True)
                # DATA CONTAINER
                # data_container['id'] = self.get_id()
                data_container['n_processo'] = self.get_sei()[0]
                data_container['assunto'] = self.get_requerimento()
                data_container['status'] = self.get_status()
                data_container['data_deferimento'] = self.find_value('date', self.get_def_indef()[-1])
                data_container['tipo_de_localizacao'] = loc['tipo_id']
                data_container['localizacao'] = loc['sql']
                data_container['endereco'] = loc['endereco']
                data_container['cep'] = loc['cep']
                data_container['categoria_uso'] = self.get_grupo_atividade()
                data_container['numero_documento'] = self.get_ad()
                data_container['certf_conclusao_tipo'] = self.get_certf_tipo()
                data_container['area_objeto_certf_concl'] = self.get_area_objeto()

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
        file_path = f'{dir_raw_data}/ad_certificado_conclusao.csv'
        remove_file(file_path)

        assuntos = [
            'Certificado de Conclusão'
        ]

        cursor = self.collection.find(
            {
                # '_id': ObjectId('653bc991459c890008e87fcc'),
                'timeline': {'$exists': True},
                'config_metadata.title': {'$in': assuntos}
            },
            {
                "nP": 1,
                "sei.txtCodigoProcedimentoFormatado": 1,
                "config_metadata.title": 1,
                "timeline": 1,
                "last_version": 1}
            ).batch_size(100)

        for n, item in enumerate(cursor):
            logging.info(f'{n} > {item.get("_id")}')

            self.data = item
            data_line = self.tabela()
            for i in data_line:
                output_csv(i, file_path)


if __name__ == '__main__':
    TableExtract().table_creator()
