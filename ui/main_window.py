from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from ui.enhance_page import EnhancePage
from ui.settings_page import SettingsPage
from ui.title_bar import DARK, LIGHT, TitleBar


class GrowUp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_theme = DARK
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.resize(1200, 750)
        self.build_ui()
        self.apply_theme(DARK)

    def build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_bar = TitleBar(self)
        layout.addWidget(self.title_bar)

        self.pages = QStackedWidget()
        self.enhance_page = EnhancePage(self)
        self.settings_page = SettingsPage(self)
        self.pages.addWidget(self.enhance_page)
        self.pages.addWidget(self.settings_page)
        layout.addWidget(self.pages)

        self.title_bar.enhance_btn.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.title_bar.restore_btn.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.title_bar.history_btn.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.title_bar.settings_btn.clicked.connect(lambda: self.pages.setCurrentIndex(1))

    def change_theme(self, theme_name):
        if theme_name == "Light":
            self.current_theme = LIGHT
        elif theme_name == "Dark":
            self.current_theme = DARK
        else:
            self.current_theme = DARK

        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        self.setStyleSheet(
            f"""
            QMainWindow {{
                background: {theme["window"]};
            }}

            QWidget {{
                color: {theme["text"]};
                font-family: "Segoe UI";
                font-size: 13px;
            }}

            QLabel#subtitle {{
                color: {theme["muted"]};
                font-size: 13px;
            }}

            QLabel#heading {{
                color: {theme["text"]};
                font-size: 20px;
                font-weight: 600;
            }}

            QLabel#sectionLabel {{
                color: {theme["muted"]};
            }}

            QLabel#dropText {{
                color: {theme["muted"]};
                font-size: 19px;
            }}

            QLabel#info {{
                color: {theme["muted"]};
            }}

            QFrame#preview {{
                background: {theme["panel"]};
                border: 1px solid {theme["border"]};
                border-radius: 14px;
            }}

            QFrame#panel {{
                background: {theme["panel"]};
                border: 1px solid {theme["border"]};
                border-radius: 14px;
            }}

            QFrame#settingsSidebar {{
                background: {theme["panel"]};
                border: 1px solid {theme["border"]};
                border-radius: 12px;
            }}

            QFrame#settingsContent {{
                background: {theme["panel"]};
                border: 1px solid {theme["border"]};
                border-radius: 12px;
            }}

            QLabel#settingsTitle {{
                font-size: 22px;
                font-weight: 600;
                padding-bottom: 15px;
            }}

            QPushButton {{
                color: {theme["text"]};
                background: {theme["control"]};
                border: 1px solid {theme["border"]};
                border-radius: 8px;
                padding: 10px 16px;
            }}

            QPushButton:hover {{
                background: {theme["border"]};
            }}

            QPushButton:checked {{
                background: {theme["blue"]};
                border-color: {theme["blue"]};
                color: white;
            }}

            QPushButton#primaryButton {{
                background: {theme["blue"]};
                color: white;
                border: none;
                font-weight: 700;
                font-size: 14px;
            }}

            QPushButton#primaryButton:hover {{
                background: {theme["blue_hover"]};
            }}

            QLineEdit,
            QComboBox {{
                background: {theme["control"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 7px;
                padding: 9px;
            }}

            QSlider::groove:horizontal {{
                height: 4px;
                background: {theme["border"]};
                border-radius: 2px;
            }}

            QSlider::handle:horizontal {{
                width: 14px;
                height: 14px;
                margin: -5px 0;
                background: {theme["blue"]};
                border-radius: 7px;
            }}

            QCheckBox {{
                spacing: 8px;
            }}
            """
        )
        self.title_bar.apply_theme(theme)
