from PyPDF2 import PdfReader
from translation import traducao
from typing import Optional
from gerarPDF import gerar

def ler(caminho: str, idioma: str, page: Optional[int] = None, interval: Optional[str] = None, ret: Optional[str] = None) -> None:
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
    
    # Se o parâmetro `interval` for especificado, extrai o texto de um intervalo de páginas
    elif interval is not None:
        interval = interval.split('-')
        for i in range(int(interval[0]), int(interval[1]) + 1):
            texto += pdf.pages[i].extract_text()
    
    # Caso nenhum dos parâmetros `page` ou `interval` seja especificado, extrai o texto de todas as páginas
    else:
        for i in range(len(pdf.pages)):
            texto += pdf.pages[i].extract_text()
    
    texto = traducao(texto, idioma)  # Traduz o texto extraído para o idioma especificado pelo parâmetro `idioma`
    
    # Se o parâmetro `ret` for igual a 'txt', salva o texto traduzido em um arquivo chamado 'retorno.txt'
    if ret == 'txt':
        texto = texto.replace('•', '')
        gerar(texto)
        # with open('retorno.txt', 'w') as arquivo:
        #     arquivo.write(texto)
    # Caso contrário, imprime o texto traduzido na saída padrão
    else:
        print(texto)
