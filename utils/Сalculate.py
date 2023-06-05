import sys
from PyQt5.QtWidgets import QApplication, QDialog,QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton

class FireSafetyCalculator(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор пожароопасности")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: rgb(108, 136, 177);\n"
                           "color: rgb(255, 255, 255);")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Создание элементов интерфейса
        label_temperature = QLabel("Температура (°C):")
        self.input_temperature = QLineEdit()

        label_relative_humidity = QLabel("Относительная влажность (%):")
        self.input_relative_humidity = QLineEdit()

        label_dew_point_temperature = QLabel("Температура точки росы (°C):")
        self.input_dew_point_temperature = QLineEdit()

        button_calculate = QPushButton("Вычислить")
        button_calculate.clicked.connect(self.calculate_fire_hazard_index)

        self.label_result = QLabel()

        layout.addWidget(label_temperature)
        layout.addWidget(self.input_temperature)
        layout.addWidget(label_relative_humidity)
        layout.addWidget(self.input_relative_humidity)
        layout.addWidget(label_dew_point_temperature)
        layout.addWidget(self.input_dew_point_temperature)
        layout.addWidget(button_calculate)
        layout.addWidget(self.label_result)

        self.setLayout(layout)

    def calculate_fire_hazard_index(self):
        # Получение введенных значений из полей ввода
        temperature = float(self.input_temperature.text())
        relative_humidity = float(self.input_relative_humidity.text())
        dew_point_temperature = float(self.input_dew_point_temperature.text())

        # Вызов функции для вычисления показателя пожароопасности
        fire_hazard_index = self.calculate_index_nesterov(temperature, relative_humidity, dew_point_temperature)

        # Отображение результата вычислений
        self.label_result.setText(f"Комплексный показатель пожароопасности: {fire_hazard_index}")

    def calculate_index_nesterov(self, temperature, relative_humidity, dew_point_temperature):
        # Здесь вы можете использовать свои формулы для расчета показателя пожароопасности
        # на основе индекса Нестерова и предоставленных данных.
        # Реализуйте ваш алгоритм расчета индекса Нестерова.

        # Пример вычисления индекса Нестерова
        index_nesterov = temperature * relative_humidity / dew_point_temperature

        return index_nesterov
