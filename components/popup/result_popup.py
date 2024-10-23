from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from components.ui.spinner_widget import SpinnerLabel
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from components.common_ui import ImageButton
from config import Config

resource_add_path("./assets/fonts/Bungee/")
LabelBase.register(name="Bungee", fn_regular="Bungee-Regular.ttf")


class ResultPopup(Popup):
    def __init__(
        self,
        is_correct,
        score_increase,
        time_taken,
        user_score,
        on_next,
        on_play_again,
        **kwargs,
    ):
        super(ResultPopup, self).__init__(**kwargs)
        self.title = " "
        self.separator_height = 0
        self.size_hint = (None, None)
        self.size = (300, 400)
        self.content = self.create_content(
            is_correct, score_increase, time_taken, user_score, on_next, on_play_again
        )
        self.background = ""
        self.background_color = [0, 0, 0, 0]

    def create_content(
        self, is_correct, score_increase, time_taken, user_score, on_next, on_play_again
    ):
        content = FloatLayout()
        image_source = "./assets/benar.png" if is_correct else "./assets/salah.png"
        new_image = Image(
            source=image_source,
            size_hint=(None, None),
            size=(280, 260),  # Ukuran gambar baru
            pos_hint={"center_x": 0.5, "center_y": 0.85},  # Posisi di atas gambar piala
        )
        content.add_widget(new_image)
        # Trophy image
        trophy = Image(
            source="./assets/piala.png",
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={"center_x": 0.2, "center_y": 0.5},
        )
        content.add_widget(trophy)
        score = 0 if score_increase == -100 else score_increase
        self.spinner = SpinnerLabel(
            start_value=0,
            end_value=score,
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"center_x": 0.57, "center_y": 0.5},
        )
        content.add_widget(self.spinner)

        time_label = Label(
            text=f"Waktu: {time_taken:.1f} detik",
            font_name="Bungee",
            size_hint=(None, None),
            size=(200, 30),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
        )
        content.add_widget(time_label)

        if is_correct:
            next_btn = ImageButton(
                source="./assets/lanjut.png",
                size_hint=(None, None),
                size=Config.get_button_back_size(80, 80),
                pos_hint={"center_x": 0.5, "center_y": 0.25},
            )
            next_btn.bind(on_release=on_next)
            content.add_widget(next_btn)
        else:
            button_layout = FloatLayout(
                size_hint=(None, None),
                size=(200, 50),
                pos_hint={"center_x": 0.5, "center_y": 0.2},
            )
            play_again_btn = ImageButton(
                source="./assets/main_lagi.png",
                size_hint=(None, None),
                size=Config.get_button_back_size(80, 80),
                pos_hint={"center_x": 0, "y": 0},
            )
            next_btn = ImageButton(
                source="./assets/lanjut.png",
                size_hint=(None, None),
                size=Config.get_button_back_size(80, 80),
                pos_hint={"center_x": 1, "y": 0},
            )

            play_again_btn.bind(on_release=on_play_again)
            next_btn.bind(on_release=on_next)

            button_layout.add_widget(play_again_btn)
            button_layout.add_widget(next_btn)
            content.add_widget(button_layout)

        return content

    def on_open(self):
        Clock.schedule_once(lambda dt: self.spinner.start_spin(), 0.5)
