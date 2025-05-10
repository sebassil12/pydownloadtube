from PyQt5.QtWidgets import (
    QApplication, QPushButton, QMainWindow, QLabel, QLineEdit, 
    QVBoxLayout, QHBoxLayout, QWidget, QDialog, QDialogButtonBox, QGridLayout, QProgressBar
)
from PyQt5.QtCore import QThread, pyqtSignal
import sys
from download import Download


class DownloadThread(QThread):
    """
    Thread to handle the download process.
    """
    status_signal = pyqtSignal(str)  # Signal to update the status
    error_signal = pyqtSignal(str)   # Signal to handle errors

    def __init__(self, url, output_path):
        super().__init__()
        self.url = url
        self.output_path = output_path

    def run(self):
        """
        Executes the download process in a separate thread.
        """
        try:
            downloader = Download(self.output_path)
            downloader.download_audio(self.url)
            self.status_signal.emit("Download completed successfully!")
        except Exception as e:
            self.error_signal.emit(f"Error: {str(e)}\nIf possible, try with another video.")


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
        self.status_label = QLabel("")  # Label to show the download status

        # Create input fields
        self.input = QLineEdit()
        self.input_path_download = QLineEdit()

        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Create the clear button
        self.clear_button = QPushButton("Limpiar")
        self.clear_button.clicked.connect(self.input.clear)
        self.clear_button.clicked.connect(self.input_path_download.clear)
        # Create the download button
        self.button = QPushButton("Descargar")
        self.button.clicked.connect(self.start_download)

        # Set up the layout
        layout = QGridLayout()
        layout.addWidget(self.label_path_download, 0, 0)
        layout.addWidget(self.input_path_download, 0, 1)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.input, 1, 1)
        layout.addWidget(self.progress_bar, 2, 0, 1, 2)
        layout.addWidget(self.status_label, 3, 0, 1, 2)
        layout.addWidget(self.button, 4, 0, 1, 2)  # Span the button across two columns

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
            QProgressBar {
                font-size: 14px;
                text-align: center;
            }
        """)

    def start_download(self):
        """
        Starts the download process in a separate thread.
        """
        url = self.input.text()
        output_path = self.input_path_download.text()

        # Validate inputs
        if not url:
            self.show_message("Error: Please provide a valid YouTube URL.")
            return

        if not output_path:
            self.show_message("Error: Please provide a valid download path.")
            return

        # Reset progress bar and status label
        self.progress_bar.setValue(0)
        self.status_label.setText("Downloading...")

        # Start the download thread
        self.download_thread = DownloadThread(url, output_path)
        self.download_thread.status_signal.connect(self.on_download_complete)
        self.download_thread.error_signal.connect(self.on_download_error)
        self.download_thread.start()

    def on_download_complete(self, message):
        """
        Handles the completion of the download.
        """
        self.progress_bar.setValue(100)
        self.status_label.setText(message)

    def on_download_error(self, error_message):
        """
        Handles errors during the download process.
        """
        self.progress_bar.setValue(0)
        self.status_label.setText(error_message)

    def show_message(self, message):
        """
        Displays a message in a dialog box.
        """
        dlg = CustomDialog(message, self)
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
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

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