
from PySide6.QtCore import QObject, Signal, Slot


class PhotoProcessingWorker(QObject):
    progress = Signal(int, int, str,int,int,int)
    finished = Signal()
    error = Signal(str)

    def __init__(self, photo_processor, folder):
        super().__init__()
        self.photo_processor = photo_processor
        self.folder = folder

    @Slot()
    def run(self):
        try:
            self.photo_processor.process_directory(
                self.folder,
                progress_callback=self.report_progress
            )
        except Exception as exc:
            self.error.emit(str(exc))
        finally:
            self.finished.emit()

    
        
    def report_progress(
        self,
        current,
        total,
        image_path,
        processed,
        skipped,
        failed
    ):
        self.progress.emit(
            current,
            total,
            str(image_path),
            processed,
            skipped,
            failed
        )


