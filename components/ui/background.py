# components/background.py

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window


class Background(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self.background = Rectangle(
                source="./assets/bg.png", pos=self.pos, size=Window.size
            )

        self.bind(size=self.update_background, pos=self.update_background)

    def update_background(self, *args):
        self.background.size = Window.size
        self.background.pos = self.pos
