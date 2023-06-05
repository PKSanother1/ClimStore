from PyQt5.QtWidgets import QDialog,QApplication,QProgressDialog,QHBoxLayout,QVBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import json
import os 
from utils.Settings import Settings
from neo4j import GraphDatabase
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QPushButton, QGridLayout

class Load(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Load")
        self.setObjectName("Load")
        self.resize(1920, 1080)
        self.setStyleSheet("background-color: rgb(108, 136, 177);\n"
                           "color: rgb(255, 255, 255);")
        # Создание таблицы для отображения данных
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(15)
        self.table_widget.setHorizontalHeaderLabels([
            'Synoptic Index', 'Year in Greenwich', 'Month in Greenwich', 'Day in Greenwich', 'Time in Greenwich',
            'Year from Source Local', 'Month from Source Local', 'Day from Source Local', 'Time from Source Local',
            'Local Time', 'Average Wind Speed', 'Maximum Wind Speed',
            'Precipitation Sum', 'Min Soil Surface Temperature', 'Max Soil Surface Temperature'
        ])
        self.table_widget.resizeColumnsToContents()
        # Создание кнопок
        self.btn_select_file = QPushButton('Choose a file')
        # self.btn_convert_to_json = QPushButton('Convert to JSON')
        self.btn_send_to_database = QPushButton('Send to DB')
        self.btn_show_table = QPushButton('Calculate')
        self.btn_save_excel = QPushButton('Save Excel')

       # Назначение обработчиков событий для кнопок
        self.btn_select_file.clicked.connect(self.select_file)
        # self.btn_convert_to_json.clicked.connect(self.convert_to_json)
        self.btn_send_to_database.clicked.connect(self.send_to_database)
        self.btn_show_table.clicked.connect(self.open_data_window)
        # Создание компоновщика для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_select_file)
        # button_layout.addWidget(self.btn_convert_to_json)
        button_layout.addWidget(self.btn_send_to_database)
        button_layout.addWidget(self.btn_show_table)

        # Создание компоновщика для таблицы
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table_widget)

        # Создание компоновщика для кнопки "Save Excel"
        save_button_layout = QHBoxLayout()
        save_button_layout.addStretch(1)  # Добавляем растяжку перед кнопкой
        save_button_layout.addWidget(self.btn_save_excel)

        # Создание компоновщика для всех виджетов
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addLayout(table_layout)
        layout.addLayout(save_button_layout)

        # Установка компоновщика в диалоговое окно
        self.setLayout(layout)
        
        # Переменная для хранения данных
        self.data = []
    @staticmethod
    def save_data_as_json(data, directory, filename):
        # Формируем полный путь к файлу
        file_path = os.path.join(directory, filename)
        
        # Проверяем, существует ли файл
        if os.path.exists(file_path):
            # Если файл существует, генерируем новое имя
            base_name, ext = os.path.splitext(filename)
            new_filename = base_name + "_new" + ext
            file_path = os.path.join(directory, new_filename)
        
        # Конвертируем данные в формат JSON
        json_data = json.dumps(data)
        
        try:
            # Открываем файл для записи
            with open(file_path, 'w') as file:
                # Записываем данные в файл
                file.write(json_data)
            
            print(f"Данные успешно сохранены в файле {file_path}")
        
        except IOError:
            print(f"Ошибка при сохранении данных в файл {file_path}")

    def select_file(self):
        # Открытие диалога выбора файла
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '', 'Text files (*.txt)')

        if file_path:
            try:
                # Чтение данных из файла
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Очистка таблицы
                self.table_widget.setRowCount(0)
                self.data.clear()

                # Заполнение таблицы и сохранение данных
                for line in lines:
                    values = line.split()
                    if len(values) == 15:
                        row = len(self.data)
                        self.table_widget.insertRow(row)
                        for column, value in enumerate(values):
                            item = QTableWidgetItem(value)
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                            self.table_widget.setItem(row, column, item)
                        self.data.append(values)

                # Конвертация данных в формат JSON
                self.convert_to_json(file_path)

                QMessageBox.information(self, 'Успех', 'Файл успешно загружен.')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка при чтении файла: {str(e)}')

    def convert_to_json(self, file_path):
        if not self.data:
            QMessageBox.warning(self, 'Предупреждение', 'Нет данных для конвертации.')
            return

        try:
            # Получение имени файла без пути и расширения
            filename = os.path.splitext(os.path.basename(file_path))[0]

            # Получение директории файла
            directory = os.path.dirname(file_path)

            # Получение заголовков столбцов из таблицы
            headers = [self.table_widget.horizontalHeaderItem(column).text() for column in range(self.table_widget.columnCount())]

            # Создание списка для хранения сконвертированных данных
            converted_data = []

            # Обработка каждой строки данных
            for values in self.data:
                row_data = {}

                # Обработка каждого столбца
                for column, value in enumerate(values):
                    header = headers[column]
                    row_data[header] = value

                converted_data.append(row_data)

            # Формирование полного пути к файлу
            file_path = os.path.join(directory, filename + '.json')

            # Проверка наличия файла
            if os.path.exists(file_path):
                # Если файл существует, генерируем новое имя
                base_name, ext = os.path.splitext(filename)
                new_filename = base_name + "_new" + ext
                file_path = os.path.join(directory, new_filename)

            # Сохранение данных в формате JSON
            with open(file_path, 'w') as file:
                json.dump(converted_data, file, indent=4)

            QMessageBox.information(self, 'Успех', f'Данные успешно конвертированы и сохранены в файле:\n{file_path}')

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка при конвертации в JSON: {str(e)}')
            
    def send_to_database(self):
        # Получение настроек подключения к базе данных
        settings_win = Settings()
        address = settings_win.get_setting('Connection', 'Address')
        login = settings_win.get_setting('Connection', 'Login')
        password = settings_win.get_setting('Connection', 'Password')

        if not self.data:
            QMessageBox.warning(self, 'Предупреждение', 'Нет данных для отправки в базу данных.')
            return

        try:
            # Подключение к базе данных Neo4j
            driver = GraphDatabase.driver(f"neo4j+s://{address}", auth=(login, password))

            # Создание диалогового окна с ползунком загрузки
            progress_dialog = QProgressDialog("Отправка данных...", "Отмена", 0, len(self.data))
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setWindowTitle("Отправка данных")
            progress_dialog.setAutoClose(False)
            progress_dialog.setAutoReset(False)

            with driver.session() as session:
                # Отправка данных в базу данных
                for index, values in enumerate(self.data):
                    if progress_dialog.wasCanceled():
                        break

                    query = """
                    CREATE (s:Station {SynopticIndex: $synopticIndex})
                    MERGE (w:WeatherData {
                        YearInGreenwich: $yearInGreenwich,
                        MonthInGreenwich: $monthInGreenwich,
                        DayInGreenwich: $dayInGreenwich,
                        TimeInGreenwich: $timeInGreenwich,
                        YearFromSourceLocal: $yearFromSourceLocal,
                        MonthFromSourceLocal: $monthFromSourceLocal,
                        DayFromSourceLocal: $dayFromSourceLocal,
                        TimeFromSourceLocal: $timeFromSourceLocal,
                        LocalTime: $localTime,
                        AverageWindSpeed: $averageWindSpeed,
                        MaximumWindSpeed: $maximumWindSpeed,
                        PrecipitationSum: $precipitationSum,
                        MinSoilSurfaceTemperature: $minSoilSurfaceTemperature,
                        MaxSoilSurfaceTemperature: $maxSoilSurfaceTemperature
                    })
                    CREATE (s)-[:HAS_WEATHER_DATA]->(w)
                    """

                    # Выполнение запроса и передача параметров
                    session.run(query, {
                        'synopticIndex': values[0],
                        'yearInGreenwich': values[1],
                        'monthInGreenwich': values[2],
                        'dayInGreenwich': values[3],
                        'timeInGreenwich': values[4],
                        'yearFromSourceLocal': values[5],
                        'monthFromSourceLocal': values[6],
                        'dayFromSourceLocal': values[7],
                        'timeFromSourceLocal': values[8],
                        'localTime': values[9],
                        'averageWindSpeed': values[10],
                        'maximumWindSpeed': values[11],
                        'precipitationSum': values[12],
                        'minSoilSurfaceTemperature': values[13],
                        'maxSoilSurfaceTemperature': values[14]
                    })

                    # Обновление значения ползунка загрузки
                    progress_dialog.setValue(index + 1)
                    QApplication.processEvents()

            progress_dialog.close()
            QMessageBox.information(self, 'Успех', 'Данные успешно отправлены в базу данных.')
        except Exception as e:
            progress_dialog.close()
            QMessageBox.critical(self, 'Ошибка', f'Ошибка при отправке в базу данных: {str(e)}')

    def save_as_excel(self):
        if self.table_widget.rowCount() == 0:
            QMessageBox.warning(self, 'Предупреждение', 'Нет данных для сохранения.')
            return

        # Создание экземпляра Workbook
        workbook = Workbook()
        # Получение активного листа
        sheet = workbook.active

        # Запись данных в активный лист
        for row in range(self.table_widget.rowCount()):
            for column in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, column)
                if item is not None:
                    sheet.cell(row=row + 1, column=column + 1).value = item.text()

        # Выбор пути для сохранения файла
        file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить как Excel', '', 'Excel Files (*.xlsx)')

        if file_path:
            try:
                # Сохранение книги в формате Excel
                workbook.save(file_path)
                QMessageBox.information(self, 'Успех', 'Таблица успешно сохранена в формате Excel.')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Ошибка при сохранении таблицы в формате Excel: {str(e)}')
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Не указан путь для сохранения файла.')


    def show_table(self):
        if not self.data:
            QMessageBox.warning(self, 'Предупреждение', 'Нет данных для отображения в таблице.')
            return
        
        self.table_widget.setRowCount(0)
        
        # Заполнение таблицы из данных
        for row, values in enumerate(self.data):
            self.table_widget.insertRow(row)
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(row, column, item)

        QMessageBox.information(self, 'Успех', 'Таблица успешно отображена.')

    def open_data_window(self):
        if not self.data:
            QMessageBox.warning(self, 'Предупреждение', 'Нет данных для отображения в таблице.')
            return
        self.show_table() 
        data_window = DataWindow(self.data)  # Передача self.data в конструктор DataWindow
        data_window.exec_()

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QMessageBox

