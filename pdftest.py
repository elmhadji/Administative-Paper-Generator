import qrcode 
from PyPDF2 import PdfFileReader
from cv2 import imread
from os import remove
def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    print(txt)
    return information


from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display



class PDF(FPDF):
    def lines(self):
        pdf_w=210
        pdf_h=297
        self.set_line_width(0.0)
        self.line(5.0,5.0,205.0,5.0) # top one
        self.line(5.0,292.0,205.0,292.0) # bottom one
        self.line(5.0,5.0,5.0,292.0) # left one
        self.line(205.0,5.0,205.0,292.0) # right one

    def imagex(self):
        img='DesktopAPP/IMAGE/logo2.png'
        self.set_xy(6.0,6.0)
        self.image(name=img,link='',type='',w=195,h=35)

    def titles(self):
        self.set_xy(0.0,0.0)
        self.set_font('Arial','B',16)
        #self.set_text_color(220,50,50)
        self.cell(w=210.0,h=70.0,align='',txt='help',border=0)

    def qrcod(self):
        qr =qrcode.make("hello")
        qr.save("DesktopAPP/IMAGE/qrcod.png")
        img =''
        self.set_xy(20,20)
        self.image(name='DesktopAPP/IMAGE/qrcod.png',link='',type='',w=50,h=50)
        remove('DesktopAPP/IMAGE/qrcod.png')

pdf = PDF(orientation='P',unit='mm',format='A4')
pdf.add_page()
pdf.add_font('DejaVu', '', 'dejavu-fonts-ttf-2.37/ttf/DejaVuSansCondensed.ttf', uni=True)
pdf.set_font('DejaVu', '', 14)
#pdf.add_font('gargi', '', 'gargi.ttf', uni=True)
#pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
#pdf.set_font('DejaVu', '', 14)
name ="helllo"
reshaped_text = arabic_reshaper.reshape(u'{}اللغة العربية رائعة'.format(name))
bidi_text = get_display(reshaped_text)
pdf.cell(w=0.0,h=70.0,txt= bidi_text,align='R')
#pdf.image(name='C:/Users/a-elm/Desktop/work/DesktopAPP/qrcod.jpg',link='',type='',w=50,h=50)

#pdf.qrcod()
pdf.output('test.pdf','F')
print('programe complete')

#if __name__ == '__main__':
    #path = 'reportlab-sample.pdf'
    #extract_information(path)
    