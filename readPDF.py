from PyPDF2 import PdfReader
from googletrans import Translator
from typing import Optional
from fpdf import FPDF
from pytesseract import pytesseract
import os
from fpdf.errors import FPDFUnicodeEncodingException

class TranslatePDF():

    def extract_data_pdf(
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
        Esta método lê um arquivo PDF no caminho especificado pelo parâmetro `caminho`,
        extrai o texto do PDF, e o traduz para o idioma especificado pelo parâmetro `idioma` 
        usando uma função chamada `traducao`. O texto traduzido é então salvo em um arquivo 
        'saida_nomeArquivo.pdf' se o parâmetro `ret` for igual a 'pdf', ou impresso na saída 
        padrão se o parâmetro `ret` não for especificado ou for diferente de 'pdf'. O método
        também verifica se há imagens na página, se o parâmentro check_img estiver definido
        como True.

        Parameters
        -----------
            caminho: str 
                Caminho para o arquivo PDF.
            idioma: str 
                Idioma para o qual o texto deve ser traduzido.
            caminho_save_pdf: Optional[str]
                Caminho para salvar o arquivo PDF gerado. Padrão é None.
            page: Optional[int]
                Número da página para extrair o texto. Padrão é None.
            interval: Optional[str]
                Intervalo de páginas para extrair o texto no formato 'x-y', onde x é o número 
                da página inicial e y é o número da página final. Padrão é None.
            ret: Optional[str]
                Se definido como 'pdf', salva o texto traduzido em um arquivo PDF. Caso contrário,
                imprime o texto traduzido na saída padrão. Padrão é None.
            check_img: Optional[bool]
                Se definido como True, verifica se há imagens na página especificada. Padrão é None.
            caminho_save_img: Optional[str]
                Caminho para salvar as imagens extraídas. Padrão é None.
        Return
        ------
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
                    self.extract_image_page(pdf.pages[page], caminho_save_img) 

            # Se o parâmetro `interval` for especificado, extrai o texto de um intervalo de páginas
            elif interval is not None:
                interval = interval.split('-')
                aux = ''
                if int(interval[0]) >= 0 and int(interval[1]) <= len(pdf.pages):
                    for i in range(int(interval[0]), int(interval[1]) + 1):
                        aux = pdf.pages[i].extract_text()
                        texto += self.trans_text_bigger(aux, idioma)
                        if check_img:    
                            if caminho_save_img is None:  
                                caminho_save_img = os.getcwd()
                            self.extract_image_page(pdf.pages[i], caminho_save_img)

            # Caso nenhum dos parâmetros `page` ou `interval` seja especificado, extrai o texto de todas as páginas
            else:
                aux = ''
                for pag in pdf.pages:
                    aux = pag.extract_text()
                    texto += self.trans_text_bigger(aux, idioma)
                    if check_img:    
                        if caminho_save_img is None:  
                            caminho_save_img = os.getcwd()
                        self.extract_image_page(aux, caminho_save_img) 
                
            # Se o parâmetro `ret` for igual a 'txt', salva o texto traduzido em um arquivo chamado 'retorno.txt'
            if ret == 'pdf':
                print(caminho)
                if '/' in caminho:
                    tam = len(caminho) - 1
                    while caminho[tam] != '/':
                        print(caminho[tam])
                        tam -= 1
                    caminho = caminho[tam + 1:]
                nome_arquivo = 'saida_' + caminho
                texto = texto.replace('•', '').replace('–','').replace('𝑥','')
                if caminho_save_pdf is None:
                    caminho_save_pdf = os.getcwd()
                self.gerarPDF(texto, nome_arquivo, caminho_save_pdf)

            # Caso contrário, imprime o texto traduzido na saída padrão
            else:
                print(texto)
        else:
            print("Arquivo não encontrado")
    
    def trans_text_bigger(self, texto, idioma):
        """
            Traduz o texto extraído para o idioma especificado pelo parâmetro `idioma`. 
            
            Parameters
            ----------
            texto: str
                O texto extraído do arquivo PDF.
            idioma: str 
                O idioma para o qual o texto será traduzido.
            Return
            ------
            Retorna o texto traduzido.
        """
        tam = 500
        texto2 = ''
        while len(texto) > tam: # Se o texto tiver mais que 500 caracteres ele vai traduzir o texto por partes
            if texto[tam] == ' ': # Verifica se na posição 500 da string é um espaço
                aux = texto[:tam] # aux recebe os 500 primeiros caracteres
                texto = texto[tam:] # texto recebe o restante dos caracteres
                texto2 += self.traducao(aux, idioma)   
            else:
                while texto[tam] != ' ': # Esse loope acontece até encontrar o espaço em branco antes do caractere 500
                    tam -= 1
                if texto[tam] == ' ':
                    aux = texto[:tam]
                    texto = texto[tam:]
                    texto2 += self.traducao(aux, idioma)
        else:
            texto2 += self.traducao(texto, idioma)  # Traduz o texto extraído para o idioma especificado pelo parâmetro `idioma`
        return texto2

    def traducao(self, texto, idioma):
        """
            Método que realiza a tradução de um texto para o idioma especificado.

            Parameters
            ----------
            texto: str
                Texto a ser traduzido.
            idioma: str
                Idioma para o qual o texto deve ser traduzido.

            Retorn
            ------
                Retorna o texto traduzido para o idioma especificado.
        """
        trans = Translator()
        textoTraduzido = trans.translate(texto, dest=idioma)
        return textoTraduzido.text

    def gerarPDF(self, texto, nome_arquivo, caminho_save_pdf) -> None:
        """
            Gera um arquivo PDF a partir de um texto e o salva em um diretório especificado.

            Parameters
            ----------
            texto: str
                o texto que será salvo no arquivo PDF
            nome_arquivo: str
                o nome do arquivo PDF a ser gerado
            caminho_save_pdf: str
                o caminho onde o arquivo PDF será salvo
            Return
            ------
                None
                raises FPDFUnicodeEncodingException: se o texto contém um caractere que não é suportado 
                pela fonte "times", um erro é lançado e a função imprime uma mensagem de erro.
        """
        try:
            if os.path.isdir(caminho_save_pdf):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("times", "", 14)
                pdf.multi_cell(txt=texto, w=0, align="j")
                pdf.output(caminho_save_pdf + '/' + nome_arquivo)
            else:
                print("Diretório para salvar pdf não encontrado.")
        except FPDFUnicodeEncodingException as e:
            e = str(e)
            print(f"O {e[:13]} não é suportado pela a fonte times, tente novamente sem a saída em pdf.")

    def extrairIMG(self, caminho, caminho_save: Optional[str] = None, all: Optional[int] = None) -> None:
        """
            Extrai as imagens de um arquivo PDF.

            Parameters
            ----------
            caminho: str
                Caminho do arquivo PDF a ser processado.
            caminho_save: str, optional 
                Caminho onde as imagens extraídas serão salvas. Se não for especificado, o diretório atual será usado.
            all: int, optional
                Índice da página que contém a imagem a ser extraída. Se não for especificado, todas as páginas serão processadas.
            
            Return
            ------
                None
        """
        if os.path.isfile(caminho):
            if caminho_save is None:
                caminho_save = os.getcwd()
            reader = PdfReader(caminho)
            if all is not None:
                if all >= 0 and all <= all:
                    page = reader.pages[all]
                    self.extract_image_page(page)
                else:
                    return None
            else:
                for page in reader.pages:
                    self.extract_image_page(page)
        else:
            print("Arquivo não encontrado.")

    def extract_image_page(self, page, caminho_save):
        """
            Extrai as imagens de uma página do PDF e as salva em um diretório.

            Parameters
            ----------
            page: pdfreader.Page
                Página do PDF a ser processada.
            caminho_save: str
                Caminho onde as imagens extraídas serão salvas.
            Return
            ------
                None
        """
        count = 0
        if os.path.isdir(caminho_save):
            for image_file_object in page.images:
                with open(caminho_save + "/" + str(count) + image_file_object.name, "wb") as fp:
                    print(caminho_save + "/" + str(count) + image_file_object.name)
                    fp.write(image_file_object.data)
                    count += 1
        else:
            print('Diretório para salva imagem não encontrado.')

    def extract_text_img(self, caminho_image, idioma: Optional[str] = None):
        """
            Extrai texto de uma imagem usando o OCR do Tesseract.

            Parameters
            ----------
            caminho_image: str
                caminho_image: Caminho da imagem a ser processada.
            idioma: str, optional
                idioma: Idioma do texto na imagem. Padrão é None.
            Return
            ------
                None
        """
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

# No windows
"C:\Users\09wei\Downloads\b.pdf"
# Troque \ pela / para indicar o diretorio
"C:/Users/09wei/Downloads/b.pdf"

a.extract_data_pdf("C:/Users/09wei/Downloads/b.pdf", caminho_save_pdf="C:/Users/09wei/Downloads",  idioma='pt', ret='pdf', page=0)
# a.extract_text_img('R.png')
