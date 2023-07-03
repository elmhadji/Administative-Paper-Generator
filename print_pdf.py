import PyQt6
from PyQt6.uic.load_ui import loadUi
from PyQt6.QtWidgets import QMainWindow, QTableWidget, QPushButton, QLabel, QLineEdit, \
    QApplication
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
import qrcode
import mysql.connector as mdb
from cryptography.fernet import Fernet
import sys
import os


class PrintPdf(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/printpdf.ui', self)
        self.title = self.findChild(QLabel, "title")
        self.btnMainpage = self.findChild(QPushButton, "mainpage")
        self.btnAdistation = self.findChild(QPushButton, "adistation")
        self.btnDiplome = self.findChild(QPushButton, "diplome")
        self.btnSearch = self.findChild(QPushButton, "btnSearch")
        self.inputSearch = self.findChild(QLineEdit, "inputSearch")
        self.mainpage.clicked.connect(self.second)
        self.btnAdistation.clicked.connect(self.showAdistation)
        self.btnDiplome.clicked.connect(self.showDiplome)  # TODO create showDiplome
        self.table = self.findChild(QTableWidget, "tableWidget")
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.stack = None
        self.secondWindow = None
        self.showAdistation()

    def showAdistation(self):
        self.stack = 0
        self.table.clear()
        self.title.setText("Adistation")
        self.table.setColumnCount(15)
        self.table.setHorizontalHeaderLabels(
            ("University", "Numero Inscription", "Numero Registrer", "Specialiter", "Domain", "Filier",
             "Nom (arabic)", "Prenom (arabic)",
             "Nom & Prenom (french)", "Annee De Naissance",
             "Lieu De Naissance", "Note", "Annee Preparer", "Annee Inscpription", "Print PDf"))
        self.table.verticalHeader().setDefaultSectionSize(10)
        self.table.horizontalHeader().setDefaultSectionSize(140)
        try:
            tablerow = 0
            conn = mdb.connect(host='localhost', user='root', password='root', database='bdd')
            cur = conn.cursor()
            cur.execute("SELECT COUNT(Num_Inscription) FROM student;")
            self.table.setRowCount(cur.fetchone()[0])
            cur.execute("SELECT * FROM student;")
            result = cur.fetchall()
            for row in result:
                num_inscription = str(row[0])
                num_registre = str(row[1])
                domain = str(row[2])
                annee_preparer = str(row[3])
                specialiter = str(row[4])
                filier = str(row[5])
                note = str(row[6])
                nom_arabic = str(row[9])
                prenom_arabic = str(row[10])
                nom_french = str(row[11])
                prenom_french = str(row[12])
                annee_de_naisance = str(row[13])
                lieu_naisance = str(row[14])
                annee_inscri = str(row[15])
                university = str(row[16])
                self.table.setItem(tablerow, 0, PyQt6.QtWidgets.QTableWidgetItem(university))
                self.table.setItem(tablerow, 1, PyQt6.QtWidgets.QTableWidgetItem(num_inscription))
                self.table.setItem(tablerow, 2, PyQt6.QtWidgets.QTableWidgetItem(num_registre))
                self.table.setItem(tablerow, 3, PyQt6.QtWidgets.QTableWidgetItem(specialiter))
                self.table.setItem(tablerow, 4, PyQt6.QtWidgets.QTableWidgetItem(domain))
                self.table.setItem(tablerow, 5, PyQt6.QtWidgets.QTableWidgetItem(filier))
                self.table.setItem(tablerow, 6, PyQt6.QtWidgets.QTableWidgetItem(nom_arabic))
                self.table.setItem(tablerow, 7, PyQt6.QtWidgets.QTableWidgetItem(prenom_arabic))
                self.table.setItem(tablerow, 8, PyQt6.QtWidgets.QTableWidgetItem(nom_french + " " + prenom_french))
                self.table.setItem(tablerow, 9, PyQt6.QtWidgets.QTableWidgetItem(annee_de_naisance))
                self.table.setItem(tablerow, 10, PyQt6.QtWidgets.QTableWidgetItem(lieu_naisance))
                self.table.setItem(tablerow, 11, PyQt6.QtWidgets.QTableWidgetItem(note))
                self.table.setItem(tablerow, 12, PyQt6.QtWidgets.QTableWidgetItem(annee_preparer))
                self.table.setItem(tablerow, 13, PyQt6.QtWidgets.QTableWidgetItem(annee_inscri))
                self.GenerateQR = QPushButton('Print PDF')
                self.GenerateQR.clicked.connect(self.handelButton)
                self.table.setCellWidget(tablerow, 14, self.GenerateQR)
                tablerow += 1

        except mdb.Error as e:
            print("Failed to get record from MySQL table: {}".format(e))

        finally:
            if conn.is_connected():
                cur.close()
                conn.close()
                print('MySQL connection is closed ')

    def showDiplome(self):
        self.stack = 1
        self.table.clear()
        self.title.setText("Diplome")
        self.table.setRowCount(0)
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels(("Numero Inscription", "Domain", "Specialiter", "Filier", "Degree",
                                              "Nom & Prenom (arabic)", "Nom & Prenom (french)", "Annee De Naissance",
                                              "Lieu De Naissance", "Date Deliberations", "University", "Departement",
                                              "Print PDf"))
        self.table.verticalHeader().setDefaultSectionSize(10)
        self.table.horizontalHeader().setDefaultSectionSize(140)
        try:
            tablerow = 0
            conn = mdb.connect(host='localhost', user='root', password='root', database='bdd')
            cur = conn.cursor()
            cur.execute("SELECT COUNT(Num_Inscription) FROM student WHERE Degree IS NOT NULL;")
            self.table.setRowCount(cur.fetchone()[0])
            cur.execute("SELECT * FROM student WHERE Degree IS NOT NULL;")
            result = cur.fetchall()
            for row in result:
                num_inscription = str(row[0])
                domain = str(row[2])
                specialiter = str(row[4])
                filier = str(row[5])
                degree = str(row[7])
                date_deleberation = str(row[8])
                nom_arabic = str(row[9])
                prenom_arabic = str(row[10])
                nom_french = str(row[11])
                prenom_french = str(row[12])
                annee_de_naisance = str(row[13])
                lieu_naisance = str(row[14])
                university = str(row[16])
                departement = str(row[17])
                self.table.setItem(tablerow, 0, PyQt6.QtWidgets.QTableWidgetItem(num_inscription))
                self.table.setItem(tablerow, 1, PyQt6.QtWidgets.QTableWidgetItem(domain))
                self.table.setItem(tablerow, 2, PyQt6.QtWidgets.QTableWidgetItem(specialiter))
                self.table.setItem(tablerow, 3, PyQt6.QtWidgets.QTableWidgetItem(filier))
                self.table.setItem(tablerow, 4, PyQt6.QtWidgets.QTableWidgetItem(degree))
                self.table.setItem(tablerow, 5, PyQt6.QtWidgets.QTableWidgetItem(nom_arabic + " " + prenom_arabic))
                self.table.setItem(tablerow, 6, PyQt6.QtWidgets.QTableWidgetItem(nom_french + " " + prenom_french))
                self.table.setItem(tablerow, 7, PyQt6.QtWidgets.QTableWidgetItem(annee_de_naisance))
                self.table.setItem(tablerow, 8, PyQt6.QtWidgets.QTableWidgetItem(lieu_naisance))
                self.table.setItem(tablerow, 9, PyQt6.QtWidgets.QTableWidgetItem(date_deleberation))
                self.table.setItem(tablerow, 10, PyQt6.QtWidgets.QTableWidgetItem(university))
                self.table.setItem(tablerow, 11, PyQt6.QtWidgets.QTableWidgetItem(departement))
                self.GenerateQR = QPushButton('Print PDF')
                self.GenerateQR.clicked.connect(self.handelButton)
                self.table.setCellWidget(tablerow, 12, self.GenerateQR)
                tablerow += 1

        except mdb.Error as e:
            print("Failed to get record from MySQL table: {}".format(e))

        finally:
            if conn.is_connected():
                cur.close()
                conn.close()
                print('MySQL connection is closed ')

    def handelButton(self):
        if self.stack == 0:
            button = self.sender()
            index = self.table.indexAt(button.pos())
            if index.column() == 14:
                university = self.table.item(index.row(), 0).text()
                num_inscription = self.table.item(index.row(), 1).text()
                num_registre = self.table.item(index.row(), 2).text()
                specialiter = self.table.item(index.row(), 3).text()
                domain = self.table.item(index.row(), 4).text()
                filier = self.table.item(index.row(), 5).text()
                nom_arabic = self.table.item(index.row(), 6).text()
                prenom_arabic = self.table.item(index.row(), 7).text()
                nom_prenom_french = self.table.item(index.row(), 8).text()
                annee_de_naisance = self.table.item(index.row(), 9).text()
                lieu_naisance = self.table.item(index.row(), 10).text()
                note = self.table.item(index.row(), 11).text()
                annee_preparer = self.table.item(index.row(), 12).text()
                annee_inscri = self.table.item(index.row(), 13).text()
                info = """
يشهد نائب عميد الكلية بان الطالب(ة):
الاسم:{}
اللقب:{}
المولود(ة):{}    ب:{}
قد سجل رسميا للموسم الجامعي {}
رقم التسجيل: {}
رقم السجل: {}
لتحضير السنة:{}
الميدان: {}
الفرع: {}
التخصص: {}
الملاحظة: {}
 """.format(nom_arabic, prenom_arabic, annee_de_naisance, lieu_naisance, annee_inscri, num_inscription, num_registre,
            annee_preparer,
            domain, filier, specialiter, note)
                info_qr = """
جامعة: {}
الاسم:{}
اللقب:{}
المولود(ة):{}    ب:{}
قد سجل رسميا للموسم الجامعي {}
رقم التسجيل: {}
رقم السجل: {}
لتحضير السنة:{}
الميدان: {}
الفرع: {}
التخصص: {}
الملاحظة: {}
""".format(university, nom_arabic, prenom_arabic, annee_de_naisance, lieu_naisance, annee_inscri, num_inscription,
           num_registre,
           annee_preparer,
           domain, filier, specialiter, note)
                reshaped_text = arabic_reshaper.reshape(info)
                new_info = get_display(reshaped_text)
                pdf = FPDF(orientation='p', unit='mm', format="A4")
                pdf.add_page()
                pdf.rect(5.0, 5.0, 200.0, 287.0)
                pdf.rect(8.0, 8.0, 194.0, 282.0)
                pdf.set_xy(10, 10)
                pdf.image(name='IMAGE/logo2.png', link='', type='', w=190, h=40)
                pdf.set_xy(0, 0)
                pdf.add_font('DejaVu', '', 'dejavu-fonts-ttf-2.37/ttf/DejaVuSansCondensed.ttf', uni=True)
                pdf.set_font('DejaVu', '', 20)
                pdf.cell(w=210, h=130, align='C', txt=get_display(arabic_reshaper.reshape('شهادة مدرسية')))
                pdf.set_xy(10, 60)
                pdf.multi_cell(w=190, h=15, txt=new_info, border='', align='R')
                key = "icL5BirdckXVHl_lHUS5ezrSDYChH1myFWzVfYUbrj4="
                fernet = Fernet(key)
                encMessage = fernet.encrypt(info_qr.encode())
                # encMessage = "A" + str(encMessage)
                qr = qrcode.make(encMessage)
                qr.save("IMAGE/qrcode.png")
                pdf.set_xy(15, 226)
                pdf.image(name='IMAGE/qrcode.png', link='', type='', w=50, h=50)
                if os.path.exists("IMAGE/qrcode.png"):
                    os.remove("IMAGE/qrcode.png")
                pdf.output("Adistation.pdf", 'F')

        elif self.stack == 1:
            button = self.sender()
            index = self.table.indexAt(button.pos())
            print(index.row(), index.column())
            if index.column() == 12:
                domain = self.table.item(index.row(), 1).text()
                specialiter = self.table.item(index.row(), 2).text()
                filier = self.table.item(index.row(), 3).text()
                degree = self.table.item(index.row(), 4).text()
                nom_prenom_arabic = self.table.item(index.row(), 5).text()
                nom_prenom_french = self.table.item(index.row(), 6).text()
                annee_de_naisance = self.table.item(index.row(), 7).text()
                lieu_naisance = self.table.item(index.row(), 8).text()
                date_deleberation = self.table.item(index.row(), 9).text()
                university = self.table.item(index.row(), 10).text()
                departement = self.table.item(index.row(), 11).text()
                if (degree == "LICENCE"):
                    degree_arabic = "الليسانس"
                elif (degree == "MASTER"):
                    degree_arabic = "الماستر"
                elif (degree == "DOCTORA"):
                    degree_arabic = "الدكتوراه"
                info = """
جامعة مصطفى اسطمبولي بمعسكر بمقتضى:
-المرسوم التنفيذي رقم 08-265 المؤرخ في 19 أوت 2008 المتضمن نظام الدراسات للحصول على شهادة الليسانس و شهادة الماستر و شهادة الدكتوراه
-القرار رقم 576 المؤرخ في 5 أوت 2015 المتضمن مطابقة التكوينات في الليسانس المؤهلة بجامعة معسكر في ميدان "{}"
-محضر جلسة المداولات بتاريخ {}
بيشهد ان السيد(ة)/ الانسة: {}      المولود(ة) في: {}     ب: {}
قد تحصل(ت) على شهادة: {}       {}
في ميدان: {}
فرع: {}
تخصص: {}
بكلية: {}
بمعسكر          تاريخ: {}
عميد الكلية            مدير الجامعة
""".format(domain, date_deleberation, nom_prenom_arabic, annee_de_naisance, lieu_naisance, degree_arabic, degree,
           domain, filier, specialiter, university, date_deleberation)
                info_qr = """
Nom & Prenom (french):{}
Nom & Prenom (arabic):{}
Date De Naissance: {}
Lieu De Naissance: {}
Domain: {}
Filier: {}
Specialite: {}
""".format(nom_prenom_french, nom_prenom_arabic, annee_de_naisance, lieu_naisance, domain, filier, specialiter)
                reshaped_text = arabic_reshaper.reshape(info)
                new_info = get_display(reshaped_text)
                pdf = FPDF(orientation='l', unit='mm', format="A4")
                pdf.add_page()
                pdf.set_xy(10, 10)
                pdf.image(name='IMAGE/logo2.png', link='', type='', w=270, h=40)
                pdf.set_xy(40, 0)
                pdf.add_font('DejaVu', '', 'dejavu-fonts-ttf-2.37/ttf/DejaVuSansCondensed.ttf', uni=True)
                pdf.set_font('DejaVu', '', 20)
                pdf.cell(w=210, h=130, align='C', txt=get_display(arabic_reshaper.reshape('شهادة نجاح مؤقتة')))
                pdf.set_xy(10, 60)
                pdf.set_font('DejaVu', '', 14)
                pdf.multi_cell(w=280, h=8, txt=new_info, border='', align='R')
                key = "icL5BirdckXVHl_lHUS5ezrSDYChH1myFWzVfYUbrj4="
                fernet = Fernet(key)
                encMessage = fernet.encrypt(info_qr.encode())
                # encMessage ="B"+str(encMessage)
                qr = qrcode.make(encMessage)
                qr.save("IMAGE/qrcode.png")
                pdf.set_xy(15, 135)
                pdf.image(name='IMAGE/qrcode.png', link='', type='', w=50, h=50)
                if os.path.exists("IMAGE/qrcode.png"):
                    os.remove("IMAGE/qrcode.png")
                pdf.output("Diplom.pdf", 'F')

    def second(self):
        from databasse import DataBasse
        self.secondWindow = DataBasse()
        self.secondWindow.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = PrintPdf()
    myapp.show()
    try:
        sys.exit((app.exec()))
    except SystemExit():
        print('Closing Window')
