from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

# for dark theme
DARK = {
    "window": "#08090B",
    "bar": "#0D0F12",
    "panel": "#111317",
    "control": "#191C22",
    "border": "#252A33",
    "text": "#FFFFFF",
    "muted": "#8B919C",
    "blue": "#2F80FF",
    "blue_hover": "#4A91FF",
}
#--------------------------------------------------------------------------------------------
# fro light theme
LIGHT = {
    "window": "#F5F6F8",
    "bar": "#FFFFFF",
    "panel": "#FFFFFF",
    "control": "#EEF0F4",
    "border": "#DDE1E8",
    "text": "#111318",
    "muted": "#6D7480",
    "blue": "#25DB89",
    "blue_hover": "#0CF4AB",
}
#----------------------------------------------------------------------------------------------------
#title bar 
class TitleBar(QFrame):
    # basic setup
    def __init__(self, window):
        #layout 
        super().__init__()
        self.window = window
        self.drag_position = QPoint()
        self.setFixedHeight(54)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 0, 0)
        layout.setSpacing(0)
        #----------------------------------------------------------------
        #logo 
        self.logo = QLabel("G")
        self.logo.setFixedSize(30, 30)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_font = QFont("Arial")
        logo_font.setPointSize(17)
        logo_font.setWeight(QFont.Weight.Bold)
        self.logo.setFont(logo_font)
        layout.addWidget(self.logo)
    #----------------------------------------------------------------
        #name of app 
        self.name = QLabel("GrowUp")
        name_font = QFont("Arial")
        name_font.setPointSize(15)
        name_font.setWeight(QFont.Weight.DemiBold)
        self.name.setFont(name_font)
        self.name.setContentsMargins(9, 0, 28, 0)
        layout.addWidget(self.name)
    #----------------------------------------------------------------
        #buttons
        self.enhance_btn = self.nav_button("Enhance")
        self.restore_btn = self.nav_button("Restore")
        self.history_btn = self.nav_button("History")
        self.settings_btn = self.nav_button("Settings")
        layout.addWidget(self.enhance_btn)
        layout.addWidget(self.restore_btn)
        layout.addWidget(self.history_btn)
        layout.addWidget(self.settings_btn)
        layout.addStretch()
    #----------------------------------------------------------------
        #windows buttons
        self.min_btn = self.window_button("−")
        self.max_btn = self.window_button("□")
        self.close_btn = self.window_button("×")
        self.min_btn.clicked.connect(self.window.showMinimized)
        self.max_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(self.window.close)
        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)
        self.apply_theme(DARK)
    #----------------------------------------------------------------
    #navigation button 
    def nav_button(self, text):
        button = QPushButton(text)
        button.setFixedHeight(54)
        return button
    #----------------------------------------------------------------
    #windows button activation
    def window_button(self, text):
        button = QPushButton(text)
        button.setFixedSize(46, 54)
        button.setFont(QFont("Segoe UI Symbol", 15))
        return button
    #----------------------------------------------------------------
    # maximize / restore  
    def toggle_maximize(self):
        if self.window.isMaximized():
            self.window.showNormal()
        else:
            self.window.showMaximized()
    #----------------------------------------------------------------
    # apply theme of ui 
    def apply_theme(self, theme):
        self.setStyleSheet(f"""QFrame {{background: {theme["bar"]};border-bottom: 1px solid {theme["border"]};}}""")
        self.logo.setStyleSheet(f"""QLabel {{background: {theme["blue"]};color: white;border-radius: 8px;}}""")
        self.name.setStyleSheet(f"""QLabel {{color: {theme["text"]};background: transparent;}}""")
        for button in [self.enhance_btn,self.restore_btn,self.history_btn,self.settings_btn,]:
            button.setStyleSheet(f"""QPushButton {{color: {theme["muted"]};background: transparent;border: none;padding: 0 14px;font-size: 13px;}}QPushButton:hover {{color: {theme["text"]};background: {theme["control"]};}}""")
        for button in [self.min_btn, self.max_btn, self.close_btn]:
            button.setStyleSheet(f"""QPushButton {{color: {theme["muted"]};background: transparent;border: none;font-size: 17px;}}QPushButton:hover {{color: {theme["text"]};background: {theme["control"]};}}""")
    #----------------------------------------------------------------       
    # window drag
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            current = event.globalPosition().toPoint()
            delta = current - self.drag_position
            self.window.move(self.window.pos() + delta)
            self.drag_position = current
