import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.uic.load_ui import loadUi


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/MainPage.ui', self)
        self.btnLogout = self.findChild(QPushButton, "Logout")
        self.btnDataBass = self.findChild(QPushButton, "DataBass")
        self.btnPrintPdf = self.findChild(QPushButton, "PrintPdf")
        self.btnPrintPdf.clicked.connect(self.PrintPdf_page)
        self.btnDataBass.clicked.connect(self.DataBass_page)
        self.btnLogout.clicked.connect(self.Logout_page)
        self.page = None

    def Logout_page(self):
        if self.page != None:
            self.page = None
        if self.page is None:
            from login import LoginForm
            self.page = LoginForm()
            self.page.show()
            self.close()

    def DataBass_page(self):
        if self.page != None:
            self.page = None
        if self.page is None:
            from databasse import DataBasse

            self.page = DataBasse()
            self.page.show()
            self.close()

    def PrintPdf_page(self):
        if self.page != None:
            self.page = None
        if self.page is None:
            from print_pdf import PrintPdf

            self.page = PrintPdf()
            self.page.show()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MainPage()
    myapp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('clossing window')
