# Module Imports
import mysql.connector
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Absolute path para o diretório atual
dir_atual = os.path.abspath(os.path.dirname(__file__))
# Absolute path para o diretório irmão onde os arquivos serão criados
dir_raw_data = os.path.abspath(os.path.join(dir_atual, '..', 'dat_raw'))
logging.info(f'Extraindo documentos para {dir_raw_data}')

# Connect to MariaDB Platform
mydb = mysql.connector.connect(
    user="root",
    password="selsystem",
    host="10.75.34.253",
    port=3306,
    database="bi_sissel"
)
cursor = mydb.cursor()

query_despachos = """
                    SELECT 
                        P_ANO_AUTC_PCSS, 
                        P_COD_NRO_PCSS, 
                        P_COD_DIGI_PCSS,
                        Assunto AS assunto,
                        Situacao AS situacao, 
                        DataPublicacao AS data_despacho, 
                        Unidade AS coord_despacho 
                    
                    FROM despachossissel
                    
                    WHERE
                        DataPublicacao != 'NULL'
                        AND
                        Situacao != 'DOCUMENTAL'
                    """

query_comuniqueses = """
                    SELECT 
                        P_ANO_AUTC_PCSS,
                        P_COD_NRO_PCSS,
                        P_COD_DIGI_PCSS,
                        P_DT_PUBL_DOM AS data_comuniquese,
                        UNIDADE AS coord_comuniquese
                    
                    FROM comuniqueses
                    
                    WHERE 
                        P_DT_PUBL_DOM != 'NULL'
                    """

sissel_despachos = pd.read_sql(query_despachos, mydb)
sissel_comuniqueses = pd.read_sql(query_comuniqueses, mydb)

sissel_despachos.to_csv(f'{dir_raw_data}/sissel_despachos_raw.csv', sep=';', encoding='latin-1', index=False)
logging.info('SISSEL_EXTRACT - Tabela de despachos exportada para pasta raw_data')

sissel_comuniqueses.to_csv(f'{dir_raw_data}/sissel_comuniqueses_raw.csv', sep=';', encoding='latin-1', index=False)
logging.info('SISSEL_EXTRACT - Tabela de comunique-ses exportada para pasta raw_data')

mydb.close()
