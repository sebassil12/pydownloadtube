from PyQt5.QtWidgets import (
    QApplication, QPushButton, QMainWindow, QLabel, QLineEdit, 
    QVBoxLayout, QHBoxLayout, QWidget, QDialog, QDialogButtonBox, QGridLayout, QProgressBar, QMenuBar, QAction, QFileDialog
)
from PyQt5.QtCore import QThread, pyqtSignal
import os
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
        self._is_running = True  # Flag to control the thread's execution

    def run(self):
        """
        Executes the download process in a separate thread.
        """
        try:
            downloader = Download(self.output_path)

            # Check periodically if the thread should stop
            def progress_hook(d):
                if not self._is_running:
                    raise Exception("Descarga interrumpida por usuario.")
                if d['status'] == 'error':
                    raise Exception(d.get('error', 'Unknown error occurred.'))

            downloader.download_audio(self.url, progress_hook=progress_hook)
            if self._is_running:
                # Emit success message to the thread
                self.status_signal.emit("¡Deacarga completada exitosamenta!")
        except Exception as e:
                # Emit error message to the thread
            self.error_signal.emit(f"Error: {str(e)}\nSi es posible intenta con otro video, lyric video quizá.")

    def stop(self):
        """
        Stops the thread by setting the _is_running flag to False.
        """
        self._is_running = False


class SettingsDialog(QDialog):
    """
    Dialog for configuring application settings.
    """
    def __init__(self, current_path, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Configuraciones")
        self.current_path = current_path

        # Create widgets
        self.label = QLabel("Ruta de descarga:")
        self.path_input = QLineEdit(self.current_path)
        self.browse_button = QPushButton("Buscar")
        self.browse_button.clicked.connect(self.browse_path)

        # Create dialog buttons
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.path_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def browse_path(self):
        """
        Opens a file dialog to select a folder.
        """
        path = QFileDialog.getExistingDirectory(self, "Selecciona carpeta de descarga")
        if path:
            self.path_input.setText(path)

    def get_path(self):
        """
        Returns the selected path.
        """
        return self.path_input.text()


class MainWindow(QMainWindow):
    """
    Main application window for the YouTube music downloader.
    """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.download_thread = None  # Keep track of the current download thread

        # Default download path
        self.default_download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Set up the main window
        self.setWindowTitle("DeSCargardOr DE música de youtube")
        self.setGeometry(100, 100, 800, 600)

        # Create menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Add "Settings" menu
        settings_menu = menu_bar.addMenu("Configuraciones")
        settings_action = QAction("Configurar ruta de descarga", self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

        # Create labels
        self.label = QLabel("Introduce la URL del video de YouTube:")
        self.status_label = QLabel("")  # Label to show the download status

        # Create input fields
        self.input = QLineEdit()

        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Create the download button
        self.button = QPushButton("Descargar")
        self.button.clicked.connect(self.start_download)

        # Set up the layout
        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.input, 0, 1)
        layout.addWidget(self.progress_bar, 1, 0, 1, 2)
        layout.addWidget(self.status_label, 2, 0, 1, 2)
        layout.addWidget(self.button, 3, 0, 1, 2)  # Span the button across two columns

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

    # Action to open the settings screen
    def open_settings(self):
        """
        Opens the settings dialog to configure the download path.
        """
        dialog = SettingsDialog(self.default_download_path, self)
        if dialog.exec() == QDialog.Accepted:
            self.default_download_path = dialog.get_path()

    def start_download(self):
        """
        Starts the download process in a separate thread.
        """
        url = self.input.text()

        # Validate inputs
        if not url:
            self.show_message("Error: Coloca una URL válida.")
            return

        # Stop the current thread if it is running
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.stop()
            self.download_thread.wait()  # Wait for the thread to finish

        # Reset progress bar and status label
        self.progress_bar.setValue(0)
        self.status_label.setText("Descargando...")

        # Start a new download thread
        self.download_thread = DownloadThread(url, self.default_download_path)
        self.download_thread.status_signal.connect(self.on_download_complete)
        self.download_thread.error_signal.connect(self.on_download_error)
        self.download_thread.start()

    # Signal emit to the thread when the download is complete
    def on_download_complete(self, message):
        """
        Handles the completion of the download.
        """
        self.progress_bar.setValue(100)
        self.status_label.setText(message)

    # Signal emit to the thread when the download stops or fails
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
        self.setWindowTitle("Importante!")

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