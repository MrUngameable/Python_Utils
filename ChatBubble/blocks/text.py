from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from .base import Block


class TextBlock(Block):
    block_type = "text"

    def __init__(self, text=""):
        super().__init__()
        self.label = QLabel(text)
        self.label.setObjectName("ChatBubbleText")
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(
            Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse
        )
        self.label.setTextFormat(Qt.RichText)
        self._text = text

        layout = self.layout() or self._init_layout()
        layout.addWidget(self.label)
    
    def _init_layout(self):
        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        return layout
    
    def append(self, text: str):
        self._text += text
        self.label.setText(self._text)
        self.label.adjustSize()