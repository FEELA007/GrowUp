from pathlib import Path

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SettingsPage(QWidget):

    def __init__(self, window):
        super().__init__()

        self.window = window

        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        sidebar = QFrame()
        sidebar.setObjectName("settingsSidebar")
        sidebar.setFixedWidth(210)

        sidebar_layout = QVBoxLayout(sidebar)
        title = QLabel("Settings")
        title.setObjectName("settingsTitle")
        sidebar_layout.addWidget(title)

        for name in [
            "General",
            "Appearance",
            "Processing",
            "Performance",
            "Updates",
            "Privacy",
            "About",
        ]:
            sidebar_layout.addWidget(QPushButton(name))

        sidebar_layout.addStretch()
        layout.addWidget(sidebar)

        content = QFrame()
        content.setObjectName("settingsContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 30, 30, 30)

        heading = QLabel("General")
        heading.setObjectName("heading")
        content_layout.addWidget(heading)
        content_layout.addWidget(QLabel("Default save location"))

        save_layout = QHBoxLayout()
        self.save_location = QLineEdit()
        self.save_location.setText(str(Path.home() / "Pictures" / "GrowUp"))

        change = QPushButton("Change")
        change.clicked.connect(self.change_save_location)
        save_layout.addWidget(self.save_location)
        save_layout.addWidget(change)
        content_layout.addLayout(save_layout)

        content_layout.addWidget(QCheckBox("Ask where to save each image"))
        content_layout.addWidget(QCheckBox("Open output folder after processing"))

        content_layout.addSpacing(25)
        content_layout.addWidget(QLabel("Theme"))
        self.theme = QComboBox()
        self.theme.addItems(["System", "Light", "Dark"])
        self.theme.currentTextChanged.connect(self.window.change_theme)
        content_layout.addWidget(self.theme)

        content_layout.addSpacing(25)
        content_layout.addWidget(QLabel("Default upscale"))
        self.default_scale = QComboBox()
        self.default_scale.addItems(["2×", "4×"])
        content_layout.addWidget(self.default_scale)
        content_layout.addStretch()

        layout.addWidget(content, 1)

    def change_save_location(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Save Location")
        if folder:
            self.save_location.setText(folder)
