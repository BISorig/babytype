# Form implementation generated from reading ui file 'leaderboard.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Leaderboard(object):
    def setupUi(self, Leaderboard):
        Leaderboard.setObjectName("Leaderboard")
        Leaderboard.resize(597, 613)
        self.leade_buttonBox = QtWidgets.QDialogButtonBox(parent=Leaderboard)
        self.leade_buttonBox.setGeometry(QtCore.QRect(130, 560, 341, 32))
        self.leade_buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.leade_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.leade_buttonBox.setCenterButtons(True)
        self.leade_buttonBox.setObjectName("leade_buttonBox")
        self.leader_table = QtWidgets.QTableWidget(parent=Leaderboard)
        self.leader_table.setGeometry(QtCore.QRect(30, 20, 541, 531))
        self.leader_table.setObjectName("leader_table")
        self.leader_table.setColumnCount(0)
        self.leader_table.setRowCount(0)

        self.retranslateUi(Leaderboard)
        self.leade_buttonBox.accepted.connect(Leaderboard.accept) # type: ignore
        self.leade_buttonBox.rejected.connect(Leaderboard.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Leaderboard)

    def retranslateUi(self, Leaderboard):
        _translate = QtCore.QCoreApplication.translate
        Leaderboard.setWindowTitle(_translate("Leaderboard", "Dialog"))
