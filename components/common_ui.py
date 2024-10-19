from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase

LabelBase.register(name="Bungee", fn_regular="./assets/fonts/Bungee/Bungee-Regular.ttf")


class ImageButton(ButtonBehavior, Image):
    pass


class ClickableImage(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        self.on_click = kwargs.pop("on_click", None)
        super(ClickableImage, self).__init__(**kwargs)

    def on_press(self):
        if self.on_click:
            self.on_click(self)

    def update_source(self, new_source):
        self.source = new_source


class LabeledAvatar(BoxLayout):
    def __init__(self, source, label_text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 5
        self.size_hint = (None, None)
        self.size = (100, 130)

        self.avatar = ClickableImage(
            source=source,
            size_hint=(None, None),
            size=(100, 100),
        )
        self.add_widget(self.avatar)

        self.label = Label(
            text=label_text,
            size_hint_y=None,
            height=30,
            font_size=17,
            font_name="Bungee",
            color=get_color_from_hex("#050a30"),
        )
        self.add_widget(self.label)
