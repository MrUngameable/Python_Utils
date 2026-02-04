from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import re


# -------------------------------------
# Built-in ChatBubble QSS Styling
# -------------------------------------
DEFAULT_CHATBUBBLE_QSS = """
#ChatBubbleUser #ChatBubbleBody {
    background: #1f2933;
    border-radius: 14px;
    padding: 8px;
}

#ChatBubbleAI #ChatBubbleBody {
    background: #0b1220;
    border-radius: 14px;
    padding: 8px;
}

#ChatBubbleText {
    color: #e6edf3;
}

#ChatBubbleCodeBlock {
    background: #0d1117;
    border-radius: 8px;
    border: 1px solid #30363d;
}

#ChatBubbleCodeEditor {
    background: transparent;
    color: #e6edf3;
    font-family: Consolas;
    font-size: 11px;
}

#ChatBubbleCodeLang {
    color: #7d8590;
    font-size: 10px;
}

/* Copy button base */
#ChatBubbleCopyButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #21262d,
        stop:1 #161b22
    );
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 4px 10px;
    font-weight: 600;
}

/* Hover */
#ChatBubbleCopyButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #30363d,
        stop:1 #21262d
    );
    border: 1px solid #58a6ff;
}

/* Pressed */
#ChatBubbleCopyButton:pressed {
    background: #0d1117;
    border: 1px solid #1f6feb;
    padding-top: 5px;
    padding-left: 11px;
}

/* Focus */
#ChatBubbleCopyButton:focus {
    border: 1px solid #79c0ff;
}

/* Disabled */
#ChatBubbleCopyButton:disabled {
    background: #0d1117;
    color: #6e7681;
    border: 1px solid #30363d;
}

/* Copied success */
#ChatBubbleCopyButton[copySuccess="true"] {
    background: #238636;
    border: 1px solid #2ea043;
    color: white;
}
"""

def apply_default_chatbubble_theme(app: QApplication):
    """Call once in your app to apply default ChatBubble styling."""
    app.setStyleSheet(app.styleSheet() + DEFAULT_CHATBUBBLE_QSS)


