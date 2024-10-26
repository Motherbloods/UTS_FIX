from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime, timedelta
from kivy.core.window import Window
from components.common_ui import ImageButton
from config import Config
from utils.sound_manager import SoundManager
from utils.user_data_utils import UserDataUtils


class HeartsEmptyPopup(Popup):
    def __init__(self, time_remaining, use_point=False, point=0, goBack=None, **kwargs):
        kwargs["auto_dismiss"] = False
        super(HeartsEmptyPopup, self).__init__(**kwargs)

        window_width, window_height = Window.size
        self.width = window_width * 0.92

        aspect_ratio = 625 / 1080
        self.height = self.width * aspect_ratio

        self.title = " "
        self.size_hint = (None, None)
        self.size = (self.width, self.height)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.background_scale = (3, 3)
        self.separator_height = 0
        self.padding = 0
        self.background = "./assets/bg_popup.png"
        self.use_point = use_point
        self.goBack = goBack

        layout = FloatLayout()

        heart_positions = [0.2, 0.35, 0.5, 0.65, 0.8]

        # Tambahkan 5 gambar hati
        for x_pos in heart_positions:
            heart_image = Image(
                source="./assets/kosong.png",
                size_hint=(None, None),
                size=(130, 130),
                pos_hint={"center_x": x_pos, "center_y": 0.7},
            )
            layout.add_widget(heart_image)
        minutes = (time_remaining % 3600) // 60

        # Label untuk pesan
        message_label = Label(
            text=f"Hati kamu habis!\nTunggu {int(minutes)} menit lagi untuk bermain!",
            font_name="Bungee",
            font_size="20   sp",
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            halign="center",
        )
        close_button = ImageButton(
            source="./assets/mengerti.png",
            size_hint=(None, None),
            size=Config.get_button_back_size(80, 80),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
        )
        close_button.bind(on_press=self.close_with_sound)
        layout.add_widget(close_button)
        layout.add_widget(message_label)

        if use_point:
            # Trophy image
            trophy_image = Image(
                source="./assets/piala.png",
                size_hint=(None, None),
                size=(50, 50),
                pos_hint={"center_x": 0.45, "center_y": 0.35},
            )

            # Point label
            point_label = Label(
                text=str(point),
                font_name="Bungee",
                font_size="20sp",
                color=(0, 0, 0, 1),
                pos_hint={"center_x": 0.54, "center_y": 0.35},
            )

            layout.add_widget(trophy_image)
            layout.add_widget(point_label)

        self.add_widget(layout)

    def close_with_sound(self, instance):
        SoundManager.play_arrow_sound()

        if self.use_point and self.goBack:
            # Use goBack to navigate back
            self.goBack(instance)
        else:
            self.dismiss()
