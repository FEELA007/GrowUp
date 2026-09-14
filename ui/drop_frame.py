from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
#drop funtion
class DropFrame(QFrame):
    file_dropped = Signal(str)
    #making drop box setup
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
    # event 
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    #takes files 
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if path:
                self.file_dropped.emit(path)
            event.acceptProposedAction()