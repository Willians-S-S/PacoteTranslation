from pytesseract import pytesseract
from translation import traducao

def lerImg():
    texto = pytesseract.image_to_string('dockerfile.jpg')
    print(texto)
    traducao(texto, 'en')
