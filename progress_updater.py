from abc import ABC, abstractmethod
from PySide2.QtCore import QObject, Signal

class ProgressUpdater(ABC):
    @abstractmethod
    def update_progress(self, progress):
        pass

    @abstractmethod
    def update_status(self, message):
        pass

class CommandLineUpdater(ProgressUpdater):
    def update_progress(self, progress):
        print(f"Progress: {progress}%")

    def update_status(self, message):
        print(message)

class GUIUpdater(QObject):
    status_updated = Signal(str)
    progress_updated = Signal(int)

    def __init__(self, progressBar, statusLabel):
        super().__init__()  # 注意呼叫 QObject 的構造函數
        self.progressBar = progressBar
        self.statusLabel = statusLabel
        # 連接信號到槽
        self.status_updated.connect(self.statusLabel.setText)
        self.progress_updated.connect(self.progressBar.setValue)
    
    def update_status(self, message):
        self.status_updated.emit(message)
    
    def update_progress(self, progress):
        self.progress_updated.emit(progress)

