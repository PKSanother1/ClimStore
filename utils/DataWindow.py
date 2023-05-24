from PyQt5 import QtCore, QtGui, QtWidgets
from neo4j import GraphDatabase

class DataWindow(QtWidgets.QDialog):
    def __init__(self, neo4j_session, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Data")
        self.resize(800, 800)
        self.setStyleSheet("background-color: rgb(108, 136, 177);\n"
                           "color: rgb(255, 255, 255);")
        self.neo4j_session = neo4j_session  # Сохраняем сеанс Neo4j
        self.setup_ui()

    def setup_ui(self):
        # Создание таблицы
        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(3)  # Установка количества столбцов
        self.table.setHorizontalHeaderLabels(["Name", "Age", "City"])

        # Импорт данных из Neo4j
        self.import_data_from_neo4j()

        # Размещение таблицы в макете
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def import_data_from_neo4j(self):
        # Запрос данных из Neo4j
        query = "MATCH (p:person) RETURN p.movie, p.person, p.role"
        result = self.neo4j_session.run(query)

        # Получение списка имен полей из результата запроса
        field_names = result.keys()

        # Установка количества столбцов
        self.table.setColumnCount(len(field_names))

        # Заполнение заголовков столбцов
        self.table.setHorizontalHeaderLabels(field_names)

        # Заполнение таблицы данными из Neo4j
        self.table.setRowCount(0)
        records = list(result)
        self.table.setRowCount(len(records))
        
        row = 0

        for record in records:
            for column, field_name in enumerate(field_names):
                value = record[field_name]
                item = QtWidgets.QTableWidgetItem(str(value))
                self.table.setItem(row, column, item)

            row += 1