from PySide6.QtWidgets import QFrame
from .base import Block


class DividerBlock(Block):
    block_type = "divider"

    def __init__(self):
        super().__init__()
        self.setObjectName("ChatBubbleDivider")
        self.setFixedHeight(1)