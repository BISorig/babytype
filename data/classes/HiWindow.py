from data.ui.hi_window import Ui_Hi_Window
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIcon, QPixmap


class Hi_Window(QDialog, Ui_Hi_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        pxm = QPixmap('data/pictures/gus2.png')
        self.icon = QIcon(pxm)
        self.setWindowIcon(self.icon)
        self.setWindowTitle('Приветствие')
        self.hi_buttonBox.accepted.connect(self.close)