from data.ui.exit_dialog import Ui_Exit_Dialog
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIcon, QPixmap
import sys



class Exit_Dialog(QDialog, Ui_Exit_Dialog):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        self.setWindowTitle('Выход')
        self.initUI()

    def initUI(self):
        pxm = QPixmap('data/pictures/gus2.png')
        self.icon = QIcon(pxm)
        self.setWindowIcon(self.icon)
        self.exit_dialog_buttonBox.buttons()[0].setText('Да')
        self.exit_dialog_buttonBox.buttons()[1].setText('Нет')
        self.exit_dialog_buttonBox.accepted.connect(sys.exit)
        self.exit_dialog_buttonBox.rejected.connect(self.close_dlg)

    def close_dlg(self):
        if self.main_window.sound_menu_bool:
            self.main_window.sound_buttons.play()
        self.close()