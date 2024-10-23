from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from components.common_ui import ImageButton
from config import Config
from utils.sound_manager import SoundManager


class UnlockedPopup(Popup):
    def __init__(self, unlocked_avatar, on_close_callback, **kwargs):
        super(UnlockedPopup, self).__init__(**kwargs)
        self.title = " "
        self.separator_height = 0
        self.size_hint = (None, None)
        self.size = (500, 400)
        self.background = ""
        self.background_color = [0, 0, 0, 0]
        self.on_close_callback = on_close_callback

        # Main layout
        self.content = FloatLayout()

        # Congratulations text
        congrats_label = Label(
            text="Selamat!\nKamu Membuka Avatar Baru!",
            font_name="Bungee",
            font_size="24sp",
            halign="center",
            size_hint=(None, None),
            size=(400, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.8},
        )
        self.content.add_widget(congrats_label)

        # Avatar image
        avatar_image = Image(
            source=f"./assets/avatar/png/{unlocked_avatar.lower()}.png",
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.content.add_widget(avatar_image)

        # Close button
        close_btn = ImageButton(
            source="./assets/close.png",
            size_hint=(None, None),
            size=Config.get_button_back_size(80, 80),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
        )
        close_btn.bind(on_release=self.on_close)
        self.content.add_widget(close_btn)

    def on_close(self, instance):
        SoundManager.play_arrow_sound()
        self.dismiss()
        if self.on_close_callback:
            self.on_close_callback()
