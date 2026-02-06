from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys

from ChatBubble.bubble import ChatBubble
from ChatBubble.blocks.parser import BlockParser

from utils.style import load_stylesheet

# -----------------------------
class ChatBubbleDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatBubble API – Full Demo")
        self.resize(760, 700)

        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.chat_layout = QVBoxLayout(container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(14)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        self._add_demo_messages()

    def _add_demo_messages(self):
        parser = BlockParser()

        content = """
## Welcome to the ChatBubble API

This demo showcases **all supported blocks**.

---

### Code Example

```python
def hello():
    print("Hello from ChatBubble!")
```

### Useful Links
Check out [Qt for Python](https://doc.qt.io/qtforpython-6/)

---

### Actions
[[button:Run Code|{"action":"run"}]]
[[button:Open Docs|{"action":"docs"}]]
"""
        blocks = parser.parse(content)

        bubble = ChatBubble(role="assistant")
        bubble.add_blocks(blocks)
        
        self.chat_layout.addWidget(bubble)


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load default theme
    load_stylesheet(app, "ChatBubble/theme.qss")

    demo = ChatBubbleDemo()
    demo.show()

    sys.exit(app.exec())