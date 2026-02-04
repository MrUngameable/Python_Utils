from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys

from PopupMenu.popup_menu import PopupMenu

# --- Demo functions for actions ---
def attach_files():
    print("Attach files clicked!")

def create_image():
    print("Create image clicked!")

def web_search():
    print("Web search clicked!")

def deep_search():
    print("Deep search clicked!")

def option_a1():
    print("Submenu Option A1 clicked!")

def option_a2():
    print("Submenu Option A2 clicked!")


# --- Demo App ---
class DemoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Popup Menu Demo with Submenus")
        self.resize(400, 300)
        layout = QVBoxLayout(self)
        self.label = QLabel("Click the button to open the Popup Menu menu")
        layout.addWidget(self.label)

        self.btn_show_popup = QPushButton("Open Popup Menu Menu")
        layout.addWidget(self.btn_show_popup)

        # Submenu
        submenu = PopupMenu()
        submenu.add_action("Option A1", callback=option_a1)
        submenu.add_action("Option A2", callback=option_a2)

        # Main menu
        self.popup_menu = PopupMenu(position="auto")
        self.popup_menu.add_action("Add photos & files", callback=attach_files, icon="📎")
        self.popup_menu.add_divider()
        self.popup_menu.add_action("Advanced Options", submenu=submenu, icon="⚙️")
        self.popup_menu.add_action("Create image", callback=create_image, icon="🖼️")
        self.popup_menu.add_action("Web search", callback=web_search, icon="🌐")
        self.popup_menu.add_action("Deep search", callback=deep_search, icon="🔎")

        self.btn_show_popup.clicked.connect(lambda: self.popup_menu.popup(self.btn_show_popup))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = DemoApp()
    demo.show()
    sys.exit(app.exec())