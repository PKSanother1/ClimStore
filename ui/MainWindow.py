from PyQt5 import QtCore, QtGui, QtWidgets
from ui.About import About
from ui.Settings import Settings

class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(888, 563)
        
        # Устанавливаем шрифт
        font = QtGui.QFont()
        font.setFamily("URW Gothic")
        font.setKerning(True)
        MainWindow.setFont(font)
        
        # Устанавливаем стиль главного окна
        MainWindow.setStyleSheet("background-color: rgb(108, 136, 177);\n"
                                 "color: rgb(255, 255, 255);")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        
        self.MainWindow_text = QtWidgets.QLabel(self.centralwidget)
        self.MainWindow_text.setGeometry(QtCore.QRect(490, 60, 261, 61))
        font = QtGui.QFont()
        font.setFamily("URW Gothic")
        font.setPointSize(40)
        self.MainWindow_text.setFont(font)
        self.MainWindow_text.setStyleSheet("\n"
                                     "background-color: rgb(108, 136, 177);")
        self.MainWindow_text.setAlignment(QtCore.Qt.AlignCenter)
        self.MainWindow_text.setObjectName("MainWindow_text")
        
        self.settings_btn = QtWidgets.QPushButton(self.centralwidget)
        self.settings_btn.setGeometry(QtCore.QRect(530, 390, 190, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.settings_btn.setFont(font)
        self.settings_btn.setObjectName("settings_btn")
        
        self.data_btn = QtWidgets.QPushButton(self.centralwidget)
        self.data_btn.setGeometry(QtCore.QRect(530, 150, 190, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.data_btn.setFont(font)
        self.data_btn.setObjectName("data_btn")
        
        self.view_btn = QtWidgets.QPushButton(self.centralwidget)
        self.view_btn.setGeometry(QtCore.QRect(530, 230, 190, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.view_btn.setFont(font)
        self.view_btn.setObjectName("view_btn")
        
        self.calculate_btn = QtWidgets.QPushButton(self.centralwidget)
        self.calculate_btn.setGeometry(QtCore.QRect(530, 310, 190, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.calculate_btn.setFont(font)
        self.calculate_btn.setObjectName("calculate_btn")
        
        self.image_1 = QtWidgets.QLabel(self.centralwidget)
        self.image_1.setGeometry(QtCore.QRect(50, 80, 400, 400))
        self.image_1.setText("")
        self.image_1.setPixmap(QtGui.QPixmap("/home/fda/Pictures/earth.png"))
        self.image_1.setScaledContents(True)
        self.image_1.setObjectName("image_1")
        self.image_1.raise_()
        self.settings_btn.raise_()
        self.data_btn.raise_()
        self.view_btn.raise_()
        self.calculate_btn.raise_()
        self.MainWindow_text.raise_()

        # Установка центрального виджета главного окна
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 888, 24))
        self.menubar.setObjectName("menubar")
        
        self.menu_about = QtWidgets.QMenu(self.menubar)
        self.menu_about.setObjectName("menu_about")
        
        self.menu_settings = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("URW Gothic")
        self.menu_settings.setFont(font)
        self.menu_settings.setObjectName("menu_settings")
        
        self.menu_open = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("URW Gothic")
        self.menu_open.setFont(font)
        self.menu_open.setObjectName("menu_open")
        
        self.menuSave = QtWidgets.QMenu(self.menubar)
        self.menuSave.setObjectName("menuSave")
        
        self.menu_send = QtWidgets.QMenu(self.menubar)
        self.menu_send.setObjectName("menu_send")
        
        self.menu_recieve = QtWidgets.QMenu(self.menubar)
        self.menu_recieve.setObjectName("menu_recieve")
        
        self.menu_view = QtWidgets.QMenu(self.menubar)
        self.menu_view.setObjectName("menu_view")
        
        # Установка строки меню в главном окне
        MainWindow.setMenuBar(self.menubar)
        
        self.file_btn = QtWidgets.QAction(MainWindow)
        self.file_btn.setObjectName("file_btn")
        
        self.data_btn_2 = QtWidgets.QAction(MainWindow)
        self.data_btn_2.setObjectName("data_btn_2")
        
        self.save_btn = QtWidgets.QAction(MainWindow)
        self.save_btn.setObjectName("save_btn")
        
        self.saveAs_btn = QtWidgets.QAction(MainWindow)
        self.saveAs_btn.setObjectName("saveAs_btn")
        
        self.actionData_2 = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("URW Gothic")
        self.actionData_2.setFont(font)
        self.actionData_2.setObjectName("actionData_2")
        
        self.actionData_3 = QtWidgets.QAction(MainWindow)
        self.actionData_3.setObjectName("actionData_3")
        
        self.plot_action = QtWidgets.QAction(MainWindow)
        self.plot_action.setObjectName("plot_action")
        
        self.settings_action = QtWidgets.QAction(MainWindow)
        self.settings_action.setObjectName("settings_action")
        self.settings_action.setText("Settings")
        
        self.about_action = QtWidgets.QAction(MainWindow)
        self.about_action.setObjectName("about_action")
        self.about_action.setText("About")
        
        self.menu_settings.addAction(self.settings_action)
        self.menu_about.addAction(self.about_action)
        self.menu_open.addAction(self.file_btn)
        self.menu_open.addAction(self.data_btn_2)
        self.menuSave.addAction(self.save_btn)
        self.menuSave.addAction(self.saveAs_btn)
        self.menu_view.addAction(self.plot_action)
        
        self.menubar.addAction(self.menu_open.menuAction())
        self.menubar.addAction(self.menuSave.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menubar.addAction(self.menu_send.menuAction())
        self.menubar.addAction(self.menu_recieve.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_about.menuAction())

        MainWindow.setWindowTitle("MainWindow")
        self.MainWindow_text.setText("ClimStore")
        self.settings_btn.setText("Settings")
        self.data_btn.setText("Data")
        self.view_btn.setText("View")
        self.calculate_btn.setText("Calculate")
        self.menu_about.setTitle("About")
        self.menu_settings.setTitle("Settings")
        self.menu_open.setTitle("Open")
        self.menuSave.setTitle("Save")
        self.menu_send.setTitle("Send")
        self.menu_recieve.setTitle("Recieve")
        self.menu_view.setTitle("View")
        self.file_btn.setText("File")
        self.data_btn_2.setText("Data")
        self.save_btn.setText("Save")
        self.saveAs_btn.setText("Save as")
        self.actionData_2.setText("Data")
        self.actionData_3.setText("Data")
        self.plot_action.setText("Plot")


        self.settings_btn.clicked.connect(self.open_settings)
        self.menu_settings.triggered.connect(self.open_settings)
        self.menu_about.triggered.connect(self.show_about)

    def open_settings(self):
        settings_dialog = QtWidgets.QDialog()
        settings_ui = Settings()
        settings_ui.setupUi(settings_dialog)
        settings_dialog.exec()

    def show_about(self):
        about_dialog = QtWidgets.QDialog()
        about_ui = About()
        about_ui.setupUi(about_dialog)
        about_dialog.exec_()