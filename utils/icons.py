from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QSize, Qt

from utils.paths import resource_path

_icon_cache: dict[str, QIcon] = {}

def load_icon(
        relative_path: str,
        size: QSize = QSize(24, 24),
) -> QIcon:
    """
    Load and cache icons.
    Supports PNG/JPG/etc natively and SVG via QSvgRenderer.
    """

    cache_key = f"{relative_path}:{size.width()}x{size.height()}"
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]
    
    path = resource_path(relative_path)
    icon = QIcon()

    if path.suffix.lower() == ".svg":
        # Render SVG -> Pixmap
        renderer = QSvgRenderer(str(path))

        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()

        icon.addPixmap(pixmap)
    
    else:
        # PNG, JPG, ICO, etc
        icon = QIcon(str(path))
    
    _icon_cache[cache_key] = icon
    return icon