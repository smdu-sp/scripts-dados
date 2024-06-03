from reportlab.lib.pagesizes import A4


class BasicBlock:

    def __init__(self):

        self.width, self.height = A4
        self.x_unit = self.width / 100
        self.y_unit = self.height / 100
        self.x_margin = (self.x_unit * 5) - 0.5
        self.x_width = self.x_margin + 536.5
        self.cell_width = (self.x_width - self.x_margin) / 13
        self.cell_height = self.y_unit * 2

        # Paletes
        self.blue_pallete = [(159, 197, 232), (111, 168, 220), (61, 133, 198), (11, 83, 148), (7, 55, 99)]
        self.green_pallete = [(216, 243, 250), (196, 223, 230), (102, 165, 173), (7, 87, 91), (0, 59, 70)]
        self.orange_pallete = [(252, 229, 205), (249, 203, 156), (246, 178, 107), (230, 145, 56), (180, 95, 6)]
        self.pink_pallete = [(234, 209, 220), (213, 166, 189), (194, 123, 160), (166, 77, 121), (116, 27, 71)]


    @staticmethod
    def vertical_line(cv, pos, size):
        cv.line(pos[0], pos[1], pos[0], pos[1] + size)

    def title(self, cv, y, text):
        x = self.width / 2
        y = self.y_unit * y
        cv.setFont('Helvetica-Bold', 14)
        cv.drawCentredString(x, y, text)


    def subtitle(self, cv, y, sistemas):
        x = self.width / 2
        y = self.y_unit * y
        cv.setFont('Helvetica-Bold', 12)
        cv.drawCentredString(x, y, sistemas)


    def coord_mes(self, cv, y, coord, mes, ano):
        x = self.width / 2
        y = self.y_unit * y
        cv.setFont('Helvetica', 12)
        cv.drawCentredString(x, y, f'{coord} - {mes} de {ano}')


    def rect_title(self, cv, y, rgb_color, text):
        x = self.x_margin
        x_ = self.x_width - self.x_margin
        y = self.y_unit * y + 1.3
        y_ = self.cell_height

        # Retangulo
        r, g, b = rgb_color[-1]
        cv.setStrokeColorRGB(r / 255, g / 255, b / 255)
        cv.setFillColorRGB(r / 255, g / 255, b / 255)
        cv.rect(x, y, x_, y_, fill=1)

        # Texto
        cv.setFont('Helvetica-Bold', 12)
        cv.setStrokeColorRGB(1, 1, 1)
        cv.setFillColorRGB(1, 1, 1)
        cv.drawCentredString(self.width / 2, y + 5, text)


    def rect_subtitle(self, cv, y_pos, rgb_color_list, text):
        x = self.x_margin
        y = y_pos * self.y_unit + 0.5
        y_ = self.cell_height
        # Retangulo 1
        r, g, b = rgb_color_list[0]
        cv.setStrokeColorRGB(r / 255, g / 255, b / 255)
        cv.setFillColorRGB(r / 255, g / 255, b / 255)
        cv.rect(x, y, (self.cell_width * 9) - 1, y_, fill=1)

        for i in range(4):
            r, g, b = rgb_color_list[i + 1]
            cv.setStrokeColorRGB(r / 255, g / 255, b / 255)
            cv.setFillColorRGB(r / 255, g / 255, b / 255)
            cv.rect(x + self.cell_width * (i + 9), y, self.cell_width, y_, fill=1)

        # Texto
        cv.setFont('Helvetica-Bold', 12)
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(0, 0, 0)
        cv.drawString(x + 9, y + 4, text)


    def resumo(self, cv, y, dados, unidades_aprovadas=False):
        # Setup
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(0, 0, 0)

        # Linha 1
        self.vertical_line(cv, (self.x_unit * 7, self.y_unit * y), -(self.y_unit * 12.5))

        # Total despachos
        cv.setFont('Helvetica-Bold', 10)
        cv.drawString(self.x_unit * 10, self.y_unit * (y - 2), 'Total de Despachos')
        cv.setFont('Helvetica-Bold', 12)
        cv.drawRightString(self.x_unit * 45, self.y_unit * (y - 2), str(dados['total_despachos']))

        # Deferidos
        cv.setFont('Helvetica-Bold', 10)
        cv.drawString(self.x_unit * 10, self.y_unit * (y - 5), 'Deferidos')
        cv.setFont('Helvetica', 12)
        cv.drawRightString(self.x_unit * 45, self.y_unit * (y - 5), str(dados['deferidos']))

        # Indeferidos
        cv.setFont('Helvetica-Bold', 10)
        cv.drawString(self.x_unit * 10, self.y_unit * (y - 8), 'Indeferidos')
        cv.setFont('Helvetica', 12)
        cv.drawRightString(self.x_unit * 45, self.y_unit * (y - 8), str(dados['indeferidos']))

        # Indeferido e encerrado
        cv.setFont('Helvetica-Bold', 10)
        cv.drawString(self.x_unit * 10, self.y_unit * (y - 11), 'Indeferidos e encerrados')
        cv.setFont('Helvetica', 12)
        cv.drawRightString(self.x_unit * 45, self.y_unit * (y - 11), str(dados['indef_encerrados']))

        # Linha 2
        self.vertical_line(cv, (self.x_unit * 55, self.y_unit * y), -(self.y_unit * 12.5))

        if not unidades_aprovadas:
            # Comunicados
            cv.setFont('Helvetica-Bold', 10)
            cv.drawString(self.x_unit * 58, self.y_unit * (y - 5), 'Comunicados')
            cv.setFont('Helvetica', 12)
            cv.drawRightString(self.x_unit * 91, self.y_unit * (y - 5), str(dados['comunicados']))

            # Indeferidos
            cv.setFont('Helvetica-Bold', 10)
            cv.drawString(self.x_unit * 58, self.y_unit * (y - 8), 'Autuados')
            cv.setFont('Helvetica', 12)
            cv.drawRightString(self.x_unit * 91, self.y_unit * (y - 8), str(dados['autuados']))

        else:
            # Comunicados
            cv.setFont('Helvetica-Bold', 10)
            cv.drawString(self.x_unit * 58, self.y_unit * (y - 2), 'Comunicados')
            cv.setFont('Helvetica', 12)
            cv.drawRightString(self.x_unit * 91, self.y_unit * (y - 2), str(dados['comunicados']))

            # Indeferidos
            cv.setFont('Helvetica-Bold', 10)
            cv.drawString(self.x_unit * 58, self.y_unit * (y - 5), 'Autuados')
            cv.setFont('Helvetica', 12)
            cv.drawRightString(self.x_unit * 91, self.y_unit * (y - 5), str(dados['autuados']))

            """ # Unidades Aprovadas
            cv.setFont('Helvetica-Bold', 10)
            cv.drawString(self.x_unit * 58, self.y_unit * (y - 8), 'Unidades Aprovadas')
            cv.setFont('Helvetica', 12)
            cv.drawRightString(self.x_unit * 91, self.y_unit * (y - 8), str(dados['unidades_residenciais']))"""

    def quadro_sistemas(self, cv, y, dados, img=None, padding=5, width=350, height=150, line=1, img_y=1, img_x=1):
        # Linha
        self.vertical_line(cv, (self.x_unit * 10, self.y_unit * (y - 1) + 8), -(self.y_unit * 12 * line))

        for n, i in enumerate(dados):
            cv.setFont('Helvetica-Bold', 10)
            cv.drawString(self.x_unit * 13, self.y_unit * (y - 2 - (n * padding)), i)
            cv.setFont('Helvetica', 12)
            cv.drawRightString(self.x_unit * 38, self.y_unit * (y - 2 - (n * padding)), str(dados[i]))

        # Grafico
        if img:
            cv.drawImage(img, (self.x_unit * 40) + img_x, self.y_unit * (y - (16 * img_y)), width=width, height=height)
        else:
            pass

    def quadro_comparativo(self, cv, y_pos, img=None):
        # Setup
        x = self.x_margin
        x_ = self.x_width
        y = self.y_unit * (y_pos - 22.5)
        y_ = y + 195

        if img:
            cv.drawImage(img, self.x_unit - 27, y, width=646, height=217)

        # Margens - trocar para rect
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setLineWidth(0.05)
        cv.line(x, y, x, y_)  # Right Margin
        cv.line(x, y_, x_, y_)  # Top Margin
        cv.line(x_, y_, x_, y)  # Left Margin
        cv.line(x_, y, x, y)  # Bottom Margin

    def tabela(self, cv, y_margin, dataframe, rgb):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]

        x = self.x_margin
        x_ = self.x_width - self.x_margin
        y = self.y_unit * y_margin

        cell_size = x_ / 13
        rect_height = 2

        # Tabela
        for line in range(len(dataframe.columns) + 1):
            ref_x = x
            for i in range(6):
                # Pintando o padrão da celula
                cv.setStrokeColorRGB(1, 1, 1)  # Bordas brancas
                cv.setFillColorRGB(r / 255, g / 255, b / 255)
                cv.rect(ref_x + cell_size, y, cell_size, self.y_unit * rect_height, fill=1)
                ref_x += cell_size * 2

            cv.setStrokeColorRGB(0, 0, 0)
            cv.setFillColorRGB(1, 1, 1)
            cv.rect(x, y, x_, self.y_unit * rect_height)
            y -= self.y_unit * rect_height

        # Valores setup
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(0, 0, 0)
        y = self.y_unit * y_margin

        # Meses
        cv.setFont('Helvetica-Bold', 9)
        cv.drawCentredString(x + cell_size / 2, y + 5, ' ')
        for n, i in enumerate(dataframe.index):
            cv.drawCentredString((x + cell_size * (n + 2)) - cell_size / 2, y + 4, str(i))

        # Dados
        for n, i in enumerate(dataframe.columns):
            cv.setFont('Helvetica-Bold', 9) if i != 'Indeferidos' else cv.setFont('Helvetica-Bold', 7,5)
            y_pos = (y - (self.y_unit * rect_height) * (n + 1)) + 5
            text = 'AD' if i == 'Aprova Digital' else i
            cv.drawCentredString(x + cell_size / 2, y_pos, str(text))
            for n2, value in enumerate(dataframe[i]):
                cv.setFont('Helvetica', 9) if i != 'Total' else cv.setFont('Helvetica-Bold', 10)
                cv.drawCentredString((x + cell_size * (n2 + 2)) - cell_size / 2, y_pos, str(value))

    def assuntos(self, cv, y_base, assuntos_dict, pallete):

        y = (y_base - 1) * self.y_unit

        # Cores
        color = pallete[0]
        white = (255, 255, 255)

        sorted_assuntos = sorted(assuntos_dict.items(), key=lambda x: x[1], reverse=True)

        for n, i in enumerate(sorted_assuntos):
            # Definindo cores das linhas - colorido para pares e branco para ímpares
            if n % 2 == 0:
                r, g, b = white
            else:
                r, g, b = color

            cv.setStrokeColorRGB(r / 255, g / 255, b / 255)
            cv.setFillColorRGB(r / 255, g / 255, b / 255)
            cv.rect(self.x_margin, y - (n * self.cell_height), (self.cell_width * 13) - 1, self.cell_height, fill=1)

            # Texto
            cv.setFont('Helvetica', 10)
            cv.setStrokeColorRGB(0, 0, 0)
            cv.setFillColorRGB(0, 0, 0)
            cv.drawString(self.x_margin + 9, y - (n * self.cell_height) + 4, str(i[0]))
            cv.drawString(self.x_margin + (self.cell_width * 8) + 9, y - (n * self.cell_height) + 4, str(i[1]))

            # Sparkline
            spark_max_width = (self.cell_width * 4) - 5
            spark_max_value = sorted_assuntos[0][1]

            sparkline_width = spark_max_width * i[1] / spark_max_value
            sparkline_height = self.cell_height - 6
            sparkline_init = (self.cell_width * 9) + 30

            r, g, b = pallete[-1]
            cv.setStrokeColorRGB(r / 255, g / 255, b / 255)
            cv.setFillColorRGB(r / 255, g / 255, b / 255)
            cv.rect(sparkline_init, y - (n * self.cell_height) + 3.5, sparkline_width, sparkline_height, fill=1)

        # Borda
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(1, 1, 1)
        cv.rect(self.x_margin, y - (len(sorted_assuntos) - 1) * self.cell_height, self.cell_width * 13,
                self.cell_height * len(sorted_assuntos))

        return (y - (self.cell_height * len(sorted_assuntos))) / self.y_unit

    def comparativo_mes(self, cv, y_base, pallete, dados, mes_ref, mes_ant):

        y = (y_base * self.y_unit) - (self.y_unit * 4)

        for i in range(5):

            color = pallete[0]
            white = (255, 255, 255)

            # Definindo cores das linhas - colorido para pares e branco para ímpares
            if i % 2 == 0:
                r, g, b = white
            else:
                r, g, b = color

            cv.setStrokeColorRGB(r / 255, g / 255, b / 255)
            cv.setFillColorRGB(r / 255, g / 255, b / 255)
            cv.rect(self.x_margin, y - (i * self.cell_height * 3) - (self.cell_height * 2),
                    (self.cell_width * 6.0) - 1, self.cell_height * 3, fill=1)

        # Texto - meses
        cv.setFont('Helvetica-Bold', 10)
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(0, 0, 0)
        cv.drawString(self.x_margin + (self.cell_width * 1.9), y - self.cell_height + 4, str(mes_ant))
        cv.drawString(self.x_margin + (self.cell_width * 3.4), y - self.cell_height + 4, str(mes_ref))
        cv.drawString(self.x_margin + (self.cell_width * 5.3), y - self.cell_height + 4, str('%'))

        # Texto valores
        cv.setFont('Helvetica', 10)
        for n, i in enumerate(dados):
            #  Calcule a posição y para começar o texto de forma centralizada
            #  start_y = height / 2 + total_text_height / 2 + y

            try:
                percent = round((i[1] * 100 / i[0]) - 100, 2)
            except ZeroDivisionError:
                percent = 0
            cv.drawString(self.x_margin + (self.cell_width * 2.2), y - (self.cell_height * n * 3) - self.cell_height * 3.6, str(i[0]))
            cv.drawString(self.x_margin + (self.cell_width * 3.7), y - (self.cell_height * n * 3) - self.cell_height * 3.6, str(i[1]))
            cv.drawString(self.x_margin + (self.cell_width * 4.9), y - (self.cell_height * n * 3) - self.cell_height * 3.6, str(f'{percent}%'))

            # SPARK LINES
            cv.setLineWidth(0.5)

            spark_x = self.x_margin + (self.cell_width * 2)
            spark_x2 = spark_x + 100
            # Up
            if percent > 0:
                spark_y = y - (self.cell_height * n * 3) - self.cell_height * 2.7
                spark_y2 = spark_y + 9
            ## Equal
            if percent == 0:
                spark_y = (y - (self.cell_height * n * 3) - self.cell_height * 2.7) + 3
                spark_y2 = spark_y
            ## Down
            if percent < 0:
                spark_y = (y - (self.cell_height * n * 3) - self.cell_height * 2.7) + 9
                spark_y2 = spark_y - 9


            cv.line(spark_x, spark_y, spark_x2, spark_y2)

        # Bordas
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(1, 1, 1)
        cv.rect(self.x_margin, y - (self.cell_height * 14), self.cell_width * 6.0, self.cell_height * 15)

        # Texto títulos
        cv.setFont('Helvetica-Bold', 10)
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(0, 0, 0)

        tit_list = ('Despachos', 'Deferidos', 'Indeferidos', 'Comuniq.')
        for n, i in enumerate(tit_list):
            cv.drawString(self.x_margin + (self.cell_width * 0.1), y - (self.cell_height * n * 3) - self.cell_height * 2.7, str(i))


        # Subtítulo
        subtitulo = f'Comparativo {mes_ant} - {mes_ref}'
        cv.setFont('Helvetica-Bold', 12)
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(0, 0, 0)
        cv.drawCentredString((self.cell_width * 7) / 2, y + self.y_unit + 14, subtitulo)

    def acumulado(self, cv, y_base, pallete, subtitulo, dados):

        y = (y_base * self.y_unit) - (self.y_unit * 4)

        for i in range(7):

            color = pallete[0]
            white = (255, 255, 255)

            # Definindo cores das linhas - colorido para pares e branco para ímpares
            if i % 2 == 0:
                r, g, b = white
            else:
                r, g, b = color

            cv.setStrokeColorRGB(r / 255, g / 255, b / 255)
            cv.setFillColorRGB(r / 255, g / 255, b / 255)
            cv.rect(self.x_margin + (self.cell_width * 7.0), y - (i * self.cell_height * 2.0) - (self.cell_height * 2),
                    (self.cell_width * 6.0) - 1, self.cell_height * 2.5, fill=1)

        # Texto títulos
        cv.setFont('Helvetica-Bold', 10)
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(0, 0, 0)

        tit_list = ('Despachos', 'Deferidos', 'Indeferidos', 'Indef. Encerrados', 'Comunique-ses', 'Autuados', 'Estoque')
        for n, i in enumerate(tit_list):
            cv.drawString(self.x_margin + (self.cell_width * 7.2),
                          y - (self.cell_height * n * 2) - self.cell_height * 0.8, str(i) + ':')

        # Texto Valores
        cv.setFont('Helvetica', 10)
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(0, 0, 0)
        for n, i in enumerate(dados.values()):
            cv.drawRightString(self.x_margin + (self.cell_width * 12.5),
                          y - (self.cell_height * n * 2) - self.cell_height * 0.8, str(i))

        # Bordas
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(1, 1, 1)
        cv.rect(self.x_margin + (self.cell_width * 7.0), y - (self.cell_height * 14), self.cell_width * 6.0, self.cell_height * 15)

        # Subtítulo
        subtitulo = str(subtitulo)
        cv.setFont('Helvetica-Bold', 12)
        cv.setStrokeColorRGB(0, 0, 0)
        cv.setFillColorRGB(0, 0, 0)
        cv.drawCentredString((self.cell_width * 10.5), y + self.y_unit + 14, subtitulo)


if __name__ == '__main__':
    a = BasicBlock()
