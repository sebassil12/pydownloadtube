from PyQt5.QtWidgets import (
    QApplication, QPushButton, QMainWindow, QLabel, QLineEdit, 
    QVBoxLayout, QHBoxLayout, QWidget, QDialog, QDialogButtonBox, QGridLayout
)
import sys
from download import Download


class MainWindow(QMainWindow):
    """
    Main application window for the YouTube music downloader.
    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Set up the main window
        self.setWindowTitle("Download YouTube Music")
        self.setGeometry(100, 100, 800, 600)

        # Create labels
        self.label = QLabel("Introduce la URL del video de YouTube:")
        self.label_path_download = QLabel("Introduce la ruta donde se guardan tus descargas:")

        # Create input fields
        self.input = QLineEdit()
        self.input_path_download = QLineEdit()

        # Create the download button
        self.button = QPushButton("Download")
        self.button.clicked.connect(self.download_audio)

        # Set up the layout
        layout = QGridLayout()
        layout.addWidget(self.label_path_download, 0, 0)
        layout.addWidget(self.input_path_download, 0, 1)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.input, 1, 1)
        layout.addWidget(self.button, 2, 0, 1, 2)  # Span the button across two columns

        # Create a container widget and set the layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Apply styles to the UI
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
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

    def download_audio(self):
        """
        Handles the download process when the "Download" button is clicked.
        """
        output_path = self.input_path_download.text()
        url = self.input.text()

        # Validate inputs
        if not url:
            dlg = CustomDialog("Error: Please provide a valid YouTube URL.", self)
            dlg.exec()
            return

        if not output_path:
            dlg = CustomDialog("Error: Please provide a valid download path.", self)
            dlg.exec()
            return

        # Attempt to download the audio
        try:
            downloader = Download(output_path)
            downloader.download_audio(url)
            dlg = CustomDialog("Download completed successfully!", self)
        except Exception as e:
            dlg = CustomDialog(f"Error: {str(e)}\nIf possible, try with another video.", self)

        dlg.exec()


class CustomDialog(QDialog):
    """
    Custom dialog for displaying messages to the user.
    """
    def __init__(self, text_message, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        # Set up the dialog window
        self.setWindowTitle("Important!")

        # Create dialog buttons
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Set up the layout
        layout = QVBoxLayout()
        message = QLabel(text_message)
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


# Entry point for the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()