from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QPlainTextEdit
)
from PySide6.QtCore import Qt, QTimer
from .base import Block
from ..highlighter import CodeHighlighter

class CodeBlock(Block):
    block_type = "code"

    def __init__(self, code:str, language="text"):
        super().__init__()
        self.language = language
        self.code = code

        self.setObjectName("ChatBubbleCodeBlock")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)

        header = QHBoxLayout()
        self.lang_label = QLabel(language.upper())
        self.lang_label.setObjectName("ChatBubbleCodeLang")

        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setObjectName("ChatBubbleCopyButton")
        self.copy_btn.clicked.connect(self.copy)

        header.addWidget(self.lang_label)
        header.addStretch()
        header.addWidget(self.copy_btn)
        layout.addLayout(header)

        self.editor = QPlainTextEdit()
        self.editor.setObjectName("ChatBubbleCodeEditor")
        self.editor.setReadOnly(True)
        self.editor.setFrameShape(QFrame.NoFrame)
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Show the code and resize the editor accordingly
        self.editor.setPlainText(self.code)
        self._resize()

        layout.addWidget(self.editor)

        CodeHighlighter(self.editor.document(), language)
    
    def append(self, text: str):
        self.code += text
        self.editor.setPlainText(self.code)
        self._resize()
    
    def finalize(self):
        self._resize()
    
    def _resize(self):
        h = self.editor.document().size().height()
        self.editor.setFixedHeight(int(h + 16))
    
    def copy(self):
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.code)
        self.copy_btn.setText("✓ Copied")
        QTimer.singleShot(1200, lambda: self.copy_btn.setText("Copy"))