from PyQt5 import QtCore, QtGui, QtWidgets
from configparser import ConfigParser

class Settings(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.config = ConfigParser()
        self.config.read('config.ini')

        self.setObjectName("Settings")
        self.resize(389, 224)
        self.setStyleSheet("background-color: rgb(108, 136, 177);\n"
                           "color: rgb(255, 255, 255);")
        self.address = QtWidgets.QLabel(self)
        self.address.setGeometry(QtCore.QRect(10, 40, 61, 20))
        self.address.setAlignment(QtCore.Qt.AlignCenter)
        self.address.setObjectName("address")
        self.address_text = QtWidgets.QLineEdit(self)
        self.address_text.setGeometry(QtCore.QRect(100, 40, 270, 21))
        self.address_text.setObjectName("address_text")
        self.login = QtWidgets.QLabel(self)
        self.login.setGeometry(QtCore.QRect(10, 70, 40, 19))
        self.login.setAlignment(QtCore.Qt.AlignCenter)
        self.login.setObjectName("login")
        self.login_text = QtWidgets.QLineEdit(self)
        self.login_text.setGeometry(QtCore.QRect(100, 70, 270, 21))
        self.login_text.setObjectName("login_text")
        self.password = QtWidgets.QLabel(self)
        self.password.setGeometry(QtCore.QRect(10, 100, 71, 20))
        self.password.setAlignment(QtCore.Qt.AlignCenter)
        self.password.setObjectName("password")
        self.password_text = QtWidgets.QLineEdit(self)
        self.password_text.setGeometry(QtCore.QRect(100, 100, 270, 21))
        self.password_text.setObjectName("password_text")
        self.save_stngs = QtWidgets.QPushButton(self)
        self.save_stngs.setGeometry(QtCore.QRect(280, 180, 88, 27))
        self.save_stngs.setObjectName("save_stngs")
        self.setWindowTitle("Settings")
        self.address.setText("Address:")
        self.login.setText("Login:")
        self.password.setText("Password:")
        self.save_stngs.setText("Save")

        address = self.get_setting('Connection', 'Address')
        login = self.get_setting('Connection', 'Login')
        password = self.get_setting('Connection', 'Password')

        # Set values in UI
        self.address_text.setText(address)
        self.login_text.setText(login)
        self.password_text.setText(password)

        # Connect Save button to save_settings function
        self.save_stngs.clicked.connect(self.save_settings)

    def open_dialog(self):
        self.exec_()

    def save_settings(self):
        # Get values from UI
        address = self.address_text.text()
        login = self.login_text.text()
        password = self.password_text.text()

        # Save settings to config.ini
        self.set_setting('Connection', 'Address', address)
        self.set_setting('Connection', 'Login', login)
        self.set_setting('Connection', 'Password', password)
        self.save_config()
        self.close()

    def get_setting(self, section, option):
        if self.config.has_option(section, option):
            return self.config.get(section, option)
        else:
            return None

    def set_setting(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)

    def save_config(self):
        with open('config.ini', 'w') as config_file:
            self.config.write(config_file)