# components/title_image.py

from kivy.uix.image import Image
from config import Config


class TitleImage(Image):
    def __init__(self, **kwargs):
        super().__init__(
            source="./assets/play2.png",
            size_hint=(None, None),
            size=Config.get_title_image_size(200, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.75},
            **kwargs
        )
