from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, \
                            QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, \
                            QWidget, QDialog, QDialogButtonBox, QGridLayout
import sys
from download import Download
#Main class to deploy the interface
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        # Initialize the main window
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Download Youtube music")
        self.setGeometry(100, 100, 800, 600)
        # Set the window icon
        self.label = QLabel()
        self.label_path_download = QLabel()
        self.label.setText("Introduce la URL del video de YouTube:")
        self.label_path_download.setText("Introduce la ruta donde se guardan tus descargas:")
        self.input = QLineEdit()
        self.input_path_download = QLineEdit()

        self.button = QPushButton("Download")
        self.button.clicked.connect(self.download_audio)

        layout = QGridLayout()
        layout.addWidget(self.label_path_download, 0, 0)
        layout.addWidget(self.input_path_download, 0, 1)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.input, 1, 1)
        layout.addWidget(self.button, 2, 0)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setStyleSheet("""
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
        dlg = QDialog(self)
        output_path = self.input_path_download.text()
        try:
            url = self.input.text()
            downloader = Download(output_path)
            downloader.download_audio(url)
            dlg = CustomDialog("Descarga completada.", self)
            
        except Exception as e:
            dlg = CustomDialog(f"Error: {str(e)}", self)

        dlg.exec()
class CustomDialog(QDialog):
    def __init__(self, text_message, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs) 

        self.setWindowTitle("Important!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(text_message)
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()