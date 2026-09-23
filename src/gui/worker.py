from PySide6.QtCore import QObject, Signal, Slot


class PhotoProcessingWorker(QObject):

    finished = Signal()
    error = Signal(str)

    def __init__(
        self,
        photo_processor,
        folder
    ):
        super().__init__()

        self.photo_processor = photo_processor
        self.folder = folder

    @Slot()
    def run(self):
        try:
            self.photo_processor.process_directory(
                self.folder
            )

        except Exception as exc:
            self.error.emit(
                str(exc)
            )

        finally:
            self.finished.emit()