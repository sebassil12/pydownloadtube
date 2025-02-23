from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QLineEdit, QVBoxLayout
import sys
from download import Download
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Download YOutube music")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel()
        self.label.setText("Introduce la URL del video de YouTube:")
        self.input = QLineEdit()

        self.button = QPushButton("Download")
        self.button.clicked.connect(self.download_audio)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                display: flex;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def download_audio(self):
        url = self.input.text()
        downloader = Download()
        downloader.download_audio(url)
        print("Descarga completada.")

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()