import pandas as pd
from bs4 import BeautifulSoup
import os


def table_reader(filename):
    with open(filename, 'r') as strange_file:
        file = strange_file.read()

    strange_symbol = file[3]
    cleaned_file = file.replace(strange_symbol, '')

    soup = BeautifulSoup(cleaned_file, 'html.parser')

    table_container = [[i.text for i in row.find_all('td')] for row in soup.find_all('tr')]

    return pd.DataFrame(table_container[1:], columns=table_container[0])


def new_name(filename):
    name = filename[:-4]
    return name + '.xlsx'



for document in os.listdir():
    if document.endswith('.xls'):
        print(f'Documento {document} encontrado, iniciando conversão')
        data_frame = table_reader(document)
        data_frame.to_excel(new_name(document), index=False)
        print(f'Documento {document} convertido e xlsx criado')



