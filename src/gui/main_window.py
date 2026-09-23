from pathlib import Path

from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QPushButton,
)

from src.person_service import PersonService
from src.photo_processor import PhotoProcessor
from src.gui.worker import PhotoProcessingWorker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Photo Organizer")
        self.resize(1000, 700)

        self.person_service = PersonService(
            output_directory="output"
        )
        self.photo_processor = PhotoProcessor(
            threshold=0.5,
            output_directory="output"
        )

        self.selected_folder = None

        self.thread = None
        self.worker = None

        self.setup_ui()
        self.load_people()

    def setup_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        title = QLabel("People")
        title.setStyleSheet(
            "font-size: 28px; "
            "font-weight: bold; "
            "padding: 10px;"
        )

        self.people_container = QWidget()

        self.people_layout = QGridLayout(
            self.people_container
        )

        self.people_layout.setSpacing(20)

        select_button = QPushButton(
            "Select Photo Folder"
        )

        select_button.clicked.connect(
            self.select_folder
        )

        

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(
            self.people_container
        )

        self.folder_label = QLabel(
            "No folder selected"
        )

        self.process_button = QPushButton(
            "Process Photos"
        )

        self.process_button.clicked.connect(
            self.process_photos
        )

        main_layout.addWidget(title)
        main_layout.addWidget(select_button)
        main_layout.addWidget(self.folder_label)
        main_layout.addWidget(self.process_button)
        main_layout.addWidget(scroll_area)

        central_widget.setLayout(
            main_layout
        )

        self.setCentralWidget(
            central_widget
        )

    def load_people(self):
        people = (
            self.person_service.load_people()
        )

        columns = 5

        for index, person in enumerate(people):
            row = index // columns
            column = index % columns

            person_widget = (
                self.create_person_widget(
                    person
                )
            )

            self.people_layout.addWidget(
                person_widget,
                row,
                column
            )

    def create_person_widget(self, person):
        widget = QWidget()

        layout = QVBoxLayout()

        image_label = QLabel()
        image_label.setFixedSize(160, 160)

        image_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        image_label.setStyleSheet(
            "border: 1px solid #cccccc;"
        )

        image_path = Path(
            person["main_image_path"]
        )

        if image_path.exists():
            pixmap = QPixmap(
                str(image_path)
            )

            pixmap = pixmap.scaled(
                150,
                150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            image_label.setPixmap(pixmap)

        else:
            image_label.setText(
                "No Image"
            )

        name_label = QLabel(
            person["name"]
        )

        name_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        name_label.setStyleSheet(
            "font-size: 16px;"
        )

        layout.addWidget(image_label)
        layout.addWidget(name_label)

        widget.setLayout(layout)

        return widget


    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Photo Folder"
        )

        if not folder:
            return

        self.selected_folder = folder

        self.folder_label.setText(
            f"Selected folder: {folder}"
        )

        print("Selected folder:", folder)


    def process_photos(self):
        if self.selected_folder is None:
            print("Please select a folder first.")
            return

        self.process_button.setEnabled(False)

        self.thread = QThread()
        self.worker = PhotoProcessingWorker(
            self.photo_processor,
            self.selected_folder
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.processing_finished
        )

        self.worker.error.connect(
            self.processing_error
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.finished.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread_finished
        )
        
        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.start()


    def processing_finished(self):
        print("Processing finished.")

        self.process_button.setEnabled(True)

        self.load_people()



    def processing_error(self, message):
        print(
            f"Processing error: {message}"
        )

    def thread_finished(self):
        print("Worker thread finished.")

        self.worker = None
        self.thread = None