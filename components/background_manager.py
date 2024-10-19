from kivy.graphics import Rectangle
from kivy.core.window import Window


class BackgroundManager:
    @staticmethod
    def set_background(widget, image_source):
        with widget.canvas.before:
            background = Rectangle(
                source=image_source, pos=widget.pos, size=Window.size
            )
        widget.bind(
            size=lambda instance, value: setattr(background, "size", instance.size),
            pos=lambda instance, value: setattr(background, "pos", instance.pos),
        )
