from pathlib import Path
import sys

def get_src_root() -> Path:
    """
    Returns the src/ directory in both Dev and Builds.
    """

    if getattr(sys, "frozen", False):
        # In PyInstaller, _MEIPASS points to the temp extracted folder
        return Path(sys._MEIPASS)
    else:
        # paths.py -> utils -> src
        return Path(__file__).resolve().parents[1]

def resource_path(relative_path: str) -> Path:
    """
    Resolve paths relative to src/.
    Example: resource_path("assets/styles/dark_theme.qss")
    """
    return get_src_root() / relative_path