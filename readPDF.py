from PyPDF2 import PdfReader
from translation import traducao




def ler(caminho, idioma, page = None, interval = None, ret=None):

    pdf = PdfReader(caminho)
    texto = ''

    if page:
        texto = pdf.pages[page].extract_text()
    elif interval:
        interval = interval.split('-')
        for i in range(int(interval[0]), int(interval[1]) + 1):
            texto +=  pdf.pages[i].extract_text()
    else:
        for i in range(len(pdf.pages)):
            texto += pdf.pages[i].extract_text()

    texto = traducao(texto, idioma)

    if ret == 'txt':
        with open('retorno.txt', 'w') as arquivo:
            arquivo.write(texto)
    else:
        print(texto)
