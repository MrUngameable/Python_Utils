from PySide6.QtWidgets import QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from .base import Block


class ButtonBlock(Block):
    """
    A clicable action button inside a chat message.
    """
    block_type = "button"

    clicked = Signal(dict)  # emits payload

    def __init__(self, label: str, payload: dict | None = None):
        super().__init__()
        self.payload = payload or {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setAlignment(Qt.AlignLeft)

        self.button = QPushButton(label)
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.setObjectName("ChatBubbleActionButton")

        self.button.clicked.connect(self._emit)

        layout.addWidget(self.button)
    
    def _emit(self):
        self.clicked.emit(self.payload)