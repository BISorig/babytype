from data.ui.level import Ui_Level
from data.classes.LeaderBoard import Leaderboard
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QTextOption, QIcon, QPixmap
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt
from data.classes.HiWindow import Hi_Window


class Level(QWidget, Ui_Level):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUi(self)
        self.setWindowTitle('Baby Tape Lite')
        self.initUI()

    def initUI(self):
        pxm = QPixmap('data/pictures/gus2.png')
        self.icon = QIcon(pxm)
        self.setWindowIcon(self.icon)
        self.main_label = QLabel(self)
        self.main_label.resize(1000, 700)
        self.main_label.setPixmap(QPixmap('data/pictures/gusi.jpg'))
        self.main_label.move(0, 0)
        self.main_label.lower()
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_timer)
        self.output.hide()
        self.input.hide()
        self.output.setReadOnly(True)
        self.input.textChanged.connect(self.run)
        self.start_button.clicked.connect(self.start)
        self.leader_button.clicked.connect(self.leader_show)
        self.txt_opt = QTextOption()
        self.output.setWordWrapMode(self.txt_opt.WrapMode.WrapAnywhere)
        self.len_page = 460

    def leader_show(self):
        if self.main_window.sound_menu_bool:
            self.main_window.sound_buttons.play()
        dialog_table = Leaderboard(self.main_window)
        dialog_table.exec()

    def load(self, sender, fname):
        self.fname = fname
        if sender.text() == '1':
            self.main_label.show()
        else:
            self.main_label.hide()
        self.sender_name = sender.objectName()
        if self.sender_name in ['select_text_button', 'accept_button']:
            self.leader_button.hide()
            self.back_to_main_button.setText('Назад в\nглавное меню')
            self.back_to_main_button.clicked.connect(self.back_to_main)
            if self.sender_name == 'select_text_button':
                with open(self.fname, 'r', encoding='utf-8') as txt:
                    self.text = txt.read()
        else:
            self.leader_button.show()
            self.back_to_main_button.setText('Назад в меню\nвыбора уровня')
            self.back_to_main_button.clicked.connect(self.back_to_level_selection)
            self.leader_button.show()
            with open(f'data/levels/{self.fname}.txt', 'r', encoding='utf-8') as txt:
                self.text = txt.read()

        self.count_pages = len(self.text) // self.len_page + 1
        self.start_button.show()
        self.back_to_main_button.show()
        first_entry = self.main_window.cur.execute(f"""SELECT first_entry FROM login_password 
                                                       WHERE login = ?""",
                                                   (self.main_window.login, )).fetchall()[0]
        if first_entry[0] == 0:
            dialog = Hi_Window()
            dialog.exec()
            self.main_window.cur.execute(f"""UPDATE login_password
                                             SET first_entry = 1
                                             WHERE login = ?""", (self.main_window.login, ))
            self.main_window.con.commit()

        self.pr_text = ''
        self.output.setEnabled(False)
        self.count_error = 0
        self.fl_countdown = True
        self.sec = 5
        self.min = 0
        self.symbol = 0

    def start(self):
        if self.main_window.sound_menu_bool:
            self.main_window.sound_buttons.play()
        self.text2 = ''
        self.page = 1
        self.count_sym = 0
        self.len_text = len(self.text)
        self.start_button.hide()
        self.page_number_label.show()
        self.output.show()
        self.timer.start(3)

    def show_timer(self):
        if self.symbol != self.len_text:
            if self.symbol % self.len_page == 0:
                self.output.clear()
                self.text2 = ''
                self.page_number_label.setText(f'{self.symbol // self.len_page + 1} / {self.count_pages}')
            self.text2 += self.text[self.symbol]
            self.output.setText(f'<font size = "10">{self.text2}</font>')
            if self.symbol == len(self.text) - 1:
                self.timer.stop()
                self.timer.start(1000)
            self.symbol += 1
        else:
            if self.fl_countdown:
                if self.sec == 5:
                    self.output.setText(f'<font size = "10">{self.text[:self.len_page]}</font>')
                    self.page_number_label.setText(f'1 / {self.count_pages}')
                if self.sec == 0:
                    self.time_label.setText('Печатайте!')
                    self.output.setEnabled(True)
                    self.input.grabKeyboard()
                else:
                    self.time_label.setText(str(self.sec))
                self.sec -= 1
                if self.sec == -1:
                    self.fl_countdown = False
                    self.timer.stop()
                    self.timer.start(100)
                    self.sec += 1
            else:
                self.input.grabKeyboard()
                if self.sec < 60 and self.min == 0:
                    if self.sec > 2:
                        self.time_label.setText(str(self.sec) + f'\nКоличество ошибок: {self.count_error}'
                                                f'\nСкорость: {round(self.count_sym / (self.sec / 60 + self.min), 1)}')
                    self.sec += 0.1
                    self.sec = round(self.sec, 1)
                else:
                    self.timer.stop()
                    self.timer.start(1000)
                    self.min += self.sec // 60
                    self.sec %= 60
                    self.time_label.setText(f'{int(self.min)}:{str(int(self.sec)).rjust(2, "0")}\nКоличество ошибок: {self.count_error}'
                                                f'\nСкорость: {round(self.count_sym / (self.sec / 60 + self.min), 1)}')
                    self.sec += 1

    def run(self):
        if self.input.toPlainText() and self.output.toPlainText():
            if self.input.toPlainText()[-1] == self.text[0]:
                if self.text[0] == ' ':
                    self.pr_text += '_'
                else:
                    self.pr_text += self.input.toPlainText()[-1]
                self.count_sym += 1
                self.text = self.text[1:]
                self.output.setText(
                    f'<font size = 10><font color = '
                    f'{self.main_window.font_correct_color}>{self.pr_text}</font>'
                    f'{self.text[:self.len_page - len(self.pr_text)]}</font>')
                self.input.clear()
                if len(self.pr_text) == self.len_page:
                    self.pr_text = ''
                    self.page += 1
                    self.output.setText(f'<font size = 10>{self.text[:self.len_page]}</font>')
                    self.page_number_label.setText(f'{self.page} / {self.count_pages}')
            elif self.text[0] == ' ':
                if self.main_window.sound_wrong_input_bool:
                    self.main_window.wrong_sound.play()
                self.output.setText(
                    f'<font size = 10><font color = '
                    f'{self.main_window.font_correct_color}>{self.pr_text}'
                    f'</font><font color = {self.main_window.font_wrong_color}>_</font>'
                    f'{self.text[1:self.len_page - len(self.pr_text)]}</font>')
                self.count_error += 1
            else:
                if self.main_window.sound_wrong_input_bool:
                    self.main_window.wrong_sound.play()
                self.output.setText(
                    f'<font size = 10><font color = '
                    f'{self.main_window.font_correct_color}>{self.pr_text}'
                    f'</font><font color = {self.main_window.font_wrong_color}>'
                    f'{self.text[0]}</font>'
                    f'{self.text[1:self.len_page - len(self.pr_text)]}</font>')
                self.count_error += 1

            if self.text == '':
                self.timer.stop()
                self.input.releaseKeyboard()
                self.time_label.setText(f'Финиш!\nВремя: {self.min} мин. {self.sec} сек.\n'
                                        f'Количество ошибок: {self.count_error}\n' 
                                        f' Скорость: {round(self.count_sym / (self.sec / 60 + self.min), 1)} с/м')
                if self.sender_name not in ['select_text_button', 'accept_button']:
                    points_level = \
                        self.main_window.cur.execute(f'''SELECT {self.fname} FROM points
                                                         INNER JOIN login_password
                                                         ON points.id = login_password.id
                                                         WHERE login_password.login = ?''',
                                                         (self.main_window.login, )
                                                     ).fetchall()[0][0].split(':')
                    points_level = sum(list(map(float, points_level)))
                    self.points = self.min * 60 + self.sec
                    if self.points < points_level or points_level == 0:
                        self.str_points = f'{int(self.points // 60)}:{self.points % 60}'
                        self.main_window.cur.execute(f'''UPDATE points SET {self.fname} = ?
                                                         WHERE points.id = 
                                                         (SELECT id FROM login_password 
                                                          WHERE login_password.login = ?)''',
                                                     (self.str_points, self.main_window.login))
                    if self.fname[-1] != 0:
                        if self.points and \
                                not self.main_window.level_buttons[int(self.fname[-1])].isEnabled():
                            self.main_window.cur.execute(f"""UPDATE login_password
                                                             SET level = {int(self.fname[-1]) + 1}
                                                             WHERE login = ?""",
                                                         (self.main_window.login, ))
                            self.main_window.level_buttons[int(self.fname[-1])].setEnabled(True)
                    self.main_window.con.commit()
                    if self.fname[-1] == '3':
                        self.main_window.select_text_button.setEnabled(True)
                    elif self.fname[-1] == '6':
                        self.main_window.select_text_button.setEnabled(True)

    def back_to_level_selection(self):
        self.timer.stop()
        self.input.releaseKeyboard()
        for main_button in self.main_window.main_buttonGroup.buttons():
            main_button.hide()
        self.main_window.title_label.hide()
        for level_button in self.main_window.level_buttons:
            level_button.show()
        self.main_window.level_select_label.show()
        self.main_window.show()
        self.time_label.clear()
        self.page_number_label.hide()
        self.output.clear()
        self.output.hide()
        # if self.main_window.sound_menu_bool:
        #     self.main_window.sound_buttons.play()
        self.close()


    def back_to_main(self):
        if self.main_window.sound_menu_bool:
            self.main_window.sound_buttons.play()
        self.timer.stop()
        self.time_label.clear()
        self.page_number_label.hide()
        self.output.hide()
        self.output.clear()
        for level_button in self.main_window.level_buttons:
            level_button.hide()
        self.main_window.level_select_label.hide()
        self.main_window.title_label.show()
        self.back_to_main_button.hide()
        for main_button in self.main_window.main_buttonGroup.buttons():
            main_button.show()
        self.main_window.show()
        self.close()