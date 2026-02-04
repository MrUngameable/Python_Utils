from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys

from ChatBubble.chat_bubble import ChatBubble, apply_default_chatbubble_theme


# -----------------------------
class ChatDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatBubble Demo")
        self.resize(700, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Scroll area for chat messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(12)
        self.scroll_area.setWidget(self.chat_container)

        layout.addWidget(self.scroll_area)

        # Input box to send messages
        self.input_box = QPlainTextEdit()
        self.input_box.setPlaceholderText("Type your message here...")
        self.input_box.setFixedHeight(80)
        layout.addWidget(self.input_box)

        send_btn = QPushButton("Send Message")
        send_btn.clicked.connect(self.send_message)
        layout.addWidget(send_btn)

        # Demo: add some long messages and code
        self.add_demo_messages()

    def add_demo_messages(self):
        # Long text message
        short_text = "This is a short message. "
        bubble1 = ChatBubble(short_text, role="user")
        self.chat_layout.addWidget(bubble1)

        # Multi-line code block
        code_text = '''def fibonacci(n):
    a, b = 0, 1
    result = []
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

print(fibonacci(10))'''
        bubble2 = ChatBubble(f"Here is some Python code:\n```python\n{code_text}\n```", role="assistant")
        self.chat_layout.addWidget(bubble2)

        # Another long text message
        long_text2 = "And here is another message that should wrap correctly and expand the bubble as needed. " * 4
        bubble3 = ChatBubble(long_text2, role="assistant")
        self.chat_layout.addWidget(bubble3)

        # Scroll to bottom
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def send_message(self):
        text = self.input_box.toPlainText()
        if not text.strip():
            return
        bubble = ChatBubble(text, role="user")
        self.chat_layout.addWidget(bubble)
        self.input_box.clear()

        # Scroll to bottom
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply default ChatBubble styling
    apply_default_chatbubble_theme(app)

    demo = ChatDemo()
    demo.show()

    sys.exit(app.exec())