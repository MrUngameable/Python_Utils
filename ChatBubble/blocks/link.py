from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from .base import Block
import html


class LinkBlock(Block):
    """
    A clickable hyperlink block.
    """
    block_type = "link"

    def __init__(self, text: str, url: str):
        super().__init__()

        safe_text = html.escape(text)
        safe_url = html.escape(url)

        label = QLabel(
            f'<a href="{safe_url}">{safe_text}</a>'
        )
        label.setOpenExternalLinks(True)
        label.setTextInteractionFlags(
            Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse
        )
        label.setStyleSheet("""
            QLabel {
                color: #58a6ff;
                font-size: 13px;
            }
            QLabel:hover {
                text-decoration: underline;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.addWidget(label)