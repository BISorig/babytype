import string
from random import choice

from data.ui.random_options import Ui_Random_Options
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon, QPixmap


class Text_Generator(QWidget, Ui_Random_Options):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUi(self)
        pxm = QPixmap('data/pictures/gus2.png')
        self.icon = QIcon(pxm)
        self.setWindowIcon(self.icon)
        self.accept_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.close_dlg)

    def accept(self):
        if self.main_window.sound_menu_bool:
            self.main_window.sound_buttons.play()
        self.lowercase_latin_letters = self.lowercase_latin_checkBox.isChecked()
        self.uppercase_latin_letters = self.uppercase_latin_checkBox.isChecked()
        self.lowercase_russian_letters = self.lowercase_russian_checkBox.isChecked()
        self.uppercase_russian_letters = self.uppercase_russian_checkBox.isChecked()
        self.digits = self.digit_checkBox.isChecked()
        self.punktuation = self.punctuation_checkBox.isChecked()
        self.count_symbols = int(self.count_symbols_spinBox.text())
        parameters = [self.lowercase_latin_letters, self.uppercase_latin_letters,
                      self.lowercase_russian_letters,
                     self.uppercase_russian_letters, self.digits, self.punktuation]
        if any(parameters) and self.count_symbols:
            self.all_symbols = ''
            if parameters[0]:
                self.all_symbols += string.ascii_lowercase
            if parameters[1]:
                self.all_symbols += string.ascii_uppercase
            if parameters[2]:
                self.all_symbols += ''.join([chr(i) for i in range(1072, 1104)])
            if parameters[3]:
                self.all_symbols += ''.join([chr(i) for i in range(1040, 1072)])
            if parameters[4]:
                self.all_symbols += string.digits
            if parameters[5]:
                for symbol in string.punctuation:
                    if symbol.isprintable():
                        self.all_symbols += symbol
            self.text = ''
            for i in range(self.count_symbols):
                self.text += choice(self.all_symbols)
            self.main_window.input_window.text = self.text
            self.main_window.load_level()
            self.close()
        elif not any(parameters) and self.count_symbols:
            self.error_label.setText('Необходимо выбрать\nхотя бы один\nнабор символов!')
        elif any(parameters) and not self.count_symbols:
            self.error_label.setText('Вы не указали\nколичество символов!')
        elif not any(parameters) and not self.count_symbols:
            self.error_label.setText('Необходимо указать\nколичество символов\nи хотя бы один'
                                     '\nнабор символов!')

    def close_dlg(self):
        if self.main_window.sound_menu_bool:
            self.main_window.sound_buttons.play()
        self.close()
