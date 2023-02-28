from fpdf import FPDF

def gerar(texto):

    pdf = FPDF()

    pdf .add_page()

    pdf .set_font("helvetica", "", 14)

    pdf.multi_cell(txt=texto, w=0, align="j")
    pdf.output("recibo.pdf") 

