from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("My App")
        self.setGeometry(100, 100, 800, 600)

        self.button = QPushButton("Press Me")
        self.setCentralWidget(self.button)

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()