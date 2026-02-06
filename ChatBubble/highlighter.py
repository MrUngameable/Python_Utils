from PySide6.QtCore import *
from PySide6.QtGui import *


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