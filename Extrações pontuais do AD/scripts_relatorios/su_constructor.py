import datetime  # Para facilitar a leitura de strings que representam objetos datetime
import logging  # Para geral logs (debug e avisos)
import json
import os
import csv  # Salvar os dados

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


###########################
#   Funções auxiliares    #
###########################
def output_csv(dict_data, file_path='output.csv'):
    """Responsável por salvar os dados em um arquivo .csv.
    :param file_path: <str> nome do arquivo
    :param dict_data: <dict> Dicionário que contém todos os atributos de interesse para o processo
    :return: <void>
    """
    try:
        if not os.path.exists(file_path):
            # Gerando o arquivo e o cabeçalho caso o arquivo não exista (1a iteração)
            with open(file_path, 'w', newline='') as output_file:
                dictwriter = csv.DictWriter(output_file, dict_data.keys(), delimiter=';')
                dictwriter.writeheader()
                dictwriter.writerow(dict_data)
        else:
            # Outras iterações
            with open(file_path, 'a', newline='') as output_file:
                dictwriter = csv.DictWriter(output_file, dict_data.keys(), delimiter=';')
                dictwriter.writerow(dict_data)

    except UnicodeEncodeError:
        logging.debug(dict_data.get('ID'))
    except PermissionError:
        logging.debug('Por favor feche todos os arquivos usados para escrever os dados')


def readable_date(time_string):
    """método que lê o a estampa de data e hora passadas e traduz para valores mais legíveis e compatíveis com o resto da planilha

    :param time_string: <str> string que representa um valor de data/hora, sem formatação
    :return: <str> a data e hora formatados
    """
    if time_string:
        if len(time_string) == 24:
            time_obj = datetime.datetime.strptime(time_string[:19 - len(time_string)],
                                                  '%Y-%m-%dT%H:%M:%S')  # Criando um obj datetime (lendo um string)

        elif len(time_string) == 26:
            time_obj = datetime.datetime.strptime(time_string[:19 - len(time_string)],
                                                  '%Y-%m-%d %H:%M:%S')  # Criando um obj datetime (lendo um string)

        elif len(time_string) == 19:
            time_obj = datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')

        else:
            return None

        delta_time = datetime.timedelta(hours=3)
        final_time = time_obj - delta_time
        return final_time.strftime('%d/%m/%Y %H:%M:%S')  # Retornando na formatação desejada.
    return None


def date_reader(date):

    date = int(date)
    date_in_seconds = (int(date / 1000))
    dt_object = datetime.datetime.fromtimestamp(date_in_seconds)

    return dt_object.strftime('%d/%m/%Y')


def remove_file(*file_path):

    for file in file_path:
        if os.path.exists(file):
            os.remove(file)


