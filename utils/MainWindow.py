from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from utils.About import About
from utils.Settings import Settings
from utils.DataWindow import DataWindow
import neo4j
from neo4j import GraphDatabase
import logging
import sys
import json
import os

# Создание логгера
logger = logging.getLogger('connection_logger')
logger.setLevel(logging.INFO)

# Создание обработчика для вывода в терминал
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

# Создание форматировщика логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавление обработчика в логгер
logger.addHandler(handler)

class LoadDataWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            # Read the txt file
            with open(self.file_path, 'r') as file:
                lines = file.readlines()

            # Prepare the list of data dictionaries
            data = []
            for line in lines:
                values = line.split()
                if len(values) == 17:  # Check if the line has enough values
                    entry = {
                        'Station Synoptic Index': values[0],
                        'Year in Greenwich': values[1],
                        'Month in Greenwich': values[2],
                        'Day in Greenwich': values[3],
                        'Time in Greenwich': values[4],
                        'Year from Source (local)': values[5],
                        'Month from Source (local)': values[6],
                        'Day from Source (local)': values[7],
                        'Time from Source (local)': values[8],
                        'Local Time': values[9],
                        'Average Wind Speed': values[10],
                        'Maximum Wind Speed': values[11],
                        'Precipitation Sum': values[12],
                        'Min. Soil Surface Temperature between Time Intervals': values[13],
                        'Max. Soil Surface Temperature between Time Intervals': values[14],
                        'Soil Surface Temperature at Maximum Thermistor Depth': values[15],
                        'Dew Point Temperature': values[16]
                    }
                    data.append(entry)

            # Convert the data to JSON string
            json_data = json.dumps(data)
            main_win = MainWindow()
            # Import the JSON data into Neo4j
            main_win.import_data_to_neo4j(json_data)

            # Save the JSON data to a file in the "data" folder
            # file_name = os.path.basename(self.file_path)
            save_path = os.path.join("data", "data3" + ".json")
            with open(save_path, 'w') as json_file:
                json_file.write(json_data)

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
    




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

        self.data_btn = QtWidgets.QPushButton(self.centralwidget)
        self.data_btn.setGeometry(QtCore.QRect(530, 230, 190, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.data_btn.setFont(font)
        self.data_btn.setObjectName("data_btn")
        self.data_btn.clicked.connect(self.open_data_window)

        self.load_btn = QtWidgets.QPushButton(self.centralwidget)
        self.load_btn.setGeometry(QtCore.QRect(530, 150, 190, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.load_btn.setFont(font)
        self.load_btn.setObjectName("load_btn")
        self.load_btn.clicked.connect(self.load_btn_clicked)

        self.view_btn = QtWidgets.QPushButton(self.centralwidget)
        self.view_btn.setGeometry(QtCore.QRect(530, 310, 190, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.view_btn.setFont(font)
        self.view_btn.setObjectName("view_btn")

        self.calculate_btn = QtWidgets.QPushButton(self.centralwidget)
        self.calculate_btn.setGeometry(QtCore.QRect(530, 390, 190, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.calculate_btn.setFont(font)
        self.calculate_btn.setObjectName("calculate_btn")

        self.settings_btn = QtWidgets.QPushButton(self.centralwidget)
        self.settings_btn.setGeometry(QtCore.QRect(530, 470, 190, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.settings_btn.setFont(font)
        self.settings_btn.setObjectName("settings_btn")

        self.image_1 = QtWidgets.QLabel(self.centralwidget)
        self.image_1.setGeometry(QtCore.QRect(50, 80, 400, 400))
        self.image_1.setText("")
        self.image_1.setPixmap(QtGui.QPixmap("assets/earth.png"))
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
        self.load_btn.setText("Load")
        self.actionData_3.setText("Data")
        self.plot_action.setText("Plot")
        self.neo4j_switch = QtWidgets.QPushButton(self.centralwidget)
        self.neo4j_switch.setGeometry(QtCore.QRect(20, 500, 100, 30))
        self.neo4j_switch.setCheckable(True)
        self.neo4j_switch.setObjectName("neo4j_switch")
        self.neo4j_switch.setText("Connect")
        self.settings_btn.clicked.connect(self.open_settings)
        self.menu_settings.triggered.connect(self.open_settings)
        self.menu_about.triggered.connect(self.show_about)
        self.neo4j_switch.clicked.connect(self.toggle_neo4j_connection)
    def toggle_neo4j_connection(self):
        if self.neo4j_switch.isChecked():
            if self.connect_to_neo4j():
                self.neo4j_switch.setText("Disconnect")
            else:
                QMessageBox.critical(self.centralwidget, "Connection Error", "Failed to connect to Neo4j.")
                self.neo4j_switch.setChecked(False)
        else:
            self.disconnect_from_neo4j()
            self.neo4j_switch.setText("Connect")

    def connect_to_neo4j(self):
        # Установка соединения с базой данных Neo4j
        settings_win = Settings()
        address = settings_win.get_setting('Connection', 'Address')
        login = settings_win.get_setting('Connection', 'Login')
        password = settings_win.get_setting('Connection', 'Password')
        # Установка соединения с базой данных Neo4j
        try:
            logger.info(f"Connecting to Neo4j - Address: {address}, Login: {login}")
            self.driver = GraphDatabase.driver(f"neo4j+s://{address}", auth=(login, password), connection_timeout=10)
            self.session = self.driver.session()
            if self.is_neo4j_connected():
                print("Connected to Neo4j")
                return True
            else:
                print("Not Connected")
                return False
        except Exception as e:
            error_message = "Connection failed: " + str(e)
            logger.error(error_message)
            self.show_error_message(error_message)
            return False

    def disconnect_from_neo4j(self):
        # Разрыв соединения с базой данных Neo4j
        self.session.close()
        self.driver.close()
        print('Disconnected')

    def open_settings(self):
        settings_win = Settings()
        settings_win.open_dialog()


    def show_about(self):
        about_ui = About()
        about_ui.open_dialog()

    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.button(QMessageBox.Ok).setStyleSheet("QPushButton { text-align: center; }")
        error_box.exec_()
        
    def is_neo4j_connected(self):
        try:
            # Проверка наличия активного соединения с базой данных Neo4j
            # Если соединение отсутствует, возникнет исключение
            self.session.run("MATCH (n) RETURN n LIMIT 1")
            return True
        except Exception:
            return False
    
    def open_data_window(self):
        # Проверяем, подключены ли мы к Neo4j
        if self.neo4j_switch.isChecked():
            # Проверяем, что есть активное соединение с Neo4j
            if self.is_neo4j_connected():
                # Создаем экземпляр класса DataWindow
                data_window = DataWindow(self.session)

                # Открываем окно DataWindow
                data_window.exec_()
            else:
                # Предупреждаем пользователя, что он должен сначала подключиться к Neo4j
                QMessageBox.information(self.centralwidget, "Connection Required", "Please connect to Neo4j first.")
        else:
            # Предупреждаем пользователя, что он должен сначала подключиться к Neo4j
            QMessageBox.information(self.centralwidget, "Connection Required", "Please connect to Neo4j first.")

    def load_btn_clicked(self):
        if self.neo4j_switch.isChecked():
            if self.is_neo4j_connected():
                file_dialog = QFileDialog()
                file_path, _ = file_dialog.getOpenFileName(None, "Select File", "", "Text Files (*.txt)")

                if file_path:
                    self.load_data_worker = LoadDataWorker(file_path)
                    self.load_data_worker.finished.connect(self.data_loaded)
                    self.load_data_worker.error.connect(self.data_load_failed)

                    self.thread = QThread()
                    self.load_data_worker.moveToThread(self.thread)

                    self.thread.started.connect(self.load_data_worker.run)
                    self.thread.finished.connect(self.thread.deleteLater)

                    self.thread.start()
            else:
                # Предупреждаем пользователя, что он должен сначала подключиться к Neo4j
                QMessageBox.information(self.centralwidget, "Connection Required", "Please connect to Neo4j first.")
        else:
            # Предупреждаем пользователя, что он должен сначала подключиться к Neo4j
            QMessageBox.information(self.centralwidget, "Connection Required", "Please connect to Neo4j first.")

    def data_loaded(self):
        QMessageBox.information(self.centralwidget, "Data Loaded", "Data loaded and imported into Neo4j successfully.")

    def data_load_failed(self, error):
        QMessageBox.critical(self.centralwidget, "Error", f"Failed to load data: {error}")
    def import_data_to_neo4j(self, json_data):
        try:
            # Check if connected to Neo4j
            if self.is_neo4j_connected():
                # Parse the JSON data
                # data = json.loads(json_data)
                driver = GraphDatabase.driver("neo4j+s://ca6a9e12.databases.neo4j.io", auth=("neo4j", "uCi5I8XGEiPniaQmgC02YQUL8C5RwpOF3BHimxATRmg"))
                session = driver.session()
                # Construct the Cypher query to import the data
                for entry in json_data:
            # Create a node for each entry
                    session.run("CREATE (entry:Entry {synopticIndex: $synopticIndex, year: $year, month: $month, day: $day})",
                                synopticIndex=entry['Station Synoptic Index'],
                                year=entry['Year in Greenwich'],
                                month=entry['Month in Greenwich'],
                                day=entry['Day in Greenwich'])

                    # Create relationships between nodes based on your data model

                # Close the Neo4j session and driver
                # self.session.close()
                # self.driver.close()

        except Exception as e:
            error_message = "Failed to import data to Neo4j: " + str(e)
            logger.error(error_message)
            self.show_error_message(error_message)