from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QTextEdit

from PyQt5.QtCore import Qt
class FireSafetyCalculator(QDialog):
    def __init__(self):
        
        super().__init__()

        self.setWindowTitle("Calculator")

        # Создание текстового поля для отображения введенных значений и результата
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        # Устанавливаем стиль главного окна
        self.setStyleSheet("background-color: rgb(108, 136, 177);\n"
                                 "color: rgb(255, 255, 255);")
         # Создание кнопок с цифрами
        self.digits = [QPushButton(str(i)) for i in range(10)]

        # Создание кнопок для операций
        self.operators = {
            '+': QPushButton('+'),
            '-': QPushButton('-'),
            '*': QPushButton('*'),
            '/': QPushButton('/'),
            '=': QPushButton('=')
        }

        # Создание кнопки очистки
        self.clear_button = QPushButton('C')

        # Создание текстового поля для отображения истории операций
        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)

        # Создание сетки для размещения кнопок
        grid = QGridLayout()

        # Размещение кнопок с цифрами в сетке
        for i, button in enumerate(self.digits):
            grid.addWidget(button, i // 3, i % 3)

        # Размещение кнопок операций в сетке
        row = len(self.digits) // 3
        for i, (operator, button) in enumerate(self.operators.items()):
            grid.addWidget(button, row, i)
            button.setStyleSheet("background-color: orange;")

        # Размещение кнопки очистки в сетке
        grid.addWidget(self.clear_button, row, len(self.operators))

        # Создание вертикального компоновщика для размещения текстового поля, сетки с кнопками и текстового поля истории
        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(grid)
        layout.addWidget(self.history_display)

        # Установка компоновщика в QDialog
        self.setLayout(layout)

        # Подключение обработчиков событий для кнопок
        for button in self.digits + list(self.operators.values()):
            button.clicked.connect(self.button_clicked)

        self.clear_button.clicked.connect(self.clear)

        # Инициализация переменных
        self.first_operand = None
        self.operator = None
        self.history = []

    def button_clicked(self):
        button = self.sender()
        text = button.text()

        if text.isdigit() or text == '.':
            self.display.insert(text)
        elif text in self.operators:
            self.calculate()
            self.first_operand = float(self.display.text())
            self.operator = text
            self.display.clear()
        elif text == '=':
            self.calculate()

    def calculate(self):
        if self.first_operand is not None and self.operator is not None:
            second_operand = float(self.display.text())

            if self.operator == '+':
                result = self.first_operand + second_operand
            elif self.operator == '-':
                result = self.first_operand - second_operand
            elif self.operator == '*':
                result = self.first_operand * second_operand
            elif self.operator == '/':
                result = self.first_operand / second_operand

            self.display.setText(str(result))
            self.add_to_history(self.first_operand, self.operator, second_operand, result)

            self.first_operand = None
            self.operator = None

    def clear(self):
        self.display.clear()
        self.first_operand = None
        self.operator = None

    def add_to_history(self, first_operand, operator, second_operand, result):
        history_entry = f"{first_operand} {operator} {second_operand} = {result}"
        self.history.append(history_entry)
        self.history_display.append(history_entry)
    # def __init__(self):
    #     super().__init__()
    #     self.setWindowTitle("Калькулятор пожароопасности")
    #     self.setGeometry(100, 100, 400, 200)
    #     self.setStyleSheet("background-color: rgb(108, 136, 177);\n"
    #                        "color: rgb(255, 255, 255);")
    #     self.init_ui()

    # def init_ui(self):
    #     layout = QVBoxLayout()

    #     # Создание элементов интерфейса
    #     label_temperature = QLabel("Температура (°C):")
    #     self.input_temperature = QLineEdit()

    #     label_relative_humidity = QLabel("Относительная влажность (%):")
    #     self.input_relative_humidity = QLineEdit()

    #     label_dew_point_temperature = QLabel("Температура точки росы (°C):")
    #     self.input_dew_point_temperature = QLineEdit()

    #     button_calculate = QPushButton("Вычислить")
    #     button_calculate.clicked.connect(self.calculate_fire_hazard_index)

    #     self.label_result = QLabel()

    #     layout.addWidget(label_temperature)
    #     layout.addWidget(self.input_temperature)
    #     layout.addWidget(label_relative_humidity)
    #     layout.addWidget(self.input_relative_humidity)
    #     layout.addWidget(label_dew_point_temperature)
    #     layout.addWidget(self.input_dew_point_temperature)
    #     layout.addWidget(button_calculate)
    #     layout.addWidget(self.label_result)

    #     self.setLayout(layout)

    # def calculate_fire_hazard_index(self):
    #     # Получение введенных значений из полей ввода
    #     temperature = float(self.input_temperature.text())
    #     relative_humidity = float(self.input_relative_humidity.text())
    #     dew_point_temperature = float(self.input_dew_point_temperature.text())

    #     # Вызов функции для вычисления показателя пожароопасности
    #     fire_hazard_index = self.calculate_index_nesterov(temperature, relative_humidity, dew_point_temperature)

    #     # Отображение результата вычислений
    #     self.label_result.setText(f"Комплексный показатель пожароопасности: {fire_hazard_index}")

    # def calculate_index_nesterov(self, temperature, relative_humidity, dew_point_temperature):
    #     # Здесь вы можете использовать свои формулы для расчета показателя пожароопасности
    #     # на основе индекса Нестерова и предоставленных данных.
    #     # Реализуйте ваш алгоритм расчета индекса Нестерова.

    #     # Пример вычисления индекса Нестерова
    #     index_nesterov = temperature * relative_humidity / dew_point_temperature

    #     return index_nesterov

