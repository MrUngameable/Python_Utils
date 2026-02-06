from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from .base import Block


class HeadingBlock(Block):
    """
    Section heading (H1-H4 style).
    """
    block_type = "heading"

    def __init__(self, text: str, level: int = 2):
        super().__init__()
        level = max(1, min(level, 4))

        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        size_map = {
            1: "22px",
            2: "18px",
            3: "15px",
            4: "13px",
        }

        weight_map = {
            1: "700",
            2: "600",
            3: "600",
            4: "500",
        }

        label.setStyleSheet(f"""
            color: #e6edf3;
            font-size: {size_map[level]};
            font-weight: {weight_map[level]};
            margin-top: 8px;
            margin-bottom: 4px;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label)