from PyQt5 import QtCore, QtGui, QtWidgets
from configparser import ConfigParser

class Settings(object):
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(281, 232)
        Settings.setStyleSheet("background-color: rgb(108, 136, 177);\n"
"color: rgb(255, 255, 255);")
        self.address = QtWidgets.QLabel(Settings)
        self.address.setGeometry(QtCore.QRect(10, 40, 61, 20))
        self.address.setAlignment(QtCore.Qt.AlignCenter)
        self.address.setObjectName("address")
        self.address_text = QtWidgets.QLineEdit(Settings)
        self.address_text.setGeometry(QtCore.QRect(100, 40, 151, 21))
        self.address_text.setObjectName("address_text")
        self.port_text = QtWidgets.QLineEdit(Settings)
        self.port_text.setGeometry(QtCore.QRect(100, 70, 151, 21))
        self.port_text.setObjectName("port_text")
        self.port = QtWidgets.QLabel(Settings)
        self.port.setGeometry(QtCore.QRect(10, 70, 31, 19))
        self.port.setAlignment(QtCore.Qt.AlignCenter)
        self.port.setObjectName("port")
        self.login = QtWidgets.QLabel(Settings)
        self.login.setGeometry(QtCore.QRect(10, 100, 40, 19))
        self.login.setAlignment(QtCore.Qt.AlignCenter)
        self.login.setObjectName("login")
        self.login_text = QtWidgets.QLineEdit(Settings)
        self.login_text.setGeometry(QtCore.QRect(100, 100, 151, 21))
        self.login_text.setObjectName("login_text")
        self.password = QtWidgets.QLabel(Settings)
        self.password.setGeometry(QtCore.QRect(10, 130, 71, 20))
        self.password.setAlignment(QtCore.Qt.AlignCenter)
        self.password.setObjectName("password")
        self.password_text = QtWidgets.QLineEdit(Settings)
        self.password_text.setGeometry(QtCore.QRect(100, 130, 151, 21))
        self.password_text.setObjectName("password_text")
        self.save_stngs = QtWidgets.QPushButton(Settings)
        self.save_stngs.setGeometry(QtCore.QRect(160, 180, 88, 27))
        self.save_stngs.setObjectName("save_stngs")
        Settings.setWindowTitle("Settings")
        self.address.setText("Address:")
        self.port.setText("Port:")
        self.login.setText("Login:")
        self.password.setText("Password:")
        self.save_stngs.setText("Save")

        address = self.get_setting('Connection', 'Address')
        port = self.get_setting('Connection', 'Port')
        login = self.get_setting('Connection', 'Login')
        password = self.get_setting('Connection', 'Password')

        # Set values in UI
        self.address_text.setText(address)
        self.port_text.setText(port)
        self.login_text.setText(login)
        self.password_text.setText(password)

        # Connect Save button to save_settings function
        self.save_stngs.clicked.connect(self.save_settings)

    def save_settings(self):
        # Get values from UI
        address = self.address_text.text()
        port = self.port_text.text()
        login = self.login_text.text()
        password = self.password_text.text()

        # Save settings to config.ini
        self.set_setting('Connection', 'Address', address)
        self.set_setting('Connection', 'Port', port)
        self.set_setting('Connection', 'Login', login)
        self.set_setting('Connection', 'Password', password)
        self.save_config()

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