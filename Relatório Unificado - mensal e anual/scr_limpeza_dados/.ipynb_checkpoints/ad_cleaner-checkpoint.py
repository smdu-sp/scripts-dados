# Limpa os dados extraídos do AD
import pandas as pd
import os


class AdTableCleaner:
    
    def __init__(self):
        # Absolute path para o diretório atual
        dir_atual = os.path.abspath(os.path.dirname(__file__))
        # Absolute path para o diretório irmão onde os arquivos serão criados
        self.dir_raw_data = os.path.abspath(os.path.join(dir_atual, '..', 'raw_data'))
        self.dir_cleaned_data = os.path.abspath(os.path.join(dir_atual, '..', 'cleaned_data'))

    def clean_ad_tabela_principal(self):
        #####################################################
        ######## Limpando dados da planilha principal #######
        #####################################################

        main_df = pd.read_csv(f'{self.dir_raw_data}/ad_principal_raw.csv', encoding='latin-1', sep=';')

        # <<<<< Excluindo processos não autuados >>>>>
        main_df = main_df.query("n_processo != 'Sei não criado'")
        
        # Procurando por processos com valores inconsistentes - TESTE
        inc_values = main_df.query("n_processo.str.len() != 19").index
        
        # <<<<< Excluindo processos com valores inconsistentes >>>>>
        main_df = main_df.drop(index=inc_values)
        
        # >>> Salvando a planilha modificada
        main_df.to_csv(f'{self.dir_cleaned_data}/ad_principal.csv',  encoding='latin-1', sep=';', index=False)

    def clean_ad_tabela_despachos(self):    
        ######################################################
        ####### Limpando dados da planilha de despachos ######
        ######################################################

        desp_df = pd.read_csv(f'{self.dir_raw_data}/ad_despachos_raw.csv', encoding='latin-1', sep=';')
        # desp_df = pd.read_csv(f'files/arquivo/ad_despachos_{self.filename}.csv', encoding='latin-1', sep=';')
        # Verificar se por algum acaso há algum processo sem número
        test_aut = desp_df.query("n_processo == 'Sei não criado'")
        # Verificar esse casos de processos não criados com despacho - no momento serão apagados
        desp_df = desp_df.query("n_processo != 'Sei não criado'")
        # Realinhando os indexes
        desp_df = desp_df.reset_index(drop=True)
        
        # Analisando entradas distintas para o campo 'quem_despachou'
        # distinct_entries = list(desp_df.quem_despachou.unique())
        # distinct_entries.sort()
        
        # <<<<< Correção de nomes duplicados - padronização >>>>>
        # Para cada nome x, substituir por nome y
        nomes_padr = [
            ('Camila Bonilha', 'Camila Luciana Cabral Bonilha'),
            ('Renaldo Moura', 'Renaldo Silva de Moura'),
            ('Viviane Urioste', 'Viviane Stankevicius Urioste'),
            ('SILVIO  LUIZ SILVIO LUIZ RODRIGUES DE CAMARGO', 'SILVIO LUIZ RODRIGUES DE CAMARGO')
            ]
        for errado, certo in nomes_padr:
            desp_df['quem_despachou'] = desp_df['quem_despachou'].str.replace(errado, certo)
        
        # <<<<< Limpeza de espaços em branco >>>>>
        # Retirar espaço em branco de todas as entradas da coluna
        desp_df['quem_despachou'] = desp_df['quem_despachou'].str.strip()
        desp_df['quem_despachou'] = desp_df['quem_despachou'].str.replace('  +', ' ', regex=True)
        
        # distinct_entries = list(desp_df.quem_despachou.unique())
        # distinct_entries.sort()
        
        # Localizando despachos sem divisão
        desp_filter = desp_df.query("(coord_despacho.isnull()) & (quem_despachou != 'Desconhecido/Evento Automático')")
        
        # <<<<< Adição de coordenadorias >>>>>
        # Colocando a divisão correta
        test = desp_df.query("(n_processo == '1010.2020/0007037-4') & (coord_despacho.isnull())").index
        test2 = desp_df.iat[18,0]
        desp_df.iat[desp_df.query("(n_processo == '1010.2020/0007037-4') & (coord_despacho.isnull())").index[0], 4] = 'SMUL/PARHIS'
        desp_df.iat[desp_df.query("(n_processo == '1010.2020/0008244-5') & (coord_despacho.isnull())").index[0], 4] = 'SMUL/PARHIS'
        desp_df.iat[desp_df.query("(n_processo == '1010.2020/0007703-4') & (coord_despacho.isnull())").index[0], 4] = 'SMUL/COMIN'
        desp_df.iat[desp_df.query("(n_processo == '1020.2020/0015772-5') & (coord_despacho.isnull())").index[0], 4] = 'SMUL/COMIN'
        desp_df.iat[desp_df.query("(n_processo == '1010.2020/0008278-0') & (coord_despacho.isnull())").index[0], 4] = 'SMUL/CONTRU'
        desp_df.iat[desp_df.query("(n_processo == '1020.2020/0015146-8') & (coord_despacho.isnull())").index[0], 4] = 'SMUL/CONTRU'
        desp_df.iat[desp_df.query("(n_processo == '1020.2020/0014876-9') & (coord_despacho.isnull())").index[0], 4] = 'SMUL/CONTRU'
        
        # <<<<<< Padronização de coordenadorias e divisões >>>>>
        # Padronizando coordenadorias e divisões
        desp_df['coord_despacho'] = desp_df['coord_despacho'].str.replace('SMUL/CONTRU/ DSUS', 'CONTRU/ DSUS')
        desp_df['coord_despacho'] = desp_df['coord_despacho'].str.replace('CONTRU/ DSUS', 'SMUL/CONTRU/DSUS')
        desp_df['coord_despacho'] = desp_df['coord_despacho'].str.replace('SEL/RESID/ DRGP', 'SMUL/RESID/DRGP')
        
        distinct_entries = list(desp_df.coord_despacho.unique())
        # desp_df.drop('quem_despachou', axis=1, inplace=True)
        
        # >>> Salvando a planilha modificada
        desp_df.to_csv(f'{self.dir_cleaned_data}/ad_despachos.csv',  encoding='latin-1', sep=';', index=False)

    def clean_ad_tabela_comuniqueses(self):       
        #############################################################
        ####### Filtrando dados da planilha de comunique-ses ########
        #############################################################
        
        comun_df = pd.read_csv(f'{self.dir_raw_data}/ad_comuniqueses_raw.csv', encoding='latin-1', sep=';')
        
        # <<<<< Limpeza de espaços em branco >>>>>
        comun_df['quem_comunicou'] = comun_df['quem_comunicou'].str.strip()
        comun_df['quem_comunicou'] = comun_df['quem_comunicou'].str.replace('  +', ' ', regex=True)
        
        # <<<<< Correção de nomes duplicados >>>>>
        nomes_padr = [
            ('Camila Bonilha', 'Camila Luciana Cabral Bonilha'),
            ('Bethania Gç Souza', 'Bethania Gonçalves de Souza'),
            ('Camila Boselli de Mendonça Camila', 'Camila Boselli de Mendonça'),
            ('Carlos R.Dias', 'Carlos Rodrigues Dias'),
            ('Daniela Salgueiro Coelho martins', 'Daniela Salgueiro Coelho Martins'),
            ('daniela martins', 'Daniela Salgueiro Coelho Martins'),
            ('Denise Canto', 'Denise Moreira Canto'),
            ('EDEN MARCONI JUNIOR', 'Eden Marconi Junior'),
            ('Edmar Marino', 'Edmar Marino de Oliveira'),
            ('FABIO CORSI FERRAO', 'Fabio Corsi Ferrao'),
            ('Francisco Miguel Maturano Santoro Maturano Santoro', 'Francisco Miguel Maturano Santoro'),
            ('Iris de abreu', 'Iris Pricilla Riibeiro de Abreu'),
            ('Luis Fernando Santos', 'Luis Fernando dos Santos'),
            ('Luiz Carlos Flosi Junior', 'Luiz Carlos Flosi'),
            ('Marcos Walder', 'Marcos Roberto Walder'),
            ('Marcus Miyata', 'Marcus Lopes Miyata'),
            ('Mario Oliveira', 'Mario de Oliveira'),
            ('Milena Shikasho', 'Milena Satie Shikasho'),
            ('Milena Steffen', 'Milena Ferreira Steffen'),
            ('Renaldo Moura', 'Renaldo Silva de Moura'),
            ('Tamires Mariana de Oliveira Tamanini', 'Tamires Mariana'),
            ('Tania Filgueiras', 'Tania Cristina Filgueiras'),
            ('luis Fernando Cato', 'Luis Fernando Cato'),
            ('wilson roberto dos santos', 'Wilson Roberto dos Santos Junior'),
            ('Edmar Marino de Oliveira de Oliveira', 'Edmar Marino de Oliveira'),
            ('Fernando Costa', 'Fernando Perpetuo Costa'),
            ('LUIS OTAVIO SANTOS GUERRA', 'Luis Otavio dos Santos Guerra'),
            ('CLAUDIA EMILIA DAVID HERNANDES', 'Claudia Emilia D. Hernandes'),
            ('JOÃO MIGUEL FERREIRA', 'João Miguel Ferreira'),
            ('LIVIA TROMBINI DELLA VITTORIA', 'Lívia Trombini Della Vitória')
            ]
        for errado, certo in nomes_padr:
            comun_df['quem_comunicou'] = comun_df['quem_comunicou'].str.replace(errado, certo)
        
        # Analisando entradas distintas para comunique-ses <<TESTE>>
        distinct_entries = list(comun_df.quem_comunicou.unique())
        distinct_entries.sort()
        
        # <<<<< Adição de coordenadorias >>>>>
        # Preenchendo coordenadorias e divisões da tabela de comunique-ses
        def coord_filler(name, sector):
            temp_df = comun_df.query(f"(coord_comuniquese.isnull()) & (quem_comunicou == '{name}')")
            for i in temp_df.index:
                comun_df.iat[i, 2] = sector
        
        lista_tecnicos_fill_coord = [
            ('Alexandre Mikio Takaki', 'PARHIS'),
            ('Ana Maria Gil Auge', 'ASSEC'),
            ('Camila Boselli de Mendonça', 'SERVIN'),
            ('Celso Kawamura', 'RESID'),
            ('Daniella Romani Vidal', 'PARHIS'),
            ('Diego Teixeira Silva', 'CONTRU'),
            ('Erica Massis', 'ASSEC'),
            ('Fernanda Csordás', 'ATECC'),
            ('Fernanda Simon Cardoso', 'DEUSO'),
            ('Gabriela Mendonça', 'COMIN'),
            ('Gabriella Roesler Radoll', 'SERVIN'),
            ('Gilcilene Silva', 'ASSEC'),
            ('Helio Akamine', 'RESID'),
            ('Isabela Correia de Queiroz', 'CONTRU'),
            ('Ivens Ferreira Fernandes', 'CONTRU'),
            ('JOSE MANUEL FERREIRA CORREIA', 'CONTRU'),
            ('João Miguel Ferreira', 'CONTRU'),
            ('Leandro Della Croche', 'DEUSO'),
            ('Lucila de Almeida Sampaio Magalhães', 'RESID'),
            ('Luis Fernando Cato', 'PARHIS'),
            ('Luis Fernando dos Santos', 'COMIN'),
            ('Luis Otavio dos Santos Guerra', 'CASE'),
            ('Luiz Carlos Flosi', 'CONTRU'),
            ('Marcus Lopes Miyata', 'COMIN'),
            ('Maria Leticia Basso', 'COMIN'),
            ('Maria Regina Braga Lagonegro', 'PARHIS'),
            ('Mariclé Ortega Xavier de Araujo Mischi', 'ASSEC'),
            ('Milena Satie Shikasho', 'COMIN'),
            ('Paula Simeliovich Birman', 'ATECC'),
            ('Pedro Luiz Fonseca', 'ATECC'),
            ('ROSSANA ANDRADE MOREIRA', 'CONTRU'),
            ('Renato Pedroso dos Santos', 'CONTRU'),
            ('Roberto Angelo de Oliveira', 'CONTRU'),
            ('SUEKO HASHIMOTO', 'RESID'),
            ('Sara Caroline Lopes da Silva', 'CONTRU'),
            ('Tania Cinquini', 'DEUSO'),
            ('Tania Cristina Filgueiras', 'COMIN'),
            ('Thiago Lagonegro', 'COMIN'),
            ('takeaki watanabe', 'CONTRU')
            ]
        for name, sector in lista_tecnicos_fill_coord:
            coord_filler(name, sector)

        # >>> Salvando a planilha modificada
        comun_df.to_csv(f'{self.dir_cleaned_data}/ad_comuniqueses.csv',  encoding='latin-1', sep=';', index= False)

    def clean_table(self):
        self.clean_ad_tabela_principal()
        print('Tabela principal do Aprova Digital criada com sucesso')
        self.clean_ad_tabela_despachos()
        print('Tabela de despachos do Aprova Digital criada com sucesso')
        self.clean_ad_tabela_comuniqueses()
        print('Tabela de comunique-ses do Aprova Digital criada com sucesso')

    
if __name__ == '__main__':
    AdTableCleaner().clean_table()