# -------------------------------------
# Syntax Highlighter
# -------------------------------------
class CodeHighlighter(QSyntaxHighlighter):
    def __init__(self, document, language=""):
        super().__init__(document)
        self.language = language
        self.rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#ff7b72"))
        keyword_format.setFontWeight(QFont.Bold)

        if language == "python":
            keywords = ["def", "class", "import", "from", "return", "if", "else", "elif", "for", "while", "in", "None", "True", "False"]
            for word in keywords:
                self.rules.append((QRegularExpression(rf"\b{word}\b"), keyword_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#a5d6ff"))
        self.rules.append((QRegularExpression(r'".*?"|\'.*?\''), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#8b949e"))
        self.rules.append((QRegularExpression(r"#.*"), comment_format))
    
    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

# -------------------------------------
# Code Block Widget
# -------------------------------------
class CodeBlock(QFrame):
    def __init__(self, code: str, language="text"):
        super().__init__()
        self.setObjectName("ChatBubbleCodeBlock")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        # Header - language label and copy button
        header = QHBoxLayout()
        lang_label = QLabel(language.upper())
        lang_label.setObjectName("ChatBubbleCodeLang")

        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setObjectName("ChatBubbleCopyButton")
        self.copy_btn.clicked.connect(self._copy)

        header.addWidget(lang_label)
        header.addStretch()
        header.addWidget(self.copy_btn)
        layout.addLayout(header)

        # Code Editor
        self.editor = QPlainTextEdit()
        self.editor.setObjectName("ChatBubbleCodeEditor")
        self.editor.setPlainText(code)
        self.editor.setReadOnly(True)
        self.editor.setFrameShape(QFrame.NoFrame)
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(self.editor)

        # Syntax Highlighting
        CodeHighlighter(self.editor.document(), language)

        # Resize editor dynamically
        def resize_editor():
            doc_height = self.editor.document().size().height()
            # THE CODE BLOCK RESIZING IS BROKEN SINCE IT IS FIXED FOR
            # EVERY CODE BLOCK MESSAGE
            self.editor.setFixedHeight(int(doc_height + 200))
            self.editor.updateGeometry()
    
        self.editor.document().contentsChanged.connect(resize_editor)
        resize_editor()

    
    def _copy(self):
        QApplication.clipboard().setText(self.editor.toPlainText())
        self.copy_btn.setText("Copied!")
        self.copy_btn.setProperty("copySuccess", True)
        self.copy_btn.style().unpolish(self.copy_btn)
        self.copy_btn.style().polish(self.copy_btn)
        QTimer.singleShot(1200, self._reset_copy_btn)
    
    def _reset_copy_btn(self):
        self.copy_btn.setText("Copy")
        self.copy_btn.setProperty("copySuccess", False)
        self.copy_btn.style().unpolish(self.copy_btn)
        self.copy_btn.style().polish(self.copy_btn)

# -------------------------------------
# Main ChatBubble API
# -------------------------------------
class ChatBubble(QFrame):
    def __init__(
            self,
            content: str,
            role: str = "assistant",    # "user" or "assistant"
            avatar=None,
            enable_code_blocks=True,
            enable_copy_button=True,
            max_width=520
    ):
        super().__init__()
        
        self.role = role
        self.content = content
        self.avatar = avatar
        self.enable_code_blocks = enable_code_blocks
        self.enable_copy_button = enable_copy_button
        self.max_width = max_width

        self.setObjectName("ChatBubbleUser" if role == "user" else "ChatBubbleAI")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.setSpacing(6)

        self._build()
        self._fade_in()

    # -----------------------
    # Public API
    # -----------------------
    def set_content(self, content: str):
        self.content = content
        self._build()
    
    def append_stream(self, chunk: str):
        self.content += chunk
        if hasattr(self, "text_view"):
            cursor = self.text_view.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(chunk)
            self.text_view.setTextCursor(cursor)
            self._resize_text_view(self.text_view)
    
    def set_role(self, role: str):
        self.role = role
        self.setObjectName("ChatBubbleUser" if role == "user" else "ChatBubbleAI")
        self._build()

    # -----------------------
    # Internal Rendering
    # -----------------------
    def _build(self):
        # Clear layout
        while self.layout.count():
            w = self.layout.takeAt(0).widget()
            if w:
                w.deleteLater()

        # Avatar
        avatar = self._build_avatar() if self.avatar else None
        body = self._build_body()

        if self.role == "user":
            self.layout.addStretch()
            self.layout.addWidget(body)
            if avatar:
                self.layout.addWidget(avatar)
        
        else:
            if avatar:
                self.layout.addWidget(avatar)
            self.layout.addWidget(body)
            self.layout.addStretch()

    def _build_body(self):
        container = QFrame()
        container.setObjectName("ChatBubbleBody")
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        container.setMaximumWidth(self.max_width + 32)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)

        parts = self._parse_markdown_blocks(self.content)

        for part in parts:
            if part["type"] == "code" and self.enable_code_blocks:
                layout.addWidget(CodeBlock(part["content"], part["lang"]))
            else:
                self.text_view = self._build_text_view(part["content"])
                layout.addWidget(self.text_view)
        
        return container
    
    def _build_text_view(self, text):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        label.setStyleSheet("color: #e6edf3;")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        label.setMaximumWidth(self.max_width)
        label.adjustSize()  # Re-calc height

        return label
    
    def _resize_text_view(self, view: QTextBrowser):
            h = view.document().size().height()
            view.setFixedHeight(int(h + 4))
            view.updateGeometry()

    def _build_avatar(self):
        avatar = QLabel()
        avatar.setObjectName("ChatBubbleAvatar")

        pixmap = self.avatar.pixmap(40, 40) if isinstance(self.avatar, QIcon) else QPixmap(str(self.avatar))
        pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
        # Make circular mask
        mask = QPixmap(40, 40)
        mask.fill(Qt.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.drawEllipse(0, 0, 40, 40)
        painter.end()
        pixmap.setMask(mask.createMaskFromColor(Qt.transparent))

        avatar.setPixmap(pixmap)
        avatar.setFixedSize(40, 40)

        # Glow ring effect
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(18)
        glow.setColor(QColor("#00d4ff"))
        glow.setOffset(0, 0)
        avatar.setGraphicsEffect(glow)

        return avatar
    
    def _parse_markdown_blocks(self, text):
        blocks = []
        pattern = r"```(\w+)?\n(.*?)```"
        last_end = 0

        for match in re.finditer(pattern, text, re.S):
            if match.start() > last_end:
                blocks.append({
                    "type": "text",
                    "content": text[last_end:match.start()]
                })
            
            blocks.append({
                "type": "code",
                "lang": match.group(1) or "text",
                "content": match.group(2).strip()
            })

            last_end = match.end()
        
        if last_end < len(text):
            blocks.append({
                "type": "text",
                "content": text[last_end:]
            })
        
        return blocks
    
    def _fade_in(self):
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)

        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(280)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()

        # keep reference
        self._fade_anim = anim