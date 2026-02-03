from PySide6.QtWidgets import QApplication
from utils.paths import resource_path

def load_stylesheet(app: QApplication, filename: str = "assets/styles/theme.qss"):
    qss_path = resource_path(filename)

    if not qss_path.exists():
        print(f"[WARNING] QSS file not found {qss_path}")
        return
    
    with qss_path.open("r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())