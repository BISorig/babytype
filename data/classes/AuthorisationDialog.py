from data.ui.autorisation_dialog import Ui_Autorisation_Dialog
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIcon, QPixmap
from data.classes.WrongLogin import Wrong_Login
import sys


class Autorisation_Dialog(QDialog, Ui_Autorisation_Dialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        pxm = QPixmap('data/pictures/gus2.png')
        self.icon = QIcon(pxm)
        self.setWindowIcon(self.icon)

        self.dialog_buttonBox.buttons()[1].setText('Отмена')
        self.dialog_buttonBox.buttons()[0].setEnabled(False)
        self.registration_button.setEnabled(False)

        self.login_lineEdit.textChanged.connect(self.enable)
        self.password_lineEdit.textChanged.connect(self.enable)

        self.dialog_buttonBox.accepted.connect(self.main_show)
        self.dialog_buttonBox.rejected.connect(sys.exit)
        self.registration_button.clicked.connect(self.registration)

    def enable(self):
        if self.login_lineEdit.text() and self.password_lineEdit.text():
            self.dialog_buttonBox.buttons()[0].setEnabled(True)
            self.registration_button.setEnabled(True)
        else:
            self.dialog_buttonBox.buttons()[0].setEnabled(False)
            self.registration_button.setEnabled(False)

    def main_show(self):
        self.main_window.login = str(self.login_lineEdit.text())
        self.main_window.password = str(self.password_lineEdit.text())

    def registration(self):
        logins = list(map(lambda x: str(x[0]),
                          self.main_window.cur.execute("""SELECT login FROM
                          login_password""").fetchall()))
        if self.login_lineEdit.text() in logins:
            wrong_dialog = Wrong_Login('Логин уже занят')
            wrong_dialog.exec()
        else:
            self.main_window.cur.execute(
                f"INSERT INTO login_password(login, password, level, first_entry)"
                f"VALUES(?, ?, 1, 0)",
                (self.login_lineEdit.text(), self.password_lineEdit.text()))
            self.main_window.con.commit()

    def closeEvent(self, event):
        sys.exit()