class DataWindow(QDialog):

    def __init__(self, data):
        super().__init__()
        self.setWindowTitle('Data')
        self.setObjectName("Data")
        self.resize(1900, 700)
        self.setStyleSheet("background-color: rgb(108, 136, 177);\n"
                           "color: rgb(255, 255, 255);")
        # Сохранение данных
        self.data = data
        
        # Создание таблицы для отображения данных
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(17)
        self.table_widget.setHorizontalHeaderLabels([
            'Station Synoptic Index', 'Year in Greenwich', 'Month in Greenwich', 'Day in Greenwich',
            'Time in Greenwich', 'Year from Source (local)', 'Month from Source (local)', 'Day from Source (local)',
            'Time from Source (local)', 'Local Time', 'Average Wind Speed', 'Maximum Wind Speed', 'Precipitation Sum',
            'Min. Soil Surface Temperature between Time Intervals', 'Max. Soil Surface Temperature between Time Intervals',
            'Soil Surface Temperature at Maximum Thermistor Depth', 'Dew Point Temperature'
        ])
        self.table_widget.resizeColumnsToContents()
        # Заполнение таблицы данными
        self.fill_table()

        # Создание полей для ввода данных и кнопки "Вычислить"
        self.line_edits = [QLineEdit() for _ in range(8)]
        self.calc_button = QPushButton('Вычислить')
        self.calc_button.clicked.connect(self.calculate)

        # Создание компоновщика и добавление виджетов
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        for line_edit in self.line_edits:
            layout.addWidget(line_edit)
        layout.addWidget(self.calc_button)

        # Установка компоновщика в окно
        self.setLayout(layout)

    def fill_table(self):
        # Очистка таблицы
        self.table_widget.setRowCount(0)

        # Заполнение таблицы из данных
        for row, values in enumerate(self.data):
            self.table_widget.insertRow(row)
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(row, column, item)

    def calculate(self):
        # Получение данных из таблицы
        table_data = []
        for row in range(self.table_widget.rowCount()):
            row_data = []
            for column in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, column)
                if item is not None:
                    row_data.append(item.text())
            table_data.append(row_data)

        # Получение введенных данных из полей
        input_values = [line_edit.text() for line_edit in self.line_edits]
        
        # Выполнение вычислений на основе введенных данных и данных из таблицы
        result = self.calculate_result(input_values, table_data)
        
        # Отображение результата
        QMessageBox.information(self, 'Результат', f'Результат: {result}')

    def calculate_result(self, input_values, table_data):
        # Реализуйте здесь свою логику вычислений на основе введенных данных и данных из таблицы
        # В данном примере просто суммируем числовые значения введенных данных и средние значения столбцов таблицы
        input_sum = sum(map(int, input_values))
        table_average = [sum(map(int, column)) / len(column) for column in zip(*table_data)]
        
        # Возвращаем сумму введенных данных и список средних значений столбцов таблицы
        return input_sum, table_average
    
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QMessageBox


