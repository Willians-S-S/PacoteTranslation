from PyPDF2 import PdfReader
from googletrans import Translator
from typing import Optional
from fpdf import FPDF
from pytesseract import pytesseract
import os
from fpdf.errors import FPDFUnicodeEncodingException

class TranslatePDF():

    def __init__(self):
        self.listaIMG = []

    # caso o usuário especifica a página unica, e o intervalo ele vai fazer apenas da página unica
    def ler(
            self, 
            caminho: str, 
            idioma: str, 
            caminho_save_pdf: Optional[str] = None,
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
        if os.path.isfile(caminho):
            pdf = PdfReader(caminho)  # Lê o arquivo PDF no caminho especificado
            texto = ''  # Inicializa a variável que irá armazenar o texto extraído

            # Se o parâmetro `page` for especificado, extrai o texto da página correspondente
            if page is not None:
                texto = pdf.pages[page].extract_text()

                texto = self.trans_text_bigger(texto, idioma)
                
                if check_img:
                    if caminho_save_img is None:  
                        caminho_save_img = os.getcwd()
                    
                    self.extract_image_of_page(pdf.pages[page], caminho_save_img)

            # Se o parâmetro `interval` for especificado, extrai o texto de um intervalo de páginas
            elif interval is not None:
                interval = interval.split('-')
                aux = ''
                if int(interval[0]) >= 0 and int(interval[1]) <= len(pdf.pages):
                    for i in range(int(interval[0]), int(interval[1]) + 1):
                        aux = pdf.pages[i].extract_text()
                        texto += self.trans_text_bigger(aux, idioma)
                        # texto += self.traducao(aux, idioma)
                        if check_img:    
                            if caminho_save_img is None:  
                                caminho_save_img = os.getcwd()
                            self.extract_image_of_page(pdf.pages[i], caminho_save_img)

            # Caso nenhum dos parâmetros `page` ou `interval` seja especificado, extrai o texto de todas as páginas
            else:
                aux = ''
                for pag in pdf.pages:
                    aux = pag.extract_text()
                    texto += self.trans_text_bigger(aux, idioma)
                    # texto += self.traducao(aux, idioma)
                    if check_img:    
                        if caminho_save_img is None:  
                            caminho_save_img = os.getcwd()
                        self.extract_image_of_page(aux, caminho_save_img) 
                
            # Se o parâmetro `ret` for igual a 'txt', salva o texto traduzido em um arquivo chamado 'retorno.txt'
            if ret == 'pdf':
                if '/' in caminho:
                    tam = len(caminho) - 1
                    while caminho[tam] != '/':
                        print(caminho[tam])
                        tam -= 1
                    caminho = caminho[tam + 1:]
                
                nome_arquivo = 'saida_' + caminho
                
                texto = texto.replace('•', '')
                
                if caminho_save_pdf is None:
                    caminho_save_pdf = os.getcwd()

                self.gerarPDF(texto, nome_arquivo, caminho_save_pdf)

            # Caso contrário, imprime o texto traduzido na saída padrão
            else:
                print(texto)
        else:
            print("Arquivo não encontrado")
    
    def trans_text_bigger(self, texto, idioma):
        tam = 500
        texto2 = ''
        while len(texto) > tam:
            if texto[tam] == ' ':
                aux = texto[:tam]
                texto = texto[tam:]
                texto2 += self.traducao(aux, idioma) 
            else:
                while texto[tam] != ' ':
                    tam -= 1
                if texto[tam] == ' ':
                    aux = texto[:tam]
                    texto = texto[tam:]
                    texto2 += self.traducao(aux, idioma)
        else:
            texto2 += self.traducao(texto, idioma)  # Traduz o texto extraído para o idioma especificado pelo parâmetro `idioma`
        return texto2

    def traducao(self, texto, idioma):
        trans = Translator()
        textoTraduzido = trans.translate(texto, dest=idioma)
        return textoTraduzido.text

    def gerarPDF(self, texto, nome_arquivo, caminho_save_pdf) -> None:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("times", "", 14)
            pdf.multi_cell(txt=texto, w=0, align="j")
            pdf.output(caminho_save_pdf + '/' + nome_arquivo)
        except FPDFUnicodeEncodingException as e:
            e = str(e)
            print(f"O {e[:13]} não é suportado pela a fonte times, tente novamente sem a saída em pdf.")

    def extrairIMG(self, caminho, caminho_save: Optional[str] = None, all: Optional[int] = None) -> None:
        if os.path.isfile(caminho):
            if caminho_save is None:
                caminho_save = os.getcwd()

            reader = PdfReader(caminho)
            if all is not None:
                if all >= 0 and all <= all:
                    page = reader.pages[all]
                    self.extract_image_of_page(page)
                else:
                    return None
            else:
                for page in reader.pages:
                    self.extract_image_of_page(page)
        else:
            print("Arquivo não encontrado.")

    def extract_image_of_page(self, page, caminho_save: Optional[str] = None):
        count = 0
        for image_file_object in page.images:
            print(str(count) + image_file_object.name) #-> aqui pega o nome da imagem
            with open(caminho_save + "/" + str(count) + image_file_object.name, "wb") as fp:
                print(caminho_save + "/" + str(count) + image_file_object.name)
                fp.write(image_file_object.data)
                count += 1

    def lerImg(self, caminho_image, idioma: Optional[str] = None):
        if os.path.isfile(caminho_image):
            sistema = os.name

            if sistema == 'nt':
                # C:\Users\09wei\AppData\Local\Programs\Tesseract-OCR\tesseract.exe
                # https://github.com/UB-Mannheim/tesseract/wiki
                usuario = os.getlogin()
                caminho_tesseract = f"C:\\Users\\{usuario}\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
                pytesseract.tesseract_cmd = caminho_tesseract

            texto = pytesseract.image_to_string(caminho_image)
            
            if idioma is not None:
                texto = self.traducao(texto, idioma)
            print(texto)
        else:
            print('Arquivo não encontrad.')

a = TranslatePDF()

# a.extrairIMG(1)
a.ler("prova_final.pdf", idioma='pt', page=0)
# a.lerImg('R.png')
