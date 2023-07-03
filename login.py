import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QMessageBox
from PyQt6.uic.load_ui import loadUi
import mysql.connector as mdb


class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/LogIn.ui', self)
        self.email = self.findChild(QLineEdit, "Email")
        self.password = self.findChild(QLineEdit, "Password")
        self.submit = self.findChild(QPushButton, "Login")
        self.submit.clicked.connect(self.login)
        self.second = None

    def login(self):
        email = str(self.email.text())
        password = str(self.password.text())
        if email != '' and password != '':
            try:
                conn = mdb.connect(host='localhost', user='root', password='root', database='bdd')
                cur = conn.cursor()
                cur.execute("SELECT * FROM admin WHERE Email= %s AND Password= %s;", (email, password))
                result = cur.fetchone()
                print(result)
                if result == None:
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("congratulation")
                    dlg.setText("Le Email et Password Pas Correct")
                    dlg.exec()
                    self.close()
                else:
                    if self.second is None:
                        from main_page import MainPage
                        self.second = MainPage()
                    self.second.show()
                    self.close()
            except mdb.Error as e:
                print("Failed to get record from MySQL table: {}".format(e))
            finally:
                if conn.is_connected():
                    cur.close()
                    conn.close()
                    print('MySQL connection is closed ')
        elif email == '' or password == '':
            print('please fill all the information')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = LoginForm()
    myapp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('clossing window')
