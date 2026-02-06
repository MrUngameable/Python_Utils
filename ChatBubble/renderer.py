from PySide6.QtWidgets import QVBoxLayout


class BlockRenderer:
    def __init__(self, container):
        self.layout = QVBoxLayout(container)
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(0, 0, 0, 0)
    
    def add_block(self, block):
        self.layout.addWidget(block)