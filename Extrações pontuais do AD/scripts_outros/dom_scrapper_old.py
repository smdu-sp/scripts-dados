import requests  # To acess the online files
import fitz
import os
import csv
import logging

"""The orginal pdf is divided in four columns and it's read from the latest to the first, so the text retrieved
 comes shuffled. For that fitz is used since is more compatible with the working machine and also brings each word 
 separated with their coordinates, getting this coordinates we can unshuffle the pdf and proceed to datamining"""


class DomCrawler:

    def __init__(self, year='2021', month='Fevereiro', day='16', page='02'):
        """ The obj is initiated with date related atributes, containers for data and some lambda functions to
        update info.
        """
        self.page = page
        self.day = day
        self.month = month
        self.year = year
        self.url = 'http://diariooficial.imprensaoficial.com.br/doflash/prototipo/{0}/{1}/{2}/cidade/pdf/pg_00{3}.pdf'
        self.dom_url = lambda url: url.format(self.year, self.month, self.day, self.page)

        self.ad_container = []
        self.document = 'backup_dom_files/{0}-{1}-{2} p{3} m.pdf'
        self.month_dict = {'Janeiro': '01', 'Fevereiro': '02', 'Março': '03', 'Abril': '04', 'Maio': '05', 'Junho': '06',
                      'Julho': '07', 'Agosto': '08', 'Setembro': '09', 'Outubro': '10', 'Novembro': '11',
                      'Dezembro': '12'}
        self.next_office = ''
        self.dom_doc = lambda doc: doc.format(self.year, self.month_dict[self.month], self.day, self.page)

    def get_summary(self):
        """ This method is designed to read specifically from the index page of the document, and retrieve it's text
        return: <str> - The text in the top half of the page
        """
        # Getting url response with requests
        response = requests.get(self.dom_url(self.url))
        response.raise_for_status()  # making sure that there is a edition on that day

        # Making a file to store the pdf file
        with open('backup_dom_files/get_text.pdf', 'w+b') as pdf_file:
            pdf_file.write(response.content)
        # Using fitz module and using it to read from the previously saved pdf
        doc = fitz.open('backup_dom_files/get_text.pdf')
        page = doc[0]
        words = page.get_text('words')

        text = ''
        # getting only the text that matters (top half of the page) and excluding repeated and bugging prone information
        for i in words:
            if i[1] < 542:
                text += i[4] + ' '

        return text

    def data_get_summary(self, text, office):

        cut = text.find(office)
        if cut == -1:
            print('There is no office in that day')
        text = text[cut:]
        char = 38
        page_init_number = ''
        page_final_number = 0
        next_office = ''
        signal_off = False

        for i in range(100):
            if text[char] == '.' or text[char] == '\n' or text[char] == ' ':

                if signal_off:
                    break

            elif text[char].isdigit():
                page_init_number += text[char]

            elif text[char].isalpha():
                next_office += text[char]
                signal_off = True

            char += 1
        # print(page_init_number, next_office)
        return page_init_number, next_office, text

    def get_pdf_text(self):
        # Retorna o texto em pdf de determinado link
        # Getting url response with requests
        print('get', self.dom_url(self.url))
        response = requests.get(self.dom_url(self.url))

        # Making a file to store the pdf file
        with open('temp_doc.pdf', 'w+b') as pdf_file:
            for chunk in response.iter_content(50000):
                pdf_file.write(chunk)
        # Using fitz module
        doc = fitz.open('temp_doc.pdf')
        page = doc[0]
        words = page.get_text('words')
        # getting text per columns
        coluna1, coluna2, coluna3, coluna4 = '', '', '', ''

        for i in words:
            # i[0] = left, i[1] = top, i[2] = right, i[3] = botom
            # Coordenadas coluna1
            if i[0] > 39 and i[1] > 50 and i[2] < 215 and i[3] < 1180:
                coluna1 += i[4] + ' '
            # Coordenadas coluna2
            if i[0] > 218 and i[1] > 50 and i[2] < 395 and i[3] < 1180:
                coluna2 += i[4] + ' '
            # Coordenadas coluna3
            if i[0] > 398 and i[1] > 50 and i[2] < 570 and i[3] < 1180:
                coluna3 += i[4] + ' '
            # Coordenadas coluna4
            if i[0] > 577 and i[1] > 50 and i[3] < 1180:
                coluna4 += i[4] + ' '

        texto = coluna1 + ' ' + coluna2 + ' ' + coluna3 + ' ' + coluna4
        return (self.cleaner(texto))

    def cleaner(self, text):

        text = text[2:]
        word_swap = (('- ', ''), ('578', '578'), ('\\br/\\> ', ''))

        for simbol, correct in word_swap:
            text = text.replace(simbol, correct)

        return text

    def pages_to_be_looked(self, initial, final):

        ini, fin = int(initial), int(final)

        if ini == fin:
            return [str(ini)]
        else:
            return [str(i + ini) for i in range(fin - ini + 1)]

    def big_texts(self, pages):

        dom_content = ''
        for i in pages:
            if int(i) < 10:
                self.page = '0' + i
            else:
                self.page = i
            dom_content += self.get_pdf_text()

        return dom_content

    def get_dom_proc(self):

        office = 'LICENCIAMENTO'
        summary_text = self.get_summary()
        page_init, next_office, first_text = self.data_get_summary(summary_text, office)
        self.next_office = next_office
        page_final, x, y = self.data_get_summary(first_text, next_office)
        pages = self.pages_to_be_looked(page_init, page_final)
        dom_content = self.big_texts(pages)

        return dom_content

    def get_AdProcess(self, text):

        while True:
            cut_ini = text.find('ocesso SEI:')
            if cut_ini == -1:
                break
            # print(self.next_office)
            signal_words_fin = ['Processo SEI', 'Processo n', 'ocesso SEI:', self.next_office, 'SECRETÁRIO',
                                'SECRETARIA']
            cut = [text.find(word, cut_ini + 1) for word in signal_words_fin if text.find(word, cut_ini + 1) > 0]
            # print(cut)
            try:
                cut_fin = min(cut)
            except ValueError as exc:
                print('EXC<<<<<<<<<<', exc, '>>>>>>>>>>>>>')
                pass

            if '6067.20' in text[cut_ini:cut_fin]:
                break
            else:
                self.ad_container.append(text[cut_ini:cut_fin])
                # print(text[cut_ini:cut_fin], cut_ini, cut_fin,'\n\n')
                # input()
                text = text[cut_fin:]

        return self.ad_container


