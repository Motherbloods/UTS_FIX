# components/settings_icon.py

from components.animated_widget import AnimatedImage
from config import Config


class SettingsIcon(AnimatedImage):
    def __init__(self, on_click_callback, **kwargs):
        super().__init__(
            base_path="./assets/avatar/gif/settings/frame_",
            frame_count=21,
            fps=30,
            loop_reverse=True,
            size_hint=(None, None),
            size=Config.get_settings_icon_size(),
            image_size=(1, 1),
            pos_hint={"right": 1, "top": 0.955},
            on_click=on_click_callback,
            **kwargs
        )
