from PySide6.QtWidgets import QWidget


class Block(QWidget):
    """
    Base class for all chat blocks.
    """
    block_type = "base"

    def append(self, text: str):
        """
        Used during streaming (only for streaming-capable blocks).
        """
        pass

    def finalize(self):
        """
        Called once streaming finishes.
        """
        pass