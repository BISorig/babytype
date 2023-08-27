from data.ui.wrong_login import Ui_Wrong_Login
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIcon, QPixmap


class Wrong_Login(QDialog, Ui_Wrong_Login):
    def __init__(self, message):
        super().__init__()
        self.setupUi(self)
        pxm = QPixmap('data/pictures/gus2.png')
        self.icon = QIcon(pxm)
        self.setWindowIcon(self.icon)
        self.setWindowTitle('Неверный ввод')
        self.label.setText(message)
        self.wrong_login_buttonBox.accepted.connect(self.close)