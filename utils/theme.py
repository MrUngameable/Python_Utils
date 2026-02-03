from enum import Enum
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt
import subprocess

from utils.paths import resource_path
from utils.system_checker import OSInfo


class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


def detect_system_theme() -> Theme:
    try:
        os_name = OSInfo.get_os()

        # ---------------- WINDOWS ----------------
        if os_name == "windows":
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            ) as key:
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return Theme.LIGHT if value == 1 else Theme.DARK

        # ---------------- MACOS ----------------
        if os_name == "macos":
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return Theme.DARK if result.returncode == 0 else Theme.LIGHT

        # ---------------- LINUX ----------------
        if os_name == "linux":
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                capture_output=True,
                text=True,
            )
            if "dark" in result.stdout.lower():
                return Theme.DARK
            return Theme.LIGHT

    except Exception:
        pass

    return Theme.LIGHT


def _load_qss(filename: str) -> str:
    path = resource_path(f"assets/styles/{filename}")
    if not path.exists():
        print(f"[THEME ERROR] QSS file not found: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def apply_theme(app: QApplication, theme: Theme, animate: bool = True):
    if theme == Theme.SYSTEM:
        theme = detect_system_theme()

    metrics_qss = _load_qss("metrics.qss")
    theme_qss = _load_qss(f"{theme.value}_theme.qss")
    final_qss = metrics_qss + "\n" + theme_qss

    # No animation → instant apply
    if not animate:
        app.setStyleSheet(final_qss)
        return

    window = app.activeWindow()
    if not window:
        app.setStyleSheet(final_qss)
        return

    # 🔒 Animate ONLY the central widget
    content: QWidget | None = window.centralWidget()
    if content is None:
        app.setStyleSheet(final_qss)
        return

    # Prepare opacity effect
    effect = QGraphicsOpacityEffect(content)
    content.setGraphicsEffect(effect)

    fade_out = QPropertyAnimation(effect, b"opacity", content)
    fade_out.setDuration(140)
    fade_out.setStartValue(1.0)
    fade_out.setEndValue(0.0)
    fade_out.setEasingCurve(QEasingCurve.OutCubic)

    fade_in = QPropertyAnimation(effect, b"opacity", content)
    fade_in.setDuration(160)
    fade_in.setStartValue(0.0)
    fade_in.setEndValue(1.0)
    fade_in.setEasingCurve(QEasingCurve.InCubic)

    def apply_and_fade_in():
        app.setStyleSheet(final_qss)
        content.repaint()
        fade_in.start()

    fade_out.finished.connect(apply_and_fade_in)
    fade_out.start()
