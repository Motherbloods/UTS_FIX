from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle
from utils.asset_manager import AssetManager


class BaseScreen(RelativeLayout):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.background = None
        self._init_background()

    def _init_background(self):
        with self.canvas.before:
            self.background = Rectangle(
                source=AssetManager.get_background_image(), pos=self.pos, size=self.size
            )
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        if self.background:
            self.background.pos = instance.pos
            self.background.size = instance.size
