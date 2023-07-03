import sys
from PyQt6.QtGui import QIntValidator
from PyQt6.uic.load_ui import loadUi
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QApplication, QPushButton, QDateEdit, QMessageBox
import mysql.connector as mdb
from datetime import date


class AddStudent(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI/addstudent.ui", self)
        self.var = -1
        self.id = -1
        self.university = self.findChild(QLineEdit, 'University')
        self.specialiter = self.findChild(QLineEdit, 'specialiter')
        self.domain = self.findChild(QLineEdit, 'domain')
        self.filier = self.findChild(QLineEdit, 'filier')
        self.departement = self.findChild(QLineEdit, 'Departement')
        self.numero_registrer = self.findChild(QLineEdit, 'NumeroRegistrer')
        self.note = self.findChild(QLineEdit, 'note')
        self.degree = self.findChild(QLineEdit, 'Degree')
        self.nom_arabic = self.findChild(QLineEdit, 'nom_arabic')
        self.prenom_arabic = self.findChild(QLineEdit, 'prenom_arabic')
        self.lieuDeNaissance = self.findChild(QLineEdit, 'lieuDeNaissance')
        self.AnneePreparer = self.findChild(QLineEdit, 'AnneePreparer')
        self.AnneeInscpription = self.findChild(QLineEdit, 'AnneeInscpription')
        self.nom_french = self.findChild(QLineEdit, 'nom_french')
        self.prenom_french = self.findChild(QLineEdit, 'prenom_french')
        self.date_naissance = self.findChild(QDateEdit, 'anneeDeNaissance')
        self.date_deleberation = self.findChild(QDateEdit, 'DateDeleberation')
        self.date_naissance.setDate(date.today())
        self.date_naissance.setDisplayFormat("yyyy-MM-d")
        self.date_deleberation.setDate(date.today())
        self.date_deleberation.setDisplayFormat("yyyy-MM-d")
        self.submit = self.findChild(QPushButton, 'submit')
        self.submit.clicked.connect(self.addstudent)
        # self.annee.setValidator(QIntValidator())

    def addstudent(self):
        university = self.university.text()
        specialiter = self.specialiter.text()
        domain = self.domain.text()
        filier = self.filier.text()  # Null
        departement = self.departement.text()
        numero_registrer = self.numero_registrer.text()
        note = self.note.text()  # Null
        degree = self.degree.text()  # Null
        nom_arabic = self.nom_arabic.text()
        prenom_arabic = self.prenom_arabic.text()
        nom_french = self.nom_french.text()
        prenom_french = self.prenom_french.text()
        lieuDeNaissance = self.lieuDeNaissance.text()
        AnneePreparer = self.AnneePreparer.text()
        AnneeInscpription = self.AnneeInscpription.text()
        date_naissance = self.date_naissance
        date_deleberation = self.date_deleberation  # Null
        if self.id == -1:  ## when we want to add a new student
            if university == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("University est Vide")
                dlg.exec()
            elif domain == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("Domain  est Vide")
                dlg.exec()
            elif specialiter == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("Specialiter est Vide")
                dlg.exec()
            elif nom_arabic == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("Le Nom (Arabic) est Vide")
                dlg.exec()
            elif prenom_arabic == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("Le Prenom (Arabic) est Vide")
                dlg.exec()
            elif nom_french == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("Le Nom (French) est Vide")
                dlg.exec()
            elif prenom_french == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("Le Prenom (French) est Vide")
                dlg.exec()
            elif departement == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("Le Departement est Vide")
                dlg.exec()
            elif date_naissance.date().toPyDate() >= date.today():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("Le Date De Naissance est superieur ou egale la date de jour")
                dlg.exec()
            elif lieuDeNaissance == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("Le Lieu De Naissance est Vide")
                dlg.exec()
            elif AnneePreparer == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("L'Annee Preparer est Vide")
                dlg.exec()
            elif AnneeInscpription == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("L'Annee Inscpription est Vide")
                dlg.exec()
            elif numero_registrer == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("Le Numero De Registrer est Vide")
                dlg.exec()
            else:
                try:
                    conn = mdb.connect(host='localhost', user='root', password='root', database='bdd')
                    cur = conn.cursor()

                    query = """INSERT INTO student (University,Num_Registre,Specialiter,Domain,Filier,
                            First_Name_Arabic,Second_Name_Arabic,First_Name_French,Second_Name_French,Birthday,
                            Birth_Place,Annee_Preparer,Annee_Inscri_Officiel,Departement) VALUE(%s,%s,%s,%s,%s,%s,
                            %s,%s,%s,%s,%s,%s,%s,%s); """
                    record = (
                        university, numero_registrer, specialiter, domain, filier, nom_arabic, prenom_arabic,
                        nom_french, prenom_french, date_naissance.date().toPyDate(), lieuDeNaissance,
                        AnneePreparer,
                        AnneeInscpription, departement
                    )
                    cur.execute(query, record)
                    conn.commit()
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("congratulation")
                    dlg.setText("L'Etudient a ete ajouter successfully")
                    dlg.exec()
                    self.university.setText("")
                    self.specialiter.setText("")
                    self.domain.setText("")
                    self.filier.setText("")
                    self.departement.setText("")
                    self.numero_registrer.setText("")
                    self.nom_arabic.setText("")
                    self.prenom_arabic.setText("")
                    self.nom_french.setText("")
                    self.prenom_french.setText("")
                    self.lieuDeNaissance.setText("")
                    self.AnneePreparer.setText("")
                    self.AnneeInscpription.setText("")
                    date_naissance.setDate(date.today())
                    date_deleberation.setDate(date.today())
                except mdb.Error as e:
                    print("Failed to get record from MySQL table: {}".format(e))
                finally:
                    if conn.is_connected():
                        cur.close()
                        conn.close()
                        print('MySQL connection is closed ')
        else:  # When we want to Update an student
            try:
                conn = mdb.connect(host='localhost', user='root', password='root', database='bdd')
                cur = conn.cursor()
                if self.var == 0 and degree == "":  ##Update The Adistation Info
                    query = """UPDATE student SET University=%s,Num_Registre=%s,Specialiter=%s,Domain=%s,Filier=%s,
                            First_Name_Arabic=%s,Second_Name_Arabic=%s,First_Name_French=%s,Second_Name_French=%s,
                            Birthday=%s ,Birth_Place=%s,Note=%s,Annee_Preparer=%s,Annee_Inscri_Officiel=%s WHERE 
                            Num_Inscription=%s; """
                    record = (
                        university, numero_registrer, specialiter, domain, filier, nom_arabic, prenom_arabic,
                        nom_french,
                        prenom_french, date_naissance.date().toPyDate(), lieuDeNaissance, note, AnneePreparer,
                        AnneeInscpription, int(self.id)
                    )
                elif self.var == 0 and degree != "":
                    query = """UPDATE student SET University=%s,Num_Registre=%s,Specialiter=%s,Domain=%s,Filier=%s,
                                                First_Name_Arabic=%s,Second_Name_Arabic=%s,First_Name_French=%s,Second_Name_French=%s,
                                                Birthday=%s ,Birth_Place=%s,Note=%s,Annee_Preparer=%s,Annee_Inscri_Officiel=%s,
                                                Date_Deliberations=%s,Degree=%s WHERE 
                                                Num_Inscription=%s; """
                    record = (
                        university, numero_registrer, specialiter, domain, filier, nom_arabic, prenom_arabic,
                        nom_french,
                        prenom_french, date_naissance.date().toPyDate(), lieuDeNaissance, note, AnneePreparer,
                        AnneeInscpription, date_deleberation.date().toPyDate(), degree, int(self.id)
                    )
                elif self.var == 1:  # Update The Diplom Info
                    query = """UPDATE student SET University=%s,Specialiter=%s,Domain=%s,Filier=%s, 
                            First_Name_Arabic=%s,Second_Name_Arabic=%s,First_Name_French=%s,Second_Name_French=%s,
                            Birthday=%s ,Birth_Place=%s, 
                            Degree=%s,Date_Deliberations=%s WHERE 
                            Num_Inscription=%s; """
                    record = (
                        university, specialiter, domain, filier, nom_arabic, prenom_arabic,
                        nom_french,
                        prenom_french, date_naissance.date().toPyDate(), lieuDeNaissance,
                        degree, date_deleberation.date().toPyDate(), int(self.id)
                    )
                cur.execute(query, record)
                conn.commit()
                dlg = QMessageBox(self)
                dlg.setWindowTitle("congratulation")
                dlg.setText("L'Etudient a ete Modifier successfully")
                dlg.exec()
                self.close()
            except mdb.Error as e:
                print("Failed to get record from MySQL table: {}".format(e))
            finally:
                if conn.is_connected():
                    cur.close()
                    conn.close()
                    print('MySQL connection is closed ')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = AddStudent()
    myapp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('clossing window')