class DataWindow(QDialog):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle('Data Window')
        self.resize(800, 600)
        self.setStyleSheet("background-color: rgb(108, 136, 177);\n"
                           "color: rgb(255, 255, 255);")
        # Создание таблицы для отображения данных
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(15)
        self.table_widget.setHorizontalHeaderLabels([
            'Год по Гринвичу', 'Месяц по Гринвичу', 'День по Гринвичу', 'Срок по Гринвичу',
            'Направление ветра', 'Средняя скорость ветра', 'Максимальная скорость ветра',
            'Сумма осадков', 'Температура поверхности почвы', 'Температура воздуха по сухому терм-ру',
            'Относительная влажность воздуха', 'Температура точки росы',
            'Атмосферное давление на уровне станции', 'Величина барической тенденции',
            'Температура воздуха'
        ])

        # Заполнение таблицы данными
        self.fill_table(data)

        # Создание вертикального компоновщика и добавление элементов
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        # Вычисление комплексного показателя пожароопасности
        self.calculate()

    def fill_table(self, data):
        self.table_widget.setRowCount(len(data))
        for row, values in enumerate(data):
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(row, column, item)

    def calculate(self):
        # Индексы столбцов в таблице
        wind_direction_column = 4
        average_wind_speed_column = 5
        maximum_wind_speed_column = 6
        precipitation_sum_column = 7
        soil_surface_temperature_column = 8
        air_temperature_column = 10
        relative_humidity_column = 11
        dew_point_temperature_column = 12

        # Получение данных из таблицы
        data = []
        for row in range(self.table_widget.rowCount()):
            values = [
                self.table_widget.item(row, wind_direction_column).text(),
                self.table_widget.item(row, average_wind_speed_column).text(),
                self.table_widget.item(row, maximum_wind_speed_column).text(),
                self.table_widget.item(row, precipitation_sum_column).text(),
                self.table_widget.item(row, soil_surface_temperature_column).text(),
                self.table_widget.item(row, air_temperature_column).text(),
                self.table_widget.item(row, relative_humidity_column).text(),
                self.table_widget.item(row, dew_point_temperature_column).text()
            ]
            data.append(values)

        # Выполнение вычислений
        results = []
        for row, values in enumerate(data):
            result = self.perform_calculations(values)
            results.append(result)

            # Отображение данных и результатов
            self.display_result(row, values, result)

        # Вывод общего результата
        total_result = sum(results) / len(results)
        QMessageBox.information(self, 'Общий результат', f'Общий результат вычислений: {total_result}')

    def perform_calculations(self, values):
        # Выполнение вычислений на основе значений
        k = 0.8
        wind_direction = float(values[0])
        average_wind_speed = float(values[1])
        maximum_wind_speed = float(values[2])
        precipitation_sum = float(values[3])
        soil_surface_temperature = float(values[4])
        air_temperature = float(values[5])
        relative_humidity = float(values[6])
        dew_point_temperature = float(values[7])

        result = k * (wind_direction + average_wind_speed + maximum_wind_speed) + (1 - k) * (
                precipitation_sum + soil_surface_temperature + air_temperature + relative_humidity + dew_point_temperature)
        return result

    def display_result(self, row, values, result):
        # Отображение данных и результата
        data_string = ', '.join(values)
        QMessageBox.information(self, 'Результат',
                                f'Для данных: {data_string}\nРезультат вычислений: {result}')


