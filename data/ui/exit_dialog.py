# Form implementation generated from reading ui file 'exit_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Exit_Dialog(object):
    def setupUi(self, Exit_Dialog):
        Exit_Dialog.setObjectName("Exit_Dialog")
        Exit_Dialog.resize(400, 190)
        self.exit_label = QtWidgets.QLabel(parent=Exit_Dialog)
        self.exit_label.setGeometry(QtCore.QRect(0, 20, 401, 81))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.exit_label.setFont(font)
        self.exit_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.exit_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.exit_label.setObjectName("exit_label")
        self.exit_dialog_buttonBox = QtWidgets.QDialogButtonBox(parent=Exit_Dialog)
        self.exit_dialog_buttonBox.setGeometry(QtCore.QRect(130, 100, 141, 75))
        self.exit_dialog_buttonBox.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.exit_dialog_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.No|QtWidgets.QDialogButtonBox.StandardButton.Yes)
        self.exit_dialog_buttonBox.setCenterButtons(True)
        self.exit_dialog_buttonBox.setObjectName("exit_dialog_buttonBox")

        self.retranslateUi(Exit_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Exit_Dialog)

    def retranslateUi(self, Exit_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Exit_Dialog.setWindowTitle(_translate("Exit_Dialog", "Dialog"))
        self.exit_label.setText(_translate("Exit_Dialog", "Вы уверены, что хотите выйти?"))
