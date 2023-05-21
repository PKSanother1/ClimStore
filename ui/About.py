from PyQt5 import QtCore, QtGui, QtWidgets


class About(object):
    def setupUi(self, dialog):
        dialog.setWindowTitle("About")
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 263, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(dialog)
        self.label_2.setGeometry(QtCore.QRect(0, 50, 263, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(dialog)
        self.label_3.setGeometry(QtCore.QRect(0, 100, 263, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.label.setText("ClimStore")
        self.label_2.setText("version: 0.01")
        self.label_3.setText("Authorized: Fedorov Juluur")