from PySide6.QtWidgets import QFrame, QHBoxLayout
from PySide6.QtCore import QEasingCurve, QPropertyAnimation

from .blocks.parser import BlockParser
from .renderer import BlockRenderer


class ChatBubble(QFrame):
    def __init__(self, role="assistant"):
        super().__init__()
        self._stream_buffer = ""

        self.setObjectName("ChatBubbleUser" if role == "user" else "ChatBubbleAI")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        self.body = QFrame()
        self.body.setObjectName("ChatBubbleBody")
        self.body.setFrameShape(QFrame.NoFrame)
        self.renderer = BlockRenderer(self.body)
        layout.addWidget(self.body)

        self.parser = BlockParser()  
        self._fade_in()

    # ---------------------------------
    # BLOCK-BASED API (NEW, STABLE)
    # ---------------------------------
    def add_block(self, block):
        self.renderer.add_block(block)
    
    def add_blocks(self, blocks):
        for block in blocks:
            self.add_block(block)

    # ---------------------------------
    # STREAMING TEXT API (LEGACY / LIVE)
    # ---------------------------------
    def append_stream(self, text: str):
        """
        Streaming-safe: accepts RAW TEXT ONLY.
        """
        self._stream_buffer += text
        blocks = self.parser.parse(text)
        for block in blocks:
            self.renderer.add_block(block)
    
    def _fade_in(self):
        anim = QPropertyAnimation(self, b"windowOpacity")

        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setDuration(220)
        anim.setEasingCurve(QEasingCurve.OutCubic)

        anim.start()
        self._anim = anim