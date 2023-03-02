from PyPDF2 import PdfReader
from googletrans import Translator
from typing import Optional
from fpdf import FPDF
from pytesseract import pytesseract
import os

class TranslatePDF():

    def __init__(self):
        self.listaIMG = []

    # caso o usuário especifica a página unica, e o intervalo ele vai fazer apenas da página unica
    def ler(
            self, 
            caminho: str, 
            idioma: str, 
            page: Optional[int] = None, 
            interval: Optional[str] = None, 
            ret: Optional[str] = None,
            check_img: Optional[bool] = None,
            caminho_save_img: Optional[str] = None
            ) -> None:
        """
        Esta função lê um arquivo PDF no caminho especificado pelo parâmetro `caminho`,
        extrai o texto do PDF usando a biblioteca `PdfReader` e o traduz para o idioma
        especificado pelo parâmetro `idioma` usando uma função chamada `traducao`. O texto
        traduzido é então salvo em um arquivo chamado 'retorno.txt' se o parâmetro `ret` for
        igual a 'txt', ou impresso na saída padrão se o parâmetro `ret` não for especificado
        ou for diferente de 'txt'.

        Parameters:
            caminho: str
                O caminho para o arquivo PDF que será lido.
            idioma: str
                o idioma para o qual o texto será traduzido.
            page: int,
                optional a página do PDF a partir da qual o texto será extraído.
                Se este parâmetro não for especificado, o texto será extraído de
                todas as páginas do PDF. Default é None.
            interval: str
                optional um intervalo de páginas (no formato 'x-y') a partir do
                qual o texto será extraído. Se este parâmetro não for especificado,
                o texto será extraído de todas as páginas do PDF. Default é None.
            ret: str
                optional se igual a 'txt', o texto traduzido será salvo em um arquivo
                chamado 'retorno.txt'. Caso contrário, o texto será impresso na saída
                padrão. Default é None.
        Returns:
            None
        """
        pdf = PdfReader(caminho)  # Lê o arquivo PDF no caminho especificado
        texto = ''  # Inicializa a variável que irá armazenar o texto extraído

        # Se o parâmetro `page` for especificado, extrai o texto da página correspondente
        if page is not None:
            texto = pdf.pages[page].extract_text()
            texto = self.traducao(texto, idioma)  # Traduz o texto extraído para o idioma especificado pelo parâmetro `idioma`
            if check_img:
                if caminho_save_img is None:  
                    caminho_save_img = os.getcwd()
                self.extract_image_of_page(pdf.pages[page], )

        # Se o parâmetro `interval` for especificado, extrai o texto de um intervalo de páginas
        elif interval is not None:
            interval = interval.split('-')
            aux = ''
            if int(interval[0]) >= 0 and int(interval[1]) <= len(pdf.pages):
                for i in range(int(interval[0]), int(interval[1]) + 1):
                    aux = pdf.pages[i].extract_text()
                    texto += self.traducao(aux, idioma)
                    if check_img:    
                        if caminho_save_img is None:  
                            caminho_save_img = os.getcwd()
                        self.extract_image_of_page(pdf.pages[i])

        # Caso nenhum dos parâmetros `page` ou `interval` seja especificado, extrai o texto de todas as páginas
        else:
            aux = ''
            for pag in pdf.pages:
                aux = pag.extract_text()
                texto += self.traducao(aux, idioma)
                if check_img:    
                    if caminho_save_img is None:  
                        caminho_save_img = os.getcwd()
                    self.extract_image_of_page(aux) 
            
        # Se o parâmetro `ret` for igual a 'txt', salva o texto traduzido em um arquivo chamado 'retorno.txt'
        if ret == 'pdf':
            texto = texto.replace('•', '')
            self.gerarPDF(texto)
        # Caso contrário, imprime o texto traduzido na saída padrão
        else:
            print(texto)

    def traducao(self, texto, idioma):
        trans = Translator()
        textoTraduzido = trans.translate(texto, dest=idioma)
        return textoTraduzido.text

    def gerarPDF(self, texto) -> None:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "", 14)
        pdf.multi_cell(txt=texto, w=0, align="j")
        pdf.output("recibo.pdf")

    def extrairIMG(self, all: Optional[int] = None) -> None:
        reader = PdfReader("b.pdf")
        if all is not None:
            if all >= 0 and all <= all:
                page = reader.pages[all]
                self.extract_image_of_page(page)
            else:
                return None
        else:
            for page in reader.pages:
                self.extract_image_of_page(page)

    def extract_image_of_page(self, page, caminho_save: Optional[str] = None):
        if caminho_save is None:
            caminho_save = os.getcwd()
        count = 0
        for image_file_object in page.images:
            print(str(count) + image_file_object.name) #-> aqui pega o nome da imagem
            with open(str(count) + image_file_object.name, "wb") as fp:
                fp.write(image_file_object.data)
                count += 1

    def lerImg(self, caminho_image, idioma: Optional[str] = None):
        texto = pytesseract.image_to_string(caminho_image)
        if idioma is not None:
            texto = self.traducao(texto, idioma)
        print(texto)

# Quando estiver executando chama pra extrair imagem se extrair guarda o nome em uma variavel, aí depois só passar para traduzir

a = TranslatePDF()

# a.extrairIMG(1)
a.ler("f.pdf", idioma='en', ret='pdf', page = 0, check_img=True)
# a.lerImg('0X5.jpg', 'pt')