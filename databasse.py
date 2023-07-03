import PyQt6
from PyQt6.uic.load_ui import loadUi
from PyQt6.QtWidgets import QMainWindow, QTableWidget, QPushButton, QLabel, QLineEdit, \
    QApplication
import mysql.connector as mdb
import sys


class DataBasse(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/DataBasse.ui', self)
        self.Third = None
        self.title = self.findChild(QLabel, 'TitleTable')
        self.inputSearch = self.findChild(QLineEdit, 'inputSearch')
        self.btnSearch = self.findChild(QPushButton, 'btnSearch')
        self.btnSearch.clicked.connect(self.search)
        self.btnAddStudent = self.findChild(QPushButton, 'btnAddStudent')
        self.btnAddStudent.clicked.connect(self.addStudent)
        self.table = self.findChild(QTableWidget, 'tableWidget')
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.stack = None
        self.btnDiplome = self.findChild(QPushButton, 'btnDiplome')
        self.btnAdistation = self.findChild(QPushButton, 'btnAdistation')
        self.btnRefresh = self.findChild(QPushButton, 'btnRefresh')
        self.btnRefresh.clicked.connect(self.refresh)
        self.btnAdistation.clicked.connect(self.showAdistation)
        self.btnDiplome.clicked.connect(self.showDiplome)
        self.btnprintpdf = self.findChild(QPushButton, "btnprintpdf")
        self.btnprintpdf.clicked.connect(self.printpdf)
        self.showAdistation()

    def showAdistation(self):
        self.stack = 0
        self.table.clear()
        self.title.setText("Adistation")
        self.table.setColumnCount(18)
        self.table.setHorizontalHeaderLabels(
            ("University", "Numero Inscription", "Numero Registrer", "Specialiter", "Domain", "Filier",
             "Nom (arabic)", "Prenom (arabic)",
             "Nom (french)", "Prenom (french)", "Annee De Naissance",
             "Lieu De Naissance", "Note", "Annee Preparer", "Annee Inscpription", "Departement", "Modifier", "Delet"))
        self.table.verticalHeader().setDefaultSectionSize(10)
        self.table.horizontalHeader().setDefaultSectionSize(130)
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
                departement = str(row[17])
                self.table.setItem(tablerow, 0, PyQt6.QtWidgets.QTableWidgetItem(university))
                self.table.setItem(tablerow, 1, PyQt6.QtWidgets.QTableWidgetItem(num_inscription))
                self.table.setItem(tablerow, 2, PyQt6.QtWidgets.QTableWidgetItem(num_registre))
                self.table.setItem(tablerow, 3, PyQt6.QtWidgets.QTableWidgetItem(specialiter))
                self.table.setItem(tablerow, 4, PyQt6.QtWidgets.QTableWidgetItem(domain))
                self.table.setItem(tablerow, 5, PyQt6.QtWidgets.QTableWidgetItem(filier))
                self.table.setItem(tablerow, 6, PyQt6.QtWidgets.QTableWidgetItem(nom_arabic))
                self.table.setItem(tablerow, 7, PyQt6.QtWidgets.QTableWidgetItem(prenom_arabic))
                self.table.setItem(tablerow, 8, PyQt6.QtWidgets.QTableWidgetItem(nom_french))
                self.table.setItem(tablerow, 9, PyQt6.QtWidgets.QTableWidgetItem(prenom_french))
                self.table.setItem(tablerow, 10, PyQt6.QtWidgets.QTableWidgetItem(annee_de_naisance))
                self.table.setItem(tablerow, 11, PyQt6.QtWidgets.QTableWidgetItem(lieu_naisance))
                self.table.setItem(tablerow, 12, PyQt6.QtWidgets.QTableWidgetItem(note))
                self.table.setItem(tablerow, 13, PyQt6.QtWidgets.QTableWidgetItem(annee_preparer))
                self.table.setItem(tablerow, 14, PyQt6.QtWidgets.QTableWidgetItem(annee_inscri))
                self.table.setItem(tablerow, 15, PyQt6.QtWidgets.QTableWidgetItem(departement))
                self.modifier = QPushButton('Modifier')
                self.delet = QPushButton('DELETE')
                self.modifier.clicked.connect(self.handelButton)
                self.delet.clicked.connect(self.handelButton)
                self.table.setCellWidget(tablerow, 16, self.modifier)
                self.table.setCellWidget(tablerow, 17, self.delet)
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
        self.title.setText("Diplome")
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(16)
        self.table.setHorizontalHeaderLabels(("Numero Inscription", "Domain", "Specialiter", "Filier", "Degree",
                                              "Nom (arabic)", "Prenom (arabic)", "Nom (french)", "Prenom (french)",
                                              "Annee De Naissance",
                                              "Lieu De Naissance", "Date Deliberations", "University", "Departement",
                                              "Modifier", "Delet"))
        self.table.verticalHeader().setDefaultSectionSize(10)
        self.table.horizontalHeader().setDefaultSectionSize(130)
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
                self.table.setItem(tablerow, 5, PyQt6.QtWidgets.QTableWidgetItem(nom_arabic))
                self.table.setItem(tablerow, 6, PyQt6.QtWidgets.QTableWidgetItem(prenom_arabic))
                self.table.setItem(tablerow, 7, PyQt6.QtWidgets.QTableWidgetItem(nom_french))
                self.table.setItem(tablerow, 8, PyQt6.QtWidgets.QTableWidgetItem(prenom_french))
                self.table.setItem(tablerow, 9, PyQt6.QtWidgets.QTableWidgetItem(annee_de_naisance))
                self.table.setItem(tablerow, 10, PyQt6.QtWidgets.QTableWidgetItem(lieu_naisance))
                self.table.setItem(tablerow, 11, PyQt6.QtWidgets.QTableWidgetItem(date_deleberation))
                self.table.setItem(tablerow, 12, PyQt6.QtWidgets.QTableWidgetItem(university))
                self.table.setItem(tablerow, 13, PyQt6.QtWidgets.QTableWidgetItem(departement))
                self.modifier = QPushButton('Modifier')
                self.delet = QPushButton('DELETE')
                self.modifier.clicked.connect(self.handelButton)
                self.delet.clicked.connect(self.handelButton)
                self.table.setCellWidget(tablerow, 14, self.modifier)
                self.table.setCellWidget(tablerow, 15, self.delet)
                tablerow += 1
        except mdb.Error as e:
            print("Failed to get record from MySQL table: {}".format(e))
        finally:
            if conn.is_connected():
                cur.close()
                conn.close()
                print('MySQL connection is closed ')

    def refresh(self):
        if self.stack == 0:
            self.showAdistation()
        elif self.stack == 1:
            self.showDiplome()

    def handelButton(self):
        if self.stack == 0:  # Adistation
            button = self.sender()
            index = self.table.indexAt(button.pos())
            if index.column() == 16:  # Modifier Student
                university = self.table.item(index.row(), 0).text()
                num_inscription = self.table.item(index.row(), 1).text()
                num_registre = self.table.item(index.row(), 2).text()
                specialiter = self.table.item(index.row(), 3).text()
                domain = self.table.item(index.row(), 4).text()
                filier = self.table.item(index.row(), 5).text()
                nom_arabic = self.table.item(index.row(), 6).text()
                prenom_arabic = self.table.item(index.row(), 7).text()
                nom_french = self.table.item(index.row(), 8).text()
                prenom_french = self.table.item(index.row(), 9).text()
                annee_de_naisance = str(self.table.item(index.row(), 10).text())
                lieu_naisance = self.table.item(index.row(), 11).text()
                note = self.table.item(index.row(), 12).text()
                annee_preparer = self.table.item(index.row(), 13).text()
                annee_inscri = self.table.item(index.row(), 14).text()
                departement = self.table.item(index.row(), 15).text()
                if self.Third is not None:
                    self.Third = None
                if self.Third is None:
                    from add_student import AddStudent
                    self.Third = AddStudent()
                    self.Third.var = 0
                    self.Third.id = num_inscription
                    self.Third.university.setText(university)
                    self.Third.specialiter.setText(specialiter)
                    self.Third.domain.setText(domain)
                    self.Third.filier.setText(filier)
                    self.Third.departement.setText(departement)
                    self.Third.numero_registrer.setText(num_registre)
                    self.Third.note.setText(note)
                    # self.Third.degree.setEnabled(False)
                    self.Third.nom_arabic.setText(nom_arabic)
                    self.Third.prenom_arabic.setText(prenom_arabic)
                    self.Third.lieuDeNaissance.setText(lieu_naisance)
                    self.Third.AnneePreparer.setText(annee_preparer)
                    self.Third.AnneeInscpription.setText(annee_inscri)
                    self.Third.nom_french.setText(nom_french)
                    self.Third.prenom_french.setText(prenom_french)
                    self.Third.date_naissance.setDate(PyQt6.QtCore.QDate.fromString(annee_de_naisance, "yyyy-MM-d"))
                    # self.Third.date_deleberation.setEnabled(False)
                    self.Third.show()
                    self.showAdistation()
            elif index.column() == 17:
                try:
                    conn = mdb.connect(host='localhost', user='root', password='root', database='bdd')
                    cur = conn.cursor()
                    id = self.table.item(index.row(), 1).text()
                    cur.execute("DELETE FROM student WHERE Num_Inscription={} ;".format(id))
                    conn.commit()
                    conn.commit()
                except mdb.Error as e:
                    print("Failed to get record from MySQL table: {}".format(e))
                finally:
                    if conn.is_connected():
                        cur.close()
                        conn.close()
                        print('MySQL connection is closed ')
                self.showAdistation()
        elif self.stack == 1:  # Diplome
            button = self.sender()
            index = self.table.indexAt(button.pos())
            if index.column() == 14:
                num_inscription = self.table.item(index.row(), 0).text()
                # num_registre = self.table.item(index.row(), 2).text()
                specialiter = self.table.item(index.row(), 2).text()
                domain = self.table.item(index.row(), 1).text()
                filier = self.table.item(index.row(), 3).text()
                degree = self.table.item(index.row(), 4).text()
                nom_arabic = self.table.item(index.row(), 5).text()
                prenom_arabic = self.table.item(index.row(), 6).text()
                nom_french = self.table.item(index.row(), 7).text()
                prenom_french = self.table.item(index.row(), 8).text()
                annee_de_naisance = str(self.table.item(index.row(), 9).text())
                lieu_naisance = self.table.item(index.row(), 10).text()
                # note = self.table.item(index.row(), 12).text()
                # annee_preparer = self.table.item(index.row(), 13).text()
                # annee_inscri = self.table.item(index.row(), 14).text()
                date_deleberation = self.table.item(index.row(), 11).text()
                university = self.table.item(index.row(), 12).text()
                departement = self.table.item(index.row(), 13).text()
                if self.Third is not None:
                    self.Third = None
                if self.Third is None:
                    from add_student import AddStudent
                    self.Third = AddStudent()
                    self.Third.var = 1
                    self.Third.id = num_inscription
                    self.Third.university.setText(university)
                    self.Third.specialiter.setText(specialiter)
                    self.Third.domain.setText(domain)
                    self.Third.filier.setText(filier)
                    self.Third.departement.setText(departement)
                    # self.Third.numero_registrer.setText(num_registre)
                    self.Third.numero_registrer.setEnabled(False)
                    self.Third.AnneePreparer.setEnabled(False)
                    # self.Third.note.setText(note)
                    self.Third.degree.setText(degree)
                    self.Third.note.setEnabled(False)
                    # self.Third.degree.setEnabled(False)
                    self.Third.nom_arabic.setText(nom_arabic)
                    self.Third.prenom_arabic.setText(prenom_arabic)
                    self.Third.lieuDeNaissance.setText(lieu_naisance)
                    # self.Third.AnneePreparer.setText(annee_preparer)
                    self.Third.AnneeInscpription.setEnabled(False)
                    # self.Third.AnneeInscpription.setText(annee_inscri)
                    self.Third.nom_french.setText(nom_french)
                    self.Third.prenom_french.setText(prenom_french)
                    self.Third.date_naissance.setDate(PyQt6.QtCore.QDate.fromString(annee_de_naisance, "yyyy-MM-d"))
                    self.Third.date_deleberation.setDate(PyQt6.QtCore.QDate.fromString(date_deleberation, "yyyy-MM-d"))
                    # self.Third.date_deleberation.setEnabled(False)
                    self.Third.show()
                    self.showAdistation()
            elif index.column() == 15:
                try:
                    conn = mdb.connect(host='localhost', user='root', password='root', database='bdd')
                    cur = conn.cursor()
                    id = self.table.item(index.row(), 0).text()
                    cur.execute("DELETE FROM student WHERE Num_Inscription={} ;".format(id))
                    conn.commit()
                    conn.commit()
                    self.showDiplome()
                except mdb.Error as e:
                    print("Failed to get record from MySQL table: {}".format(e))
                finally:
                    if conn.is_connected():
                        cur.close()
                        conn.close()
                        print('MySQL connection is closed ')

    def search(self):
        s = self.inputSearch.text()
        isInt = True
        try:
            int(s)
        except ValueError:
            isInt = False
        if self.stack == 0 and self.inputSearch.text() != '' and isInt:
            try:
                tablerow = 0
                conn = mdb.connect(host='localhost', user='root', password='root', database='bdd')
                cur = conn.cursor()
                cur.execute("SELECT COUNT(id) FROM adistation WHERE id LIKE %s ;",
                            ("%" + self.inputSearch.text() + "%",))
                self.table.setRowCount(cur.fetchone()[0])
                cur.execute("SELECT * FROM adistation;")
                result = cur.fetchall()
                for row in result:
                    num_inscription = str(row[0])
                    num_registre = str(row[1])
                    domain = str(row[2])
                    annee_preparer = str(row[3])
                    filier = str(row[4])
                    specialiter = str(row[5])
                    note = str(row[6])
                    nom = str(row[13])
                    prenom = str(row[14])
                    annee_de_naisance = str(row[9])
                    lieu_naisance = str(row[10])
                    annee_inscri = str(row[11])
                    university = str(row[12])
                    self.table.setItem(tablerow, 0, PyQt6.QtWidgets.QTableWidgetItem(university))
                    self.table.setItem(tablerow, 1, PyQt6.QtWidgets.QTableWidgetItem(specialiter))
                    self.table.setItem(tablerow, 2, PyQt6.QtWidgets.QTableWidgetItem(domain))
                    self.table.setItem(tablerow, 3, PyQt6.QtWidgets.QTableWidgetItem(filier))
                    self.table.setItem(tablerow, 4, PyQt6.QtWidgets.QTableWidgetItem(num_inscription))
                    self.table.setItem(tablerow, 5, PyQt6.QtWidgets.QTableWidgetItem(num_registre))
                    self.table.setItem(tablerow, 6, PyQt6.QtWidgets.QTableWidgetItem(note))
                    self.table.setItem(tablerow, 7, PyQt6.QtWidgets.QTableWidgetItem(nom))
                    self.table.setItem(tablerow, 8, PyQt6.QtWidgets.QTableWidgetItem(prenom))
                    self.table.setItem(tablerow, 9, PyQt6.QtWidgets.QTableWidgetItem(annee_de_naisance))
                    self.table.setItem(tablerow, 10, PyQt6.QtWidgets.QTableWidgetItem(lieu_naisance))
                    self.table.setItem(tablerow, 11, PyQt6.QtWidgets.QTableWidgetItem(annee_preparer))
                    self.table.setItem(tablerow, 12, PyQt6.QtWidgets.QTableWidgetItem(annee_inscri))
                    self.modifier = QPushButton('Modifier')
                    self.delet = QPushButton('DELETE')
                    self.modifier.clicked.connect(self.handelButton)
                    self.delet.clicked.connect(self.handelButton)
                    self.table.setCellWidget(tablerow, 13, self.modifier)
                    self.table.setCellWidget(tablerow, 14, self.delet)
                    tablerow += 1
            except mdb.Error as e:
                print("Failed to get record from MySQL table: {}".format(e))
            finally:
                if conn.is_connected():
                    cur.close()
                    conn.close()
                    print('MySQL connection is closed ')
        if self.stack == 1 and self.inputSearch.text() != '' and isInt:
            try:
                tablerow = 0
                conn = mdb.connect(host='localhost', user='root', password='root', database='bdd')
                cur = conn.cursor()
                cur.execute("SELECT COUNT(id) FROM adistation WHERE id LIKE %s ;",
                            ("%" + self.inputSearch.text() + "%",))
                self.table2.setRowCount(cur.fetchone()[0])
                cur.execute("SELECT * FROM adistation;")
                result = cur.fetchall()
                for row in result:
                    pass

            except mdb.Error as e:
                print("Failed to get record from MySQL table: {}".format(e))

            finally:
                if conn.is_connected():
                    cur.close()
                    conn.close()
                    print('MySQL connection is closed ')

    def addStudent(self):
        if self.stack == 0:
            if self.Third != None:
                self.Third = None
            if self.Third is None:
                from add_student import AddStudent
                self.Third = AddStudent()
                self.Third.degree.setEnabled(False)
                self.Third.note.setEnabled(False)
                self.Third.date_deleberation.setEnabled(False)
                self.Third.show()

    def printpdf(self):
        from print_pdf import PrintPdf
        self.window = PrintPdf()
        self.window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = DataBasse()
    myapp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('clossing window')
