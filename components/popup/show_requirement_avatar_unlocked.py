from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup
from config import Config
from utils.sound_manager import SoundManager
from kivy.uix.behaviors import ButtonBehavior


class ImageButton(ButtonBehavior, Image):
    pass


class AvatarRequirementsPopup(Popup):
    def __init__(
        self,
        avatar_source,
        avatar_name,
        requirement_message,
        on_close_callback=None,
        **kwargs,
    ):
        kwargs["auto_dismiss"] = False
        super(AvatarRequirementsPopup, self).__init__(**kwargs)
        self.title = " "
        self.separator_height = 0
        self.size_hint = (None, None)
        self.size = (500, 400)
        self.background = ""
        self.background_color = [0, 0, 0, 0]
        self.on_close_callback = on_close_callback

        self.content = FloatLayout()

        avatar_image = Image(
            source=avatar_source,
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.8},
        )
        self.content.add_widget(avatar_image)

        requirements_label = Label(
            text=requirement_message,
            font_name="Bungee",
            font_size="20sp",
            halign="center",
            size_hint=(None, None),
            size=(400, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            color=get_color_from_hex("#ffffff"),
        )
        self.content.add_widget(requirements_label)

        close_btn = ImageButton(
            source="./assets/close.png",
            size_hint=(None, None),
            size=Config.get_button_back_size(80, 80),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
        )
        close_btn.bind(on_release=self.on_close)
        self.content.add_widget(close_btn)

    def on_close(self, instance):
        SoundManager.play_arrow_sound()
        self.dismiss()
        if self.on_close_callback:
            self.on_close_callback()
