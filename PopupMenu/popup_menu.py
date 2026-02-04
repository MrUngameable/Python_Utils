from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


class PopupMenu(QFrame):
    DEFAULT_QSS = """
    QFrame#tool_popup {
        background-color: #2b2b2b;
        border: 1px solid #444;
        border-radius: 8px;
    }
    QPushButton {
        color: #fff;
        background-color: transparent;
        border: none;
        padding: 6px 12px;
        text-align: left;
    }
    QPushButton:hover {
        background-color: #3a3a3a;
    }
    QFrame {
        background-color: #444;
    }
    """

    def __init__(self, parent=None, position="auto", qss: str = None):
        """
        :param parent: Parent widget that triggers this popup.
        :param position: 'top', 'bottom', 'left', 'right' or 'auto'.
        :param qss: Optional custom stylesheet. Defaults to built-in.
        """
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup)
        self.setObjectName("tool_popup")
        
        # Apply default or custom styling
        self.setStyleSheet(qss if qss else self.DEFAULT_QSS)

        self.position = position
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(6)

        self.actions = []
    
    def add_action(self, text: str, callback=None, icon: str = "", submenu=None):
        """
        Adds a new button to the popup menu.
        :param text: Text of the button
        :param callback: Function to call when clicked
        :param icon: Optional icon
        :param submenu: Optional ToolPopup instance for a submenu
        """

        btn_text = f"{icon} {text}" if icon else text
        btn = QPushButton(btn_text)
        btn.setCursor(Qt.PointingHandCursor)
        
        # Handle submenu
        if submenu:
            # Add arrow indicator on the right
            btn.setLayoutDirection(Qt.RightToLeft)
            btn.setText(f"{btn_text} ▶")
            btn.clicked.connect(lambda _, s=submenu, b=btn: s.popup(b))
        elif callback:
            btn.clicked.connect(callback)
            
        self.layout.addWidget(btn)
        self.actions.append(btn)

    def add_divider(self):
        """
        Adds a horizontal divider line to the menu.
        """
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedHeight(1)
        self.layout.addWidget(line)
    
    def popup(self, parent_button: QWidget):
        """
        Shows the popup menu positioned relative to the parent button or parent menu.
        Works for both main menu and submenus.
        """
        parent_pos = parent_button.mapToGlobal(QPoint(0, 0))
        parent_size = parent_button.size()
        self.adjustSize()
        popup_size = self.size()
        screen_geom = QApplication.primaryScreen().availableGeometry()

        x, y = parent_pos.x(), parent_pos.y()

        # Determine if this is a submenu or main menu
        is_submenu = isinstance(parent_button.parentWidget(), QFrame) and parent_button.parentWidget().objectName() == "tool_popup"

        if is_submenu:
            # Default: show to the right of the parent button
            x += parent_size.width()
            y += 0

            # If it overflows screen on the right, open to the left
            if x + popup_size.width() > screen_geom.right():
                x = parent_pos.x() - popup_size.width()
            # If it overflows bottom, shift up
            if y + popup_size.height() > screen_geom.bottom():
                y = screen_geom.bottom() - popup_size.height() - 4
            # Ensure doesn't go off top
            if y < screen_geom.top():
                y = screen_geom.top() + 4
        else:
            # Main popup logic
            if self.position == "top":
                x += (parent_size.width() - popup_size.width()) // 2
                y -= popup_size.height()
            elif self.position == "bottom":
                x += (parent_size.width() - popup_size.width()) // 2
                y += parent_size.height()
            elif self.position == "left":
                x -= popup_size.width()
                y += (parent_size.height() - popup_size.height()) // 2
            elif self.position == "right":
                x += parent_size.width()
                y += (parent_size.height() - popup_size.height()) // 2
            else:  # auto
                if y + parent_size.height() + popup_size.height() < screen_geom.bottom():
                    y += parent_size.height()
                else:
                    y -= popup_size.height()
                x += (parent_size.width() - popup_size.width()) // 2

            # Clamp to screen
            if x + popup_size.width() > screen_geom.right():
                x = screen_geom.right() - popup_size.width() - 4
            if x < screen_geom.left():
                x = screen_geom.left() + 4

        self.move(x, y)
        self.show()