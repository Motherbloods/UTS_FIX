from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from components.common_ui import ImageButton
from components.animated_widget import AnimatedImage
from config import Config
from components.ui.spinner_widget import SpinnerLabel
from utils.sound_manager import SoundManager
from utils.user_data_utils import UserDataUtils


class ResultPopupFinish(Popup):
    def __init__(
        self,
        total_score,
        star_rating,
        level,
        zone,
        level_score,
        on_play_again,
        on_next_level,
        on_menu_level,
        **kwargs,
    ):
        super(ResultPopupFinish, self).__init__(**kwargs)
        self.title = " "
        self.separator_height = 0
        self.size_hint = (None, None)
        self.size = (500, 400)
        self.background = ""
        self.background_color = [0, 0, 0, 0]

        self.content = FloatLayout()

        if level == 9:
            SoundManager.play_sound("./assets/aplause.mp3")
            image_source = f"./assets/{zone}_done.png"
        else:
            if star_rating == "3B":
                image_source = "./assets/sempurna.png"
            else:
                image_source = "./assets/salah_2.png"

        new_image = Image(
            source=image_source,
            size_hint=(None, None),
            size=(280, 260),
            pos_hint={"center_x": 0.5, "center_y": 0.85},
        )

        self.content.add_widget(new_image)

        trophy = Image(
            source="./assets/piala.png",
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={"center_x": 0.2, "center_y": 0.5},
        )
        self.content.add_widget(trophy)

        self.spinner = SpinnerLabel(
            start_value=0,
            end_value=level_score,
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"center_x": 0.57, "center_y": 0.5},
        )
        self.content.add_widget(self.spinner)

        self.add_star_rating(star_rating)
        button_layout = FloatLayout(
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
        )
        if star_rating is not "0B":
            if level == 9:
                menu_btn = ImageButton(
                    source="./assets/menu_level.png",
                    size_hint=(None, None),
                    size=Config.get_button_back_size(120, 120),
                    pos_hint={"center_x": 0.5, "y": 0},
                )
                menu_btn.bind(on_release=on_menu_level)
                button_layout.add_widget(menu_btn)
            else:
                play_again_btn = ImageButton(
                    source="./assets/main_lagi.png",
                    size_hint=(None, None),
                    size=Config.get_button_back_size(80, 80),
                    pos_hint={"center_x": 0, "y": 0},
                )
                next_btn = ImageButton(
                    source="./assets/next_level.png",
                    size_hint=(None, None),
                    size=Config.get_button_back_size(80, 80),
                    pos_hint={"center_x": 1, "y": 0},
                )
                play_again_btn.bind(on_release=on_play_again)
                next_btn.bind(on_release=on_next_level)

                button_layout.add_widget(play_again_btn)
                button_layout.add_widget(next_btn)
        else:
            play_again_btn = ImageButton(
                source="./assets/main_lagi.png",
                size_hint=(None, None),
                size=Config.get_button_back_size(80, 80),
                pos_hint={"center_x": 0.5, "y": 0},
            )
            play_again_btn.bind(on_release=on_play_again)
            button_layout.add_widget(play_again_btn)
        self.content.add_widget(button_layout)

        self.overlay = FloatLayout()
        self.animated_image = AnimatedImage(
            base_path="./assets/avatar/gif/complete/frame_",
            frame_count=100,
            fps=50,
            size={200, 400},
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.overlay.add_widget(self.animated_image)

        Clock.schedule_once(self.show_animated_overlay, 0.1)

    def add_star_rating(self, star_rating):
        star_images = []

        if "_" in star_rating:
            star_rating = star_rating.replace("_", ".")

        if star_rating.endswith("B"):
            rating = float(star_rating[:-1])
        else:
            rating = float(star_rating)

        full_stars = int(rating)
        half_star = rating % 1 > 0

        for i in range(3):
            if i < full_stars:
                star_images.append("./assets/star_full.png")
            elif i == full_stars and half_star:
                star_images.append("./assets/star_set.png")
            else:
                star_images.append("./assets/star_0.png")

        star_layout = FloatLayout(
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={"center_x": 0.36, "center_y": 1.3},
        )

        x_offset = [0, 1, 2]
        y_offset = [0.4, 0.8, 0.4]

        for i, source in enumerate(star_images):
            star = Image(
                source=source,
                size_hint=(None, None),
                size=(0, 0),
                pos_hint={
                    "center_x": x_offset[i],
                    "center_y": y_offset[i],
                },
                opacity=0,
            )
            star_layout.add_widget(star)

            anim = (
                Animation(size=(100, 100), opacity=1, duration=0.5)
                + Animation(size=(120, 120), duration=0.1)
                + Animation(size=(100, 100), duration=0.1)
            )

            Clock.schedule_once(lambda dt, s=star, a=anim: a.start(s), i * 0.5)

        self.content.add_widget(star_layout)

    def show_animated_overlay(self, dt):
        Window.add_widget(self.overlay)
        Clock.schedule_once(self.remove_animated_overlay, 3)

    def remove_animated_overlay(self, dt):
        Window.remove_widget(self.overlay)

    def on_open(self):
        Clock.schedule_once(lambda dt: self.spinner.start_spin(), 0.5)
