import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream
from data.classes.MainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    style_file = QFile('data/resource/myqss.qss')
    style_file.open(QFile.OpenModeFlag.ReadOnly)
    style = QTextStream(style_file)
    app.setStyleSheet(style.readAll())
    ex = MainWindow()
    sys.exit(app.exec())
