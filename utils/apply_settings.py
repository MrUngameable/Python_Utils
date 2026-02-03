from utils.theme import apply_theme, Theme

def apply_app_settings(app, settings):
    """
    Apply all persisted settings to the running application.
    Called ONCE at startup and after rollback if needed.
    """

    # -------------------
    # Theme
    # -------------------
    theme_mode = settings.get_setting("ui.theme.mode", "dark")

    theme_map = {
        "light": Theme.LIGHT,
        "dark": Theme.DARK,
        "system": Theme.SYSTEM,
    }

    apply_theme(app, theme_map.get(theme_mode, Theme.DARK))

    # -------------------
    # UI Mode
    # -------------------
    ui_mode = settings.get_setting("ui.mode", "GUI")
    settings.ui_manager._ui_type = ui_mode

    # -------------------
    # Audio / Volume (stub)
    # -------------------
    volume = settings.get_setting("audio.volume")
    if volume is not None:
        pass  # hook audio engine later

    # -------------------
    # Language (stub)
    # -------------------
    language = settings.get_setting("language")
    if language:
        pass  # hook translation layer later