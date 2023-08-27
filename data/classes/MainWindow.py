import sqlite3
from data.ui.main_window import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog
from PyQt6.QtGui import QFont, QPalette, QColor, QBrush, QIcon, QPixmap
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from data.classes.Option import Option
from data.classes.Level import Level
from data.classes.AuthorisationDialog import Autorisation_Dialog
from data.classes.WrongLogin import Wrong_Login
from data.classes.TextGenerator import Text_Generator
from data.classes.ExitDialog import Exit_Dialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        pxm = QPixmap('data/pictures/gus2.png')
        self.icon = QIcon(pxm)
        self.setWindowIcon(self.icon)

        self.text = ''
        self.con = sqlite3.connect('data/accounts.db')
        self.cur = self.con.cursor()
        self.authorization()
        self.font = QFont()
        self.font_output = QFont()
        self.start_settings()

        self.back_to_main_button = QPushButton('Назад в\nглавное меню', self)
        self.font.setPointSize(12)
        self.back_to_main_button.setFont(self.font)
        self.back_to_main_button.resize(120, 60)
        self.back_to_main_button.move(50, 50)
        self.back_to_main_button.hide()
        self.back_to_main_button.clicked.connect(self.back_to_main)

        self.font.setPointSize(30)
        self.level_buttons = []
        for level_number in range(1, 11):
            button = QPushButton(f'{level_number}', self)
            button.setFont(self.font)
            button.resize(150, 150)
            button.move(105 + 160 * ((level_number - 1) % 5), 235 + 160 * ((level_number - 1) // 5))
            button.hide()
            button.clicked.connect(self.load_level)
            self.level_buttons.append(button)

        self.font.setPointSize(40)
        self.level_select_label = QLabel(self)
        self.level_select_label.setText('Выберите уровень:')
        self.level_select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.level_select_label.setFont(self.font)
        self.level_select_label.resize(self.level_select_label.sizeHint())
        self.level_select_label.move(265, 100)
        self.level_select_label.hide()
        self.current_level = self.cur.execute(f'''SELECT level 
                                                  FROM login_password WHERE login = ?''',
                                              (self.login, )).fetchall()[0][0]
        if self.current_level < 4:
            self.select_text_button.setEnabled(False)
        if self.current_level < 7:
            self.random_text_button.setEnabled(False)
        for level_number in range(10):
            if int(self.level_buttons[level_number].text()) > self.current_level:
                self.level_buttons[level_number].setEnabled(False)
        self.show()
        self.exit_button.clicked.connect(self.exit)
        self.level_selection_button.clicked.connect(self.level_selection)
        self.select_text_button.clicked.connect(self.load_level)
        self.back_to_main_button.clicked.connect(self.back_to_main)
        self.settings_button.clicked.connect(self.option_show)
        self.random_text_button.clicked.connect(self.generation_text)

    def start_settings(self):
        self.font_name, self.font_color, self.font_correct_color, self.font_wrong_color, \
        self.input_field_color, self.sound_wrong_input_bool, self.sound_wrong_input_name, \
        self.sound_menu_bool, \
        self.sound_menu_name = self.cur.execute('SELECT * FROM options WHERE id = ('
                                                  'SELECT id FROM login_password '
                                                  'WHERE login = ?)',
                                                (self.login, )).fetchall()[0][1:]
        self.font_color = list(map(int, self.font_color.split()))
        self.input_field_color = list(map(int, self.input_field_color.split()))
        self.input_window = Level(self)
        self.option = Option(self)
        self.accept_settings()

    def accept_settings(self):
        self.settings = {'font_name': self.font_name,
                         'font_color': ' '.join(list(map(str, self.font_color))),
                         'font_correct_color': self.font_correct_color,
                         'font_wrong_color': self.font_wrong_color,
                         'input_field_color': ' '.join(list(map(str, self.input_field_color))),
                         'sound_wrong_input_bool': self.sound_wrong_input_bool,
                         'sound_wrong_input_name': self.sound_wrong_input_name,
                         'sound_menu_bool': self.sound_menu_bool,
                         'sound_menu_name': self.sound_menu_name,
                         }

        for name_settings in self.settings.keys():
            self.cur.execute(f'''UPDATE options 
                                 SET {name_settings} = ?
                                 WHERE id = (SELECT id FROM login_password WHERE login = ?)''',
                             (self.settings[name_settings], self.login))
            self.con.commit()
        self.font_output.setFamily(self.font_name)
        palette = QPalette()
        brush = QBrush(QColor(self.font_color[0], self.font_color[1], self.font_color[2]))
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)
        brush = QBrush(QColor(self.input_field_color[0], self.input_field_color[1],
                              self.input_field_color[2]))
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        self.input_window.output.setFont(self.font_output)
        self.input_window.output.setPalette(palette)

        self.sound_buttons = QSoundEffect()
        self.sound_buttons.setSource(QUrl.fromLocalFile(f'data/sounds/buttons/{self.sound_menu_name}.wav'))

        self.wrong_sound = QSoundEffect()
        self.wrong_sound.setSource(QUrl.fromLocalFile(f'data/sounds/input/wrong/{self.sound_wrong_input_name}.wav'))

        self.option.font_select_comboBox.setCurrentText(self.font_name)
        self.option.sound_wrong_input_checkBox.setChecked(self.sound_wrong_input_bool)
        self.option.sound_wrong_input_comboBox.setCurrentText(self.sound_wrong_input_name)
        self.option.sound_menu_checkBox.setChecked(self.sound_menu_bool)
        self.option.sound_menu_comboBox.setCurrentText(self.sound_menu_name)
        self.option.sound_menu_comboBox.textActivated.connect(self.option.preview_play)
        self.option.sound_wrong_input_comboBox.textActivated.connect(self.option.preview_play)

    def authorization(self):
        self.login = ''
        self.password = ''
        while True:
            dlg = Autorisation_Dialog(self)
            dlg.exec()
            self.con.commit()
            logins = list(map(lambda x: (str(x[1]), str(x[2])),
                              self.cur.execute("""SELECT * FROM login_password""").fetchall()))
            if (self.login, self.password) in logins:
                break
            else:
                wrong_dialog = Wrong_Login('Неправильный логин или пароль')
                wrong_dialog.exec()

    def level_selection(self):
        if self.sound_menu_bool:
            self.sound_buttons.play()
        self.title_label.hide()
        self.back_to_main_button.show()
        for main_button in self.main_buttonGroup.buttons():
            main_button.hide()
        for level_button in self.level_buttons:
            level_button.show()
        self.level_select_label.show()

    def generation_text(self):
        if self.sound_menu_bool:
            self.sound_buttons.play()
        self.dialog = Text_Generator(self)
        self.dialog.show()

    def load_level(self):
        if self.sender().__class__.__name__ == 'QPushButton':
            if self.sound_menu_bool:
                self.sound_buttons.play()
            if self.sender().objectName() == 'select_text_button':
                self.fname = QFileDialog.getOpenFileName(self, 'Выбрать текст', '',
                                                         'Текст(*.txt)')[0]
            else:
                self.fname = f'level{self.sender().text()}'
            if self.fname:
                self.input_window.show()
                self.input_window.load(self.sender(), self.fname)
                self.hide()

    def exit(self):
        if self.sound_menu_bool:
            self.sound_buttons.play()
        dialog = Exit_Dialog(self)
        dialog.exec()

    def back_to_main(self):
        if self.sound_menu_bool:
            self.sound_buttons.play()
        for level_button in self.level_buttons:
            level_button.hide()
        self.level_select_label.hide()
        self.title_label.show()
        self.back_to_main_button.hide()
        for main_button in self.main_buttonGroup.buttons():
            main_button.show()

    def option_show(self):
        if self.sound_menu_bool:
            self.sound_buttons.play()
        self.option.show()

