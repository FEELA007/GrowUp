import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import GrowUp
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("GrowUp")
    window = GrowUp()
    window.show()
    sys.exit(app.exec())
