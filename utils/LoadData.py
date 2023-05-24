from PyQt5.QtCore import QThread, QObject, pyqtSignal
import json
import os
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
                        'Синоптический индекс станции': values[0],
                        'Год по Гринвичу': values[1],
                        'Месяц по Гринвичу': values[2],
                        'День по Гринвичу': values[3],
                        'Срок по Гринвичу': values[4],
                        'Год источника (местный)': values[5],
                        'Месяц источника (местный)': values[6],
                        'День источника (местный)': values[7],
                        'Срок источника (местный)': values[8],
                        'Время местное': values[9],
                        'Средняя скорость ветра': values[10],
                        'Максимальная скорость ветра': values[11],
                        'Сумма осадков': values[12],
                        'Мин. температура пов-сти почвы между сроками': values[13],
                        'Макс. температура пов-сти почвы между сроками': values[14],
                        'Температура пов-сти почвы по макс. терм-ру п/встр.': values[15],
                        'Температура точки росы': values[16]
                    }
                    data.append(entry)

            # Convert the data to JSON string
            json_data = json.dumps(data)

            # Import the JSON data into Neo4j
            self.import_data_to_neo4j(json_data)

            # Save the JSON data to a file in the "data" folder
            file_name = os.path.basename(self.file_path)
            save_path = os.path.join("data", file_name + ".json")
            with open(save_path, 'w') as json_file:
                json_file.write(json_data)

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
    
    import json

def import_data_to_neo4j(json_data):
    try:
        # Check if connected to Neo4j
        if self.is_neo4j_connected():
            # Parse the JSON data
            data = json.loads(json_data)

            # Construct the Cypher query to import the data
            query = "CREATE "
            for i, entry in enumerate(data):
                query += "(n" + str(i) + ":" + "Station" + " { "
                for key, value in entry.items():
                    query += key.replace(" ", "_") + ": '" + value + "', "
                query = query[:-2] + " }), "
            query = query[:-2]

            # Execute the Cypher query
            self.session.run(query)
    except Exception as e:
        error_message = "Failed to import data to Neo4j: " + str(e)
        logger.error(error_message)
        self.show_error_message(error_message)