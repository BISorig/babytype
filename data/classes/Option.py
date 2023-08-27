from data.ui.option import Ui_Option
from PyQt6.QtWidgets import QWidget, QColorDialog
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl, Qt


class Option(QWidget, Ui_Option):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        pxm = QPixmap('data/pictures/gus2.png')
        self.icon = QIcon(pxm)
        self.setWindowIcon(self.icon)

        self.prev_sound = QSoundEffect()

        self.font_name = self.main_window.font_name
        self.font_color = self.main_window.font_color
        self.font_correct_color = self.main_window.font_correct_color
        self.font_wrong_color = self.main_window.font_wrong_color
        self.input_field_color = self.main_window.input_field_color
        self.sound_wrong_input_bool = self.main_window.sound_wrong_input_bool
        self.sound_wrong_input_name = self.main_window.sound_wrong_input_name
        self.sound_menu_bool = self.main_window.sound_menu_bool
        self.sound_menu_name = self.main_window.sound_menu_name

        self.font_color_button.clicked.connect(self.set_color)
        self.font_correct_color_button.clicked.connect(self.set_color)
        self.font_wrong_color_button.clicked.connect(self.set_color)
        self.input_field_color_button.clicked.connect(self.set_color)
        self.sound_menu_checkBox.stateChanged.connect(self.set_checkBox)
        self.sound_wrong_input_checkBox.stateChanged.connect(self.set_checkBox)
        self.accept_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.cancel)

    def preview_play(self):
        if self.sender() is self.sound_wrong_input_comboBox:
            if self.sound_wrong_input_bool:
                self.prev_sound.setSource(
                    QUrl.fromLocalFile(f'data/sounds/input/wrong/{self.sender().currentText()}.wav'))
                self.prev_sound.play()

        elif self.sender() is self.sound_menu_comboBox:
            if self.sound_menu_bool:
                self.prev_sound.setSource(
                    QUrl.fromLocalFile(f'data/sounds/buttons/{self.sender().currentText()}.wav'))
                self.prev_sound.play()

    def set_color(self):
        color = QColorDialog().getColor()
        if self.sender().objectName() == 'font_color_button':
            self.font_color = list(color.getRgb()[:-1])
        elif self.sender().objectName() == 'font_correct_color_button':
            self.font_correct_color = color.name()
        elif self.sender().objectName() == 'font_wrong_color_button':
            self.font_wrong_color = color.name()
        elif self.sender().objectName() == 'input_field_color_button':
            self.input_field_color = list(color.getRgb()[:-1])

    def set_checkBox(self):
        name = self.sender().objectName()
        if name == 'sound_menu_checkBox':
            self.sound_menu_bool = self.sound_menu_checkBox.isChecked()
        elif name == 'sound_wrong_input_checkBox':
            self.sound_wrong_input_bool = self.sound_wrong_input_checkBox.isChecked()

    def accept(self):
        if self.main_window.sound_menu_bool:
            self.main_window.sound_buttons.play()
        self.main_window.font_name = self.font_select_comboBox.currentText()
        self.main_window.font_color = self.font_color
        self.main_window.font_correct_color = self.font_correct_color
        self.main_window.font_wrong_color = self.font_wrong_color
        self.main_window.input_field_color = self.input_field_color
        self.main_window.sound_wrong_input_bool = self.sound_wrong_input_bool
        self.main_window.sound_wrong_input_name = self.sound_wrong_input_comboBox.currentText()
        self.main_window.sound_menu_bool = self.sound_menu_bool
        self.main_window.sound_menu_name = self.sound_menu_comboBox.currentText()
        self.main_window.accept_settings()
        self.main_window.start_settings()
        self.close()

    def cancel(self):
        if self.main_window.sound_menu_bool:
            self.main_window.sound_buttons.play()
        self.main_window.accept_settings()
        self.close()