class AdProcess:

    def __init__(self, text, year, month, day, page):

        self.text_data = text
        date = year + '/' + str(month) + '/' + day
        self.data_container = {'Data': date, 'Pag.': page}

    def get_data(self):
        # Caso de processo Declaratório:

        if 'teressado' not in self.text_data:
            # Processo SEI
            cut_sei = self.text_data.find(':')
            self.data_container['Processo SEI'] = self.text_data[cut_sei+1:cut_sei+21]
            # Interessado
            self.data_container['Interessado'] = ''
            # N° AD
            cut_ad = self.text_data.find('número', cut_sei)
            ad_final = cut_ad + 19
            if len(self.text_data) > 30:
                for i in range(3):
                    if self.text_data[ad_final].isalpha():
                        ad_final += 1
            if self.text_data[cut_ad+7:ad_final][-1] == 'e':
                ad_final -= 1
            self.data_container['N° AD'] = self.text_data[cut_ad+7:ad_final]
            # Assunto
            cut_subject_init = self.text_data.find('assunto', ad_final)
            cut_subject_final = self.text_data.find('foi', cut_subject_init)
            self.data_container['Assunto'] = self.text_data[cut_subject_init+8:cut_subject_final-1]
            # Resultado
            cut_result_init = self.text_data.find('foi', ad_final)
            cut_result_final = self.text_data.find('.', cut_result_init)
            self.data_container['Resultado'] = self.text_data[cut_result_init+4:cut_result_final]

            self.data_container['Despacho'] = self.text_data[cut_result_final+2:cut_result_final+1000]
        else:
            # Caso do processo comum, com nome do interessado
            # Processo SEI
            cut_sei = self.text_data.find(':')
            self.data_container['Processo SEI'] = self.text_data[cut_sei+1:cut_sei+21]
            # Interessado
            cut_customer_init = self.text_data.find(':', cut_sei+1)
            cut_customer_final = self.text_data.find('processo de', cut_customer_init)
            self.data_container['Interessado'] = self.text_data[cut_customer_init+2:cut_customer_final-2]
            # N° AD
            cut_ad = self.text_data.find('número', cut_customer_final)
            ad_final = cut_ad + 19
            if len(self.text_data) > 30:
                for i in range(3):
                    if self.text_data[ad_final].isalpha():
                        ad_final += 1
            if self.text_data[cut_ad+7:ad_final][-1] == 'e':
                ad_final -= 1
            self.data_container['N° AD'] = self.text_data[cut_ad+7:ad_final]
            # Assunto
            cut_subject_init = self.text_data.find('assunto', ad_final)
            cut_subject_final = self.text_data.find('foi', cut_subject_init)
            self.data_container['Assunto'] = self.text_data[cut_subject_init+8:cut_subject_final-1]
            # Resultado
            cut_result_init = self.text_data.find('foi', ad_final)
            cut_result_final = self.text_data.find('.', cut_result_init)
            self.data_container['Resultado'] = self.text_data[cut_result_init+4:cut_result_final]

            self.data_container['Despacho'] = self.text_data[cut_result_final+2:cut_result_final+1000]

        return self.data_container


def remove_file(*file_path):

    for file in file_path:
        if os.path.exists(file):
            os.remove(file)


# Creating a CSV file and it's header
remove_file('output.csv')


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


def get_dom_data(year, month, day):

    # This try statment is basically to bypass the requests.raise_for_status() in DomCrawler in case of no edition is made in a given date
    try:
        proc = DomCrawler(year, month, day)  # getting a DOM obj at desired date
        response = proc.get_dom_proc()  # getting a full text to read data from while creating evidence files
        ad_text = proc.get_AdProcess(response)  # breaking the text in parts of interest
        for i in ad_text:
            # print(i, '\n')
            ad_data = AdProcess(i, proc.year, proc.month_dict[month], proc.day, proc.page)  # Getting and organizing the data
            output_csv(ad_data.get_data())  # Passing the data to a csv file
            # print(ad_data.get_data(), "\n")
            # input()
    except Exception as exc:
        print('\nThere was a problem: %s' %(exc))
        pass


def main():
    """ Control the two classes that are needed to make this dataminer work, also controls de date gathering and csv file writing
    return: void
    """
    # Looping trough calendar days
    years = ['2020', '2021', '2022', '2023']
    months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    # year = '2022'
    # month = 'Novembro'
    # day='14'
    for year in years:
        for month in months:
            for i in range(1, 32):
                # Adding a 0 to make url work
                if i < 10:
                    day = '0' + str(i)
                else:
                    day = str(i)

                get_dom_data(year, month, day)


if __name__ == '__main__':
    main()