class FullAd:

    def __init__(self, data=None, tec_sectors=True):
        """ Inicia o objeto a partir de um conjunto de dados do AD, em que todos os métodos atuarão sobre este conjunto

        :param data: <dict> dados do sistema web em json para dict
        :return: <void>
        """
        # Variável global que pode ser usada para todos os métodos da classe
        self.data = data

        self.TODAY = datetime.datetime.now().strftime('%Y.%m.%d')

        json_path = os.path.dirname(os.path.realpath(__file__))

        # Nomes das divisões e suas correnpondências
        with open(os.path.join(json_path, 'j_bi_names.json'), 'r') as json_file:
            self.div_bi_names = json.load(json_file)

        with open(os.path.join(json_path, 'j_sector_names.json'), 'r') as json_file:
            self.div_all_names = json.load(json_file)

        # Trabalhando apenas com setores de análise

        # Nome das divisões na hierarquia e a coordenadoria correpondente
        with open(os.path.join(json_path, 'j_coord_div_tree.json'), 'r') as json_file:
            self.coord_div_tree = json.load(json_file)

    def find_value(self, key, dict_data, tip=None):
        """ Método para a leitura dos dados, itera recursivamente sobre um dicionário procurando o valor para a chave indicada
        podendo contar com uma chave intermediária (dica) para focar um apenas um dos braços do dicionário.

        :param key: <str> o valor a ser procurado
        :param dict_data: <dict>/<list> dicionário ou lista em que serão buscadas as informações
        :param tip: <str> o valor intermediário a ser procurado
        :return: <str> a data e hora formatados
        """
        # Procurar o braço que contenha a dica primeiro
        if tip:
            dict_data = self.find_value(tip, dict_data)

        # Caso encontre uma lista retornar todos os valores encontrados para a chave (em forma de lista)
        if isinstance(dict_data, list):
            value_list = [self.find_value(key, i) for i in dict_data if self.find_value(key, i)]
            if value_list:
                return value_list

        # Caso a iteração esteja em um dict, procurar o valor, se houver, retornar
        if isinstance(dict_data, dict):
            value = dict_data.get(key, None)
            if value:
                return value
            # Caso não encontr o valor iterar pelo dict e repetir o processo usando cada valor da iteração
            else:
                for i in dict_data:
                    if isinstance(dict_data, dict) or isinstance(dict_data, list):
                        value = self.find_value(key, dict_data[i])
                        if value:
                            return value

    ###########################
    #        PROCESSO         #
    ###########################
    def get_id(self):

        return str(self.data.get('_id'))

    def get_link(self):

        return f'https://portaldolicenciamentosp.com.br/processo/{self.get_id()}'

    def get_ad(self):

        return self.data.get('nP')

    def get_sei(self):

        sei_data = self.data.get('sei')
        sei = sei_data.get('txtCodigoProcedimentoFormatado') if sei_data else None
        autuado = readable_date(str(sei_data.get('created_at_iso'))) if sei_data else None

        return sei, autuado

    def get_requerimento(self):

        return self.data.get('config_metadata').get('title')

    def get_coord_entradas(self, base, momento=''):
        entradas = []
        for i in self.data.get('timeline'):
            date = i.get('date')
            user_id = i.get('to').get('userId') if i.get('to') else None
            div_name = base.get(user_id)
            sector = self.get_coord_from_sector(div_name)
            if user_id in base:
                entradas.append((sector, date))

        if momento == 'atual' and entradas:
            return entradas[-1][0]
        elif momento == 'autuacao' and entradas:
            return entradas[0][0]
        else:
            return entradas

    def get_status(self):
        # Retorna o status atual do processo baseado em operadores lógicos
        final = self.data['last_version'].get('finalizar')
        indef = self.data['last_version'].get('indeferido')
        desist = self.data['last_version'].get('desistir')

        if final and not indef and not desist:
            return 'deferido'

        if final and indef and not desist:
            return 'indeferido e encerrado'

        if not final and indef and not desist:
            return 'indeferido'

        if not final and not indef and not desist:
            return 'em análise'

        if final and desist:
            return 'desistido'

        return 'desconhecido'

    def get_situacao(self):

        return self.data.get('timeline')[-1].get('data').get('action')

    def get_data_situacao(self):

        return self.data.get('timeline')[-1].get('date')

    ###########################
    #        ENVOLVIDOS       #
    ###########################
    def get_active_user(self):

        return self.find_value('activeUser', self.data)

    def get_proprietario(self):
        """ Retorna o(s) nome(s) do(s) proprietário(s) do terreno.

        :return: <str>
        """
        proprietario = self.find_value('nome-proprietario', self.data['last_version'].get('proprietario'))

        if proprietario:
            return ', '.join(proprietario)
        else:
            return None

        # Método antigo
        #propriet = self.find_value('nome-proprietario', self.data['last_version'])
        #if propriet:
        #    return ', '.join(list(dict.fromkeys(propriet)))

    def get_resp_tec(self):
        """ Retorna o(s) nome(s) do(s) responsavel(is) técnico(s) do projeto.

        :return: <str>
        """
        tips = ['responsaveltecnico', 'responsavel_tecnico', 'responsavel_projeto', 'responsavel_execucao']
        keys = ['nome_execucao', 'nome_projeto', 'nomeProfissional', 'nome_profissional']

        for tip in tips:
            for key in keys:
                resp_tec = self.find_value(key, self.data['last_version'], tip)
                if resp_tec:
                    return ', '.join(list(dict.fromkeys(resp_tec)))

    def get_autor_proj(self):
        """ Retorna o(s) nome(s) do(s) autor(es) técnico(s) do projeto.

        :return: <str>
        """
        autor = self.find_value('nome_responsavel', self.data['last_version'], 'autor_projeto')
        if autor:
            return ', '.join(list(dict.fromkeys(autor)))

    def get_cpf_cnpj_requerente(self):

        self.data.get('last_version')

    def get_cpf_cnpj_proprietario(self):

        self.data.get('last_version')

    ###########################
    #   LOCALIZACAO e USOS    #
    ###########################
    def get_attrb_localizacao(self, flat=False):

        # Regras
        last_version = self.data.get('last_version')
        end_list_a = last_version.get('endereco_obra')
        end_list_b = last_version.get('endereco-obra')
        dados_terreno = last_version.get('dadosterreno')
        terreno = last_version.get('terreno')
        integracao = last_version.get('integracao_localizacaoimovel')

        # Atributos buscados
        attrb = ['endereco', 'logradouro', 'numero', 'complemento', 'bairro', 'cep', 'sql', 'incra', 'area_p', 'tipo_id',
                 'codlog', 'zona_uso', 'subprefeitura', 'distrito']
        dt = {i: None for i in attrb}

        # REGRA last_version direto 5f87932507d83e00089dc55d
        if last_version.get('logradouro_rua'):
            dt['logradouro'] = str(last_version.get('logradouro_rua'))
            dt['numero'] = str(last_version.get('numero-predial'))
            dt['bairro'] = str(last_version.get('id-bairro'))
            dt['complemento'] = str(last_version.get('complemento_imovel'))
            dt['cep'] = str(last_version.get('endereco-cep'))
            dt['sql'] = str(last_version.get('campo_sql'))
            dt['incra'] = str(last_version.get('cadastro_rural'))
            tipo_id = str(last_version.get('identicacao_imovel'))
            dt['tipo_id'] = str(last_version.get('tipo_identificacao'))
            dt['area_p'] = tipo_id if tipo_id == 'Área Pública' else None
            dt['codlog'] = str(last_version.get('codlog'))
            dt['zona_uso'] = [str(i.get('lista_zona')) for i in last_version.get('zonas_uso')]
            dt['subprefeitura'] = str(last_version.get('subprefeitura'))
            dt['distrito'] = str(last_version.get('distrito'))

            dt['endereco'] = ', '.join((dt['logradouro'], dt['numero'], dt['bairro']))

        # regra last_version direto variacao 626aef1d22d0dc000977fd3d
        if last_version.get('nome_logradouro'):
            dt['logradouro'] = str(last_version.get('nome_logradouro'))
            dt['numero'] = str(last_version.get('iptu_numeracao'))
            dt['bairro'] = str(last_version.get('iptu_bairro'))
            dt['complemento'] = str(last_version.get('complemento_imovel'))
            dt['cep'] = str(last_version.get('iptu_cep'))
            dt['sql'] = self.find_value('input', last_version.get('campo_sql'))
            dt['incra'] = str(last_version.get('cadastro_rural'))
            tipo_id = str(last_version.get('tipo_identificacao'))
            dt['tipo_id'] = str(last_version.get('tipo_identificacao'))
            dt['area_p'] = tipo_id if tipo_id == 'Área Pública' else None
            dt['codlog'] = str(last_version.get('codlog'))
            dt['zona_uso'] = str(last_version.get('zon_sigla'))
            dt['subprefeitura'] = str(last_version.get('subprefeitura'))
            dt['distrito'] = str(last_version.get('distrito'))

            dt['endereco'] = ', '.join((dt['logradouro'], dt['numero'], dt['bairro']))

        # Regra endereco_obra (UNDERLINE) 5f4d5f67f1506500076de309
        if end_list_a:
            dt['logradouro'] = [str(i.get('logradouro_rua')) for i in end_list_a]
            dt['numero'] = str(last_version.get('numero-predial'))
            dt['bairro'] = str(last_version.get('id-bairro'))
            dt['complemento'] = str(last_version.get('complemento_imovel'))
            dt['cep'] = str(last_version.get('endereco-cep'))
            dt['sql'] = last_version.get('campo_sql')
            dt['incra'] = last_version.get('cadastro_rural')
            tipo_id = str(last_version.get('tipo_identificacao'))
            dt['tipo_id'] = str(last_version.get('tipo_identificacao'))
            dt['area_p'] = tipo_id if tipo_id == 'Área Pública' else None
            dt['codlog'] = str(last_version.get('codlog'))
            dt['zona_uso'] = str([i.get('lista_zona') for i in last_version.get('zonas_uso')])
            dt['subprefeitura'] = str(last_version.get('subprefeitura'))
            dt['distrito'] = str(last_version.get('distrito'))

            dt['endereco'] = [', '.join((i, dt['numero'], dt['bairro'])) for i in dt['logradouro']]

        # Regra endereco-obra (HIFEN) 5f88891c4bd47b0008d0530e
        if end_list_b:
            dt['logradouro'] = [str(i.get('logradouro-rua')) for i in end_list_b]
            dt['numero'] = str(last_version.get('numero-predial'))
            dt['bairro'] = str(last_version.get('id-bairro'))
            dt['complemento'] = str(last_version.get('complemento_imovel'))
            dt['cep'] = str(last_version.get('endereco-cep'))
            dt['sql'] = last_version.get('campo_sql')
            dt['incra'] = last_version.get('cadastro_rural')
            tipo_id = str(last_version.get('tipo_identificacao'))
            dt['tipo_id'] = str(last_version.get('tipo_identificacao'))
            dt['area_p'] = tipo_id if tipo_id == 'Área Pública' else None
            dt['codlog'] = str(last_version.get('codlog'))
            dt['zona_uso'] = str([i.get('lista_zona') for i in last_version.get('zonas_uso')])
            dt['subprefeitura'] = str(last_version.get('subprefeitura'))
            dt['distrito'] = str(last_version.get('distrito'))

            dt['endereco'] = [', '.join((i, dt['numero'], dt['bairro'])) for i in dt['logradouro']]

        # Regra dadosterreno 5fd3c69730753f000964f6e5
        if dados_terreno:
            dt['logradouro'] = [str(i.get('nome_logradouro')) for i in dados_terreno]
            dt['numero'] = [str(i.get('numero-predial')) for i in dados_terreno]
            dt['bairro'] = [str(i.get('id-bairro')) for i in dados_terreno if str(i.get('id-bairro')).strip()[0].isalnum()]
            dt['complemento'] = [str(i.get('complemento_imovel')) for i in dados_terreno if i.get('complemento_imovel')]
            dt['cep'] = [str(i.get('endereco-cep')) for i in dados_terreno]
            dt['sql'] = [i.get('campo_sql') for i in dados_terreno]
            dt['incra'] = [i.get('cadastro_rural') for i in dados_terreno]
            dt['area_p'] = ['Área Pública' if (i.get('tipo_identificacao') == 'Área Pública') else None for i in dados_terreno]
            dt['tipo_id'] = str(last_version.get('tipo_identificacao'))
            dt['codlog'] = [str(i.get('codlog')) for i in dados_terreno]
            dt['zona_uso'] = [str(i.get('lista_zona')) for i in dados_terreno]
            dt['subprefeitura'] = [str(i.get('subprefeitura')) for i in dados_terreno]
            dt['distrito'] = [str(i.get('distrito')) for i in dados_terreno if i.get('distrito')]
            if len(dt['logradouro']) == len(dt['numero']) == len(dt['bairro']):
                dt['endereco'] = [', '.join((i, dt['numero'][n], dt['bairro'][n])) for n, i in enumerate(dt['logradouro'])]
            else:
                dt['endereco'] = ', '.join((dt['logradouro'][0], dt['numero'][0], dt['bairro'][0])) if dt['bairro'] else None

        # regra terreno (APENAS) 5fde84b620147500089925ef
        if terreno:
            dt['logradouro'] = [str(i.get('nome_logradouro')) for i in terreno]
            dt['numero'] = [str(i.get('iptu_numeracao')) for i in terreno]
            dt['bairro'] = [str(i.get('iptu_bairro')) for i in terreno]
            dt['complemento'] = [str(i.get('complemento_imovel')) for i in terreno]
            dt['cep'] = [str(i.get('iptu_cep')) for i in terreno]
            dt['codlog'] = [str(i.get('codlog')) for i in terreno]
            dt['zona_uso'] = [str(i.get('zon_sigla')) for i in terreno]
            dt['subprefeitura'] = [str(i.get('subprefeitura')) for i in terreno]
            dt['distrito'] = [str(i.get('distrito')) for i in terreno]
            # definir tipo de identificação
            sql_values = []
            for i in terreno:
                if i.get('campo_sql') and isinstance(i['campo_sql'], dict):
                    if i['campo_sql'].get('input'):
                        sql_values.append(i['campo_sql']['input'])
                    elif isinstance(i['campo_sql'], str):
                        sql_values.append(i['campo_sql'])
                    else:
                        sql_values.append(None)

                if i.get('sql'):
                    if i['sql'].get('input'):
                        sql_values.append(i['sql']['input'])
                    elif isinstance(i['sql'], str):
                        sql_values.append(i['sql'])
                    else:
                        sql_values.append(None)

                if i.get('integracao_sql'):
                    if i['integracao_sql'].get('input'):
                        sql_values.append(i['integracao_sql']['input'])
                    elif isinstance(i['integracao_sql'], str):
                        sql_values.append(i['integracao_sql'])
                    else:
                        sql_values.append(None)

            dt['sql'] = sql_values
            dt['incra'] = [i.get('cadastro_rural') for i in terreno]
            dt['area_p'] = ['Área Pública' if (i.get('tipo_identificacao') == 'Área Pública') else None for i in terreno]
            dt['tipo_id'] = str(last_version.get('tipo_identificacao'))

            end = [(i, dt['numero'][n], dt['bairro'][n]) for n, i in enumerate(dt['logradouro'])]
            dt['endereco'] = [', '.join((i, dt['numero'][n], dt['bairro'][n])) for n, i in enumerate(dt['logradouro'])]

        # Regra integracao (estande de vendas) 606f9b0457feb300080a0e0a
        if integracao and integracao.get('data'):
            dt['endereco'] = self.find_value('end_testada_principal', integracao, 'response')
            dt['cep'] = self.find_value('cep', integracao, 'response')
            dt['codlog'] = self.find_value('codlog', integracao, 'response')
            dt['distrito'] = self.find_value('distrito', integracao, 'response')
            dt['tipo_id'] = self.find_value('tipo_identificacao', integracao, 'response')
            dt['sql'] = [i.get('identificacao_terreno') for i in integracao.get('data').get('response').get('data') if
                         i.get('tipo_identificacao') == 'SQL']

            dt['incra'] = [i.get('identificacao_terreno') for i in integracao.get('data').get('response').get('data') if
                           i.get('tipo_identificacao') == 'INCRA']

            dt['area_p'] = ['Área Pública' for i in integracao.get('data').get('response').get('data') if
                            i.get('tipo_identificacao') == 'Área Pública']

        for i in dt:
            if dt[i] == 'None':
                dt[i] = None
 
        if flat:
            for i in dt:
                if isinstance(dt[i], list):
                    clean_list = [item for item in dt[i] if item is not None]

                    dt[i] = ', '.join(clean_list)
                    dt[i] = dt[i].replace('None', ' ')

        return dt

    def get_tipo_uso(self):

        keys = ['tipo_uso', 'tipopedido_edilicio', 'categoria_pedido', 'usoatual', 'tipo_empreendimento']
        exclusion_list = [
            'Estabelecimento de ensino, desde que mantido por instituição sem fins lucrativos',
            'Templo religioso',
            'Empreendimento Habitacional de Interesse Social em ZEIS - EZEIS'
        ]
        uso = []
        for key in keys:
            found_uso = self.find_value(key, self.data['last_version'])
            # input(f'tipo_uso: {key} > {found_uso}')
            if found_uso:
                if isinstance(found_uso, list):
                    found_uso = list(map(lambda x: x + ' ', found_uso))
                    found_uso = list(map(lambda z: z[:z.find(':')], found_uso))
                    found_uso = ', '.join(found_uso)

                elif isinstance(found_uso, str):
                    found_uso = found_uso + ' '
                    found_uso = found_uso[:found_uso.find(':')]
                uso.append(found_uso)
        # input(', '.join(uso))
        return ', '.join(uso)

    def get_subcategoria(self):
        """ Retorna a categoria da edificação.

        :return: <str>
        """
        keys = ['categorianresid', 'categoriaresidencial', 'categoriaehis', 'sub_categoria', 'tipo_empreendimento']
        exclusion_list = ['Residencial (R)', 'Não Residencial (nR)', 'Comercial/Industrial']
        subcateg = []
        for key in keys:
            found_subcateg = self.find_value(key, self.data['last_version'])
            # input(f'subcateg: {key} > {found_subcateg}')
            if found_subcateg:
                if isinstance(found_subcateg, list):
                    found_subcateg = list(map(lambda x: x + ' ', found_subcateg))
                    found_subcateg = list(map(lambda z: z[:z.find(':')], found_subcateg))
                    found_subcateg = ', '.join(found_subcateg)

                elif isinstance(found_subcateg, str):
                    found_subcateg = found_subcateg + ' '
                    found_subcateg = found_subcateg[:found_subcateg.find(':')]

                if found_subcateg in exclusion_list:
                    pass
                else:
                    subcateg.append(found_subcateg)

        # input(', '.join(subcateg))
        return ', '.join(subcateg)

    def get_grupo_atividade(self):
        """ Retorna a subcategoria da edificação.

        :return: <str>
        """
        keys = ['tipoclassificacao', 'subcategorianr', 'subcategoria_rv', 'subcategoria_rh', 'subcategoria_nrtres',
                'subcategoria_nrdois', 'subcategoria_infra', 'subcategoria_infra_0', 'sub_categoriauso',
                'subcategoria_inddois',
                'subcategoria_indtres', 'subcategoria_ind', 'grupo_atividade']
        grupo_atv = []
        for key in keys:
            found_group = self.find_value(key, self.data['last_version'])
            # input(f'{key} > {found_group}')
            if found_group:
                if isinstance(found_group, list):
                    found_group = list(map(lambda x: x + ' ', found_group))
                    found_group = list(map(lambda z: z[:z.find(':')], found_group))
                    found_group = ', '.join(list(dict.fromkeys(found_group)))

                elif isinstance(found_group, str):
                    found_group = found_group + ' '
                    found_group = found_group[:found_group.find(':')]

                grupo_atv.append(found_group)

        # input(', '.join(grupo_atv))
        return ', '.join(grupo_atv)

    def normalizar_area_uso(self, string):

        tipo_keys = ['tipo_uso', 'tipopedido_edilicio', 'categoria_pedido', 'usoatual', 'tipoisento']

        cat_keys = ['categorianresid', 'categoriaresidencial', 'categoriaehis', 'sub_categoria', 'tipo_empreendimento']

        sub_keys = ['tipoclassificacao', 'subcategorianr', 'subcategoria_rv', 'subcategoria_rh', 'subcategoria_nrtres',
                    'subcategoria_nrdois', 'subcategoria_infra', 'subcategoria_infra_0', 'sub_categoriauso',
                    'subcategoria_inddois',
                    'subcategoria_indtres', 'subcategoria_ind', 'grupo_atividade']

        # normalizando o tipo de uso
        for key in tipo_keys:
            if key in string:
                string = string.replace(key, 'tipo')
        # normalizando a subcategoria de uso
        for key in cat_keys:
            if key in string:
                string = string.replace(key, 'cat')
        # normalizando os grupos de atividade
        for key in sub_keys:
            if key in string:
                string = string.replace(key, 'grp_atv')

        return string

    def get_quadro_area_uso(self):

        # Formatação dos nomes das categorias e grupos de atv
        abrev = lambda x: x[:x.find(':')] if x else None
        serializar_datetime = lambda obj: obj.isoformat() if isinstance(obj,
                                                                        datetime.datetime) else f'erro serializac type {type(obj)}'
        data_container = []
        # Trazendo os dados do 'quadro_area_uso'
        if data := self.data.get('last_version', {}).get('quadro_area_uso'):
            # Convertendo a 'data' para uma string
            data = json.dumps(data)
            # Normalizando
            data = self.normalizar_area_uso(data)
            # convertendo 'data' novamente para um dicionário
            data = json.loads(data)
            # data = ast.literal_eval(data)

            # Passando as informações para o data_container
            for area in data:
                quadro_areas = {}
                quadro_areas['tipo'] = area.get('tipo')
                quadro_areas['uni'] = area.get('unidades_uso')
                quadro_areas['subcateg'] = abrev(area.get('cat'))
                quadro_areas['grupo_atv'] = abrev(area.get('grp_atv'))
                quadro_areas['area_comput'] = area.get('metragem_computavel')
                quadro_areas['area_n_comput'] = area.get('metragem_naocomputavel')
                quadro_areas['area_total'] = area.get('metragem_total')
                data_container.append(quadro_areas)

            return data_container

        elif data := self.data.get('last_version'):
            # Convertendo a 'data' para uma string
            data = json.dumps(data, default=serializar_datetime)
            # Normalizando
            data = self.normalizar_area_uso(data)
            # convertendo 'data' novamente para um dicionário
            data = json.loads(data)
            # Passando as informações para o data_container
            quadro_areas = {}
            quadro_areas['tipo'] = data.get('tipo')
            quadro_areas['uni'] = data.get('unidades_uso')
            quadro_areas['subcateg'] = abrev(data.get('cat'))
            quadro_areas['grupo_atv'] = abrev(data.get('grp_atv'))
            quadro_areas['area_comput'] = data.get('metragem_computavel')
            quadro_areas['area_n_comput'] = data.get('metragem_naocomputavel')
            quadro_areas['area_total'] = data.get('metragem_total')
            data_container.append(quadro_areas)

            return data_container

    ############################
    # CERTF. CONSLUSÃO GEOINFO #
    ############################
    def get_area_objeto(self):

        return self.data.get('last_version').get('area_acrescida_pedido')

    def get_certf_tipo(self):

        return self.data.get('last_version').get('quest_certificado')

    def get_proc_vinculado(self):

        return self.data.get('last_version').get('nr_alvara_inicial')

    ###########################
    # DESPACHOS E COMUNIQUESES#
    ###########################
    def get_comuniq_count(self):
        """ Retorna o número de comunique-ses emitidos no processo.

        :return: <str>
        """
        comuniq = self.find_value('action', self.data['timeline'])
        if comuniq:
            return str(comuniq.count('Comunique-se criado'))
        else:
            return 0

    def get_deferido_count(self):
        """ Retorna o número de deferimentos no processo.

        :return: <str>
        """
        deferido = self.find_value('action', self.data['timeline'])
        if deferido:
            return str(deferido.count('Processo Deferido'))
        else:
            return 0

    def get_indeferido_count(self):
        """ Retorna o número de indeferimentos no processo.

        :return: <str>
        """
        indeferido = self.find_value('action', self.data['timeline'])
        if indeferido:
            counter = 0
            for n, i in enumerate(indeferido):
                if i == 'Processo Indeferido':
                    counter += 1

                if i == 'Processo Indeferido e Encerrado':
                    counter += 1

                if i == 'Processo Indeferido e Finalizado':
                    counter += 1

            return str(counter)
        else:
            return 0

    def get_def_indef(self):
        # Filtrando apenas despachos que foram emitidos por servidores da secretaria. 2 filtros - 1o filtro puxa todos os despachos pela timeline
        # 2o filtro puxa apenas os que foram emitidos por servidores. Após, é retornado uma lista contendo dicionários que guardam os dados de interesse
        timeline_filter = [i for i in self.data.get('timeline') if
                           (self.find_value('action', i) == 'Processo Deferido') or
                           (self.find_value('action', i) == 'Processo Indeferido') or
                           (self.find_value('action', i) == 'Processo Indeferido e Encerrado') or
                           (self.find_value('action', i) == 'Processo Indeferido e Finalizado')]

        return timeline_filter

    def get_dispatched_depachos(self):
        return [i for i in self.data.get('sei').get('dispatchedDocuments') if
                             ('Despacho' in i.get('txtTipoDocumento'))]

    def get_coord_by_publi(self, publi_date):
        coord_despacho = None
        publi_date = datetime.datetime.strptime(publi_date, '%d/%m/%Y')
        for coord, c_date in self.get_coord_entradas(self.div_bi_names):
            c_date = datetime.datetime.strptime(c_date, '%d/%m/%Y %H:%M:%S')
            if c_date < publi_date:
                coord_despacho = coord

        return coord_despacho

    def get_comuniqueses(self):

        return [i for i in self.data.get('timeline') if self.find_value('action', i) == 'Comunique-se criado']

    def get_coord_from_sector(self, sector_str):

        sector_str = sector_str.replace(' ', '') if sector_str else ''
        for i in self.coord_div_tree.items():
            if sector_str in i[1]:
                return str(i[0])

    ###########################
    #        TAXAS            #
    ###########################
    @staticmethod
    def get_taxa_nome(data):

        return data.get('detalhes').get('descricao') if data.get('detalhes') else None

    @staticmethod
    def get_valor_principal(data):

        return data.get('vlrPrincipal')

    @staticmethod
    def get_arrecadado(data):

        return data.get('arrecadada')

    @staticmethod
    def get_data_validade(data):

        return readable_date(data.get('validoPor'))

    ###########################
    #        Áreas            #
    ###########################
    def get_area_terreno(self):
        keys = ['area_terreno_real', 'terreno_real', 'escrituradoterreno', 'terreno_escritura',
                'area_terreno_realtotal', 'area_terreno_escrituratotal']

        for key in keys:
            area_terreno = self.find_value(key, self.data.get('last_version'))
            if area_terreno:
                return area_terreno
        else:
            return None

    def get_area_construir(self):
        last_version = self.data['last_version']
        computavel = float(last_version.get('construir_computavel') or 0)
        n_computavel = float(last_version.get('construir_nao_computavel') or 0)
        outros = float(last_version.get('construir_naocomputavel_outros') or 0)
        construir = float(last_version.get('construir_en') or 0)
        return computavel + n_computavel + outros + construir

    def get_area_existente(self):
        last_version = self.data['last_version']
        computavel = float(last_version.get('existente_computavel') or 0)
        n_computavel = float(last_version.get('existente_nao_computavel') or 0)
        existente = float(last_version.get('existente_reg_ref') or 0)
        return computavel + n_computavel + existente

    def get_area_regularizar(self):
        last_version = self.data['last_version']
        computavel = float(last_version.get('regularizar_computavel') or 0)
        n_computavel = float(last_version.get('regularizar_nao_computavel') or 0)
        regularizar = float(last_version.get('regularizar_ref') or 0)
        return computavel + n_computavel + regularizar

    def get_area_demolir(self):
        last_version = self.data['last_version']
        computavel = float(last_version.get('demolir_computavel') or 0)
        n_computavel = float(last_version.get('demolir_nao_computavel') or 0)
        demolir = float(last_version.get('demolir_regular_ref') or 0)
        return computavel + n_computavel + demolir

    def get_construida_total(self):
        last_version = self.data['last_version']
        if area_total := last_version.get('area_construida_total'):
            return area_total
        if area_total := last_version.get('construir_en'):
            return area_total

        construir = self.get_area_construir()
        existente = self.get_area_existente()
        regularizar = self.get_area_regularizar()
        demolir = self.get_area_demolir()

        assunto = self.get_requerimento().lower()
        # ED. NOVA
        if 'nova' in assunto:
            return construir
        # REFORMA - area total a construir = construir + existente + regularizar - demolir
        if 'reforma' in assunto:
            return construir + existente + regularizar - demolir

    ###########################
    #        Outros           #
    ###########################
    def get_num_blocos(self):
        return self.data['last_version'].get('num_blocos')

    def get_num_pavimentos(self):
        keys = ['numtotal_pavimentos', 'num_pavimentos', 'num_andar']
        for key in keys:
            pav = self.find_value(key, self.data['last_version'])
            if pav:
                return pav


    ###########################
    #        Unidades           #
    ###########################

    """def get_unidades_his(self):

        if unidades_his := self.data['last_version'].get('total_unidadesresidenciais'):
            return int(total_un)"""

    def get_num_unidades_resid(self):
        if total_un := self.data['last_version'].get('total_unidadesresidenciais'):
            return int(total_un)

        if quadro_area := self.data['last_version'].get('quadro_area_uso'):
            total_unid = 0
            for area in quadro_area:
                total_unid += (
                        (int(area.get('unidades_residencial') or 0)) +
                        (int(area.get('unidades_uso') or 0))
                )
            return total_unid

    ###########################
    #       Link Alvará       #
    ###########################
    def get_codvalid(self):

        return self.data.get('cod_valid')


    def get_templates(self):

        template_list = ["Certificado", "Certificado de Cadastro", "Alvará", "Alvará de Aprovação",
                         "Alvará - Edificações", "Alvará - Parcelamento do solo", "Alvará de Autorização", "Certidão"]
        templates = self.data.get('config_metadata').get('templates')
        return [(i['template'], i['text_button']) for i in templates if i['text_button'] in template_list]












