import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pdf_basicblocks import BasicBlock
# from data_container2 import data
import json
import os


# noinspection PyArgumentList
# noinspection PyMethodParameters
class Report(BasicBlock):

    def __init__(self, dados):
        super().__init__()

        self.y_fixed_init = 95
        self.y_init = self.y_fixed_init

        self.dados = dados


        self.block_placement_dict = self.dados['block_placement']

        self.delta_y = {
            'title': 2,
            'subtitle': 2.3,
            'coord_mes': 4,
            'rect_title': 2,
            'rect_subtitle': 2,
            'resumo': 18,
            'quadro_sistemas': 20,
            'quadro_comparativo': 25.5,
            'quadro_comparativo_simples': 26.0,
            'tabela': 11,
            'comparativo_mes': 25,
        }

        self.delta_bloco = {
            'bloco_titulo': self.delta_y['title'] + self.delta_y['subtitle'] + self.delta_y['coord_mes'],
            'bloco_resumo': self.delta_y['rect_title'] + self.delta_y['rect_subtitle'] + self.delta_y['resumo'],
            'bloco_fontes': self.delta_y['rect_subtitle'] + self.delta_y['quadro_sistemas'],
            'bloco_comparativo': self.delta_y['rect_subtitle'] + self.delta_y['quadro_comparativo'] + self.delta_y['tabela'],
            'bloco_autuacoes': self.delta_y['rect_subtitle'] + self.delta_y['quadro_comparativo_simples'],
            'bloco_comparativo_acumulado': self.delta_y['rect_subtitle'] + self.delta_y['comparativo_mes'],
            'bloco_final': 0.1,
        }

        if self.dados.get('assuntos').get('aprova_digital'):
            sorted_ad_assuntos = sorted(self.dados['assuntos']['aprova_digital']['data'].items(), key=lambda x: x[1], reverse=True)
            ad = {'ad_assuntos': (self.cell_height * len(sorted_ad_assuntos) / self.y_unit) + 3.5}
            self.delta_y.update(ad)
            bl_ad = {'bloco_ad_assunto': self.delta_y['rect_subtitle'] + self.delta_y['ad_assuntos']}
            self.delta_bloco.update(bl_ad)

        if self.dados.get('assuntos').get('sissel'):
            sorted_sissel_assuntos = sorted(self.dados['assuntos']['sissel']['data'].items(), key=lambda x: x[1], reverse=True)
            ss = {'sissel_assuntos': (self.cell_height * len(sorted_sissel_assuntos) / self.y_unit)+ 4}
            self.delta_y.update(ss)
            bl_ss = {'bloco_sissel_assunto': self.delta_y['rect_subtitle'] + self.delta_y['sissel_assuntos']}
            self.delta_bloco.update(bl_ss)

    def page_turner_decorator(func):
        def wrapper(self, *args):
            cv = args[0]
            y = args[1]
            dados = args[2]
            actual_block = args[3]
            next_block = args[4]

            func(self, cv, y, dados)

            self.y_init -= actual_block
            if self.y_init <= next_block:
                cv.showPage()
                self.y_init = self.y_fixed_init

        return wrapper

    @page_turner_decorator
    def bloco_titulo(self, cv, y, dados):

        a = self.delta_y['title']
        b = self.delta_y['subtitle']

        self.title(cv, y, dados['titulo'])
        self.subtitle(cv, y - a, dados['sistemas'])
        self.coord_mes(cv, y - a - b, dados['coord'], dados['mes'], dados['ano'])

    @page_turner_decorator
    def bloco_resumo(self, cv, y, dados):

        a = self.delta_y['rect_title']
        b = self.delta_y['rect_subtitle']

        pallete = self.pal_color(dados['pallete'])

        self.rect_title(cv, y, pallete, dados['titulo'])
        self.rect_subtitle(cv, y - a, pallete, dados['subtitulo'])
        self.resumo(cv, y - a - b, dados['data']) # , dados['unidades_resid']


    @page_turner_decorator
    def bloco_fontes(self, cv, y, dados):

        a = self.delta_y['rect_subtitle']
        pallete = self.pal_color(dados['pallete'])

        width = dados.get('img_width')
        height = dados.get('img_height')
        line = dados.get('line_size')
        img_y = dados.get('img_y')
        img_x = dados.get('img_x')
        self.quadro_sistemas(cv, y - a, dados['data'], dados['img'], padding=dados['padding'], width=width,
                             height=height, line=line, img_y=img_y, img_x=img_x)
        self.rect_subtitle(cv, y, pallete, dados['titulo'])

    @page_turner_decorator
    def bloco_comparativo(self, cv, y, dados):

        a = self.delta_y['rect_subtitle']
        b = self.delta_y['quadro_comparativo']
        pallete = self.pal_color(dados['pallete'])

        data_frame = pd.DataFrame(dados['data'], index=dados['data_index'])

        self.quadro_comparativo(cv, y - a, dados['img'])
        self.rect_subtitle(cv, y, pallete, dados['titulo'])
        self.tabela(cv, y - a - b, data_frame, pallete[0])

    @page_turner_decorator
    def bloco_comuniqueses(self, cv, y, dados):

        a = self.delta_y['rect_subtitle']
        pallete = self.pal_color(dados['pallete'])

        self.rect_subtitle(cv, y, pallete, dados['titulo'] + dados['mes'])
        self.quadro_sistemas(cv, y - a, dados['data'], dados['img'], padding=6)

    @page_turner_decorator
    def bloco_autuacoes(self, cv, y, dados):

        a = self.delta_y['rect_subtitle']
        pallete = self.pal_color(dados['pallete'])

        self.quadro_comparativo(cv, y - a, dados['img'])
        self.rect_subtitle(cv, y, pallete, dados['titulo'])

    @page_turner_decorator
    def bloco_assuntos(self, cv, y, dados):

        a = self.delta_y['rect_subtitle']
        pallete = self.pal_color(dados['pallete'])

        self.rect_subtitle(cv, y, pallete, dados['titulo'])
        self.assuntos(cv, y - a, dados['data'], pallete)

    @page_turner_decorator
    def bloco_comparativo_acumulado(self, cv, y, dados):

        a = self.delta_y['rect_subtitle']
        pallete = self.pal_color(dados['pallete'])

        dados_comp = dados['comparativo_mes']
        dados_acumulado = dados['acumulado']

        self.rect_subtitle(cv, y, pallete, dados_comp['titulo'])
        self.comparativo_mes(cv, y - a, pallete, dados_comp['data'], dados_comp['mes_ref'], dados_comp['mes_ant'])
        self.acumulado(cv, y - a, pallete, dados_acumulado['subtitulo'], dados_acumulado['data'])

    @page_turner_decorator
    def bloco_final(self, cv, y):
        pass

    def pal_color(self, color):

        if color == 'blue_pallete':
            return self.blue_pallete
        if color == 'green_pallete':
            return self.green_pallete
        if color == 'orange_pallete':
            return self.orange_pallete
        if color == 'pink_pallete':
            return self.pink_pallete

    def block_placer(self, cv):

        keys = list(self.block_placement_dict.keys())
        values = list(self.block_placement_dict.values())
        for index, func_name in enumerate(keys):
            if func_name == 'bloco_final':
                break
            if 'page_turner' in func_name:
                cv.showPage()
                self.y_init = self.y_fixed_init
            else:
                actual_block = self.block_placement_dict.get(keys[index]).get('tamanho_base')
                try:
                    next_block = self.block_placement_dict.get(keys[index + 1]).get('tamanho_base')
                except IndexError:
                    next_block = 1

                dados = self.block_placement_dict.get(keys[index])

                func = getattr(self, dados.get('block_name'))
                func(cv, self.y_init, dados, actual_block, next_block)



if __name__ == '__main__':
    pdf_files = os.listdir('pdf_relatorios/')
    for file in pdf_files:
        os.remove(f'pdf_relatorios/{file}')


    files = os.listdir('rel_parametrizacao')
    for file in files:
        print(file)
        with open(f'rel_parametrizacao\\{file}', 'r') as json_file:
            data = json.load(json_file)

            cv = canvas.Canvas(f"pdf_relatorios/{data['metadata']['coord']} {data['metadata']['created_at']}.pdf", pagesize=A4) #-{data['metadata']['created_at']}
            report = Report(data)
            report.block_placer(cv)

            cv.save()


