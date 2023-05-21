
import sys
from PyQt5 import QtWidgets
from utils.MainWindow import MainWindow

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())