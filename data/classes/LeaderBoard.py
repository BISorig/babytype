from data.ui.leaderboard import Ui_Leaderboard
from PyQt6.QtWidgets import QDialog, QTableWidgetItem
from PyQt6.QtGui import QIcon, QPixmap


class Leaderboard(QDialog, Ui_Leaderboard):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUi(self)
        pxm = QPixmap('data/pictures/gus2.png')
        self.icon = QIcon(pxm)
        self.setWindowIcon(self.icon)
        self.setWindowTitle('Таблица результатов')
        self.initUI()
        self.leade_buttonBox.accepted.connect(self.close)

    def initUI(self):
        data = self.main_window.cur.execute(
            f'''SELECT login, {self.main_window.fname} 
                FROM login_password, points WHERE login_password.id = points.id''').fetchall()
        data = list(filter(lambda x: x[1] != '0:00', data))
        data.sort(key=lambda x: list(map(float, x[1].split(':')))[0] * 60 +
                                list(map(float, x[1].split(':')))[1])
        self.leader_table.setColumnCount(2)
        self.leader_table.setRowCount(0)
        for i, row in enumerate(data):
            self.leader_table.setRowCount(self.leader_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.leader_table.setItem(i, j, QTableWidgetItem(str(elem)))