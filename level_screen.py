from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from components.common_ui import ImageButton
from config import Config
from kivy.uix.scrollview import ScrollView
from main import MainApp
from kivy.core.text import LabelBase
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label
from components.popup.locked_level_popup import LockedLevel
from components.popup.hearts_empty_popup import HeartsEmptyPopup
from kivy.uix.floatlayout import FloatLayout
from soal_screen import SoalApp
from utils.game_utils import GameUtils
from utils.constants import *
from utils.sound_manager import SoundManager
from utils.user_data_utils import UserDataUtils
from components.ui.background import Background
from components.animated_widget import AnimatedImage

LabelBase.register(name="Bungee", fn_regular=FONTS_PATH)


class LevelScreen(RelativeLayout):
    def __init__(
        self, zone_name, difficulty, avatar_path, static_avatar_path, **kwargs
    ):
        super(LevelScreen, self).__init__(**kwargs)

        self.zone_name = zone_name
        self.difficulty = difficulty
        self.avatar_path = avatar_path
        self.static_avatar_path = static_avatar_path
        self.remaining_hearts = UserDataUtils.get_remaining_hearts()
        self.arrow_sound = SoundLoader.load("./assets/arrow_music.mp3")

        self.store = JsonStore("user_progress.json")
        self.current_level = self.get_current_level()
        self.level_scores = self.get_level_scores()

        Window.size = MainApp.get_window_size()

        self.background = Background()
        self.add_widget(self.background)
        self.setup_ui()

    def setup_ui(self):
        back_btn = ImageButton(
            source="./assets/backk.png",
            size_hint=(None, None),
            size=Config.get_button_back_size(80, 80),
            pos_hint={"center_x": 0.1, "top": 0.965},
        )
        back_btn.bind(on_press=self.play_sound_and_go_back)
        self.add_widget(back_btn)

        title_image_path = f"./assets/level/title/{self.zone_name}.png"
        title_image = Image(
            source=title_image_path,
            size_hint=(None, None),
            size=Config.get_title_image_size(200, 40),
            pos_hint={"center_x": 0.57, "top": 0.948},
        )
        self.add_widget(title_image)

        self.add_trophy_and_stars()

        scroll_view = ScrollView(
            size_hint=(1, None),
            size=(Window.width, Window.height * 0.7),
            pos_hint={"center_x": 0.6, "center_y": 0.5},
        )
        self.add_widget(scroll_view)

        grid_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter("height"))
        for i in range(1, 10):
            if i > self.current_level:
                animated_button = AnimatedImage(
                    base_path="./assets/avatar/gif/gembok/frame_",
                    frame_count=100,
                    fps=20,
                    loop_reverse=True,
                    size_hint=(None, None),
                    size=(Window.width * 0.25, Window.width * 0.25),
                    use_interval=True,  # Enable interval-based animation
                    interval_duration=7,
                )
                animated_button.bind(
                    on_press=lambda x, level=i: self.on_level_select(level)
                )
                grid_layout.add_widget(animated_button)
            else:
                level_key = f"{self.zone_name}_{self.difficulty}_{i}"
                level_data = self.level_scores.get(level_key, {})
                star_rating = level_data.get("star_rating", "0B")
                if star_rating == "0B":
                    level_image = f"./assets/level/0B/{i}.png"
                else:
                    level_image = f"./assets/level/{star_rating}/{i}.png"

                level_btn = ImageButton(
                    source=level_image,
                    size_hint=(None, None),
                    size=(Window.width * 0.25, Window.width * 0.25),
                )
                level_btn.bind(on_press=lambda x, level=i: self.on_level_select(level))
                grid_layout.add_widget(level_btn)

        scroll_view.add_widget(grid_layout)

    def add_trophy_and_stars(self):
        icons_layout = FloatLayout(
            size_hint=(None, None),
            size=(Window.width * 0.6, Window.height * 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.84},
        )

        trophy_image = Image(
            source="./assets/piala.png",
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"center_x": 0.1, "center_y": 0.8},
        )
        user_score = 0
        if self.store.exists("user_score"):
            user_score = self.store.get("user_score")["score"]

        trophy_text = Label(
            text=str(user_score),
            size_hint=(None, None),
            pos_hint={"center_x": 0.1, "center_y": 0.6},
            color=CUSTOM_COLOR,
            font_name="Bungee",
            font_size="20sp",
        )

        stars_image = Image(
            source="./assets/stars.png",
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"center_x": 0.37, "center_y": 0.8},
        )

        total_stars = self.calculate_total_stars()
        stars_text = Label(
            text=f"{total_stars}/30",
            size_hint=(None, None),
            pos_hint={"center_x": 0.37, "center_y": 0.6},
            color=CUSTOM_COLOR,
            font_name="Bungee",
            font_size="20sp",
        )

        hearts_layout = FloatLayout(
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.74, "center_y": 0.83},
        )
        for i in range(1, 5 + 1):
            if i <= self.remaining_hearts:
                heart_image = Image(
                    source=f"./assets/heart{i}.png",
                    size_hint=(None, None),
                    size=(100, 100),
                    pos_hint={
                        "center_x": 0.25 * i,
                        "center_y": 0.2,
                    },
                )
            else:
                heart_image = Image(
                    source="./assets/kosong.png",
                    size_hint=(None, None),
                    size=(100, 100),
                    pos_hint={
                        "center_x": 0.25 * i,
                        "center_y": 0.2,
                    },
                )
            hearts_layout.add_widget(heart_image)

        icons_layout.add_widget(trophy_image)
        icons_layout.add_widget(trophy_text)
        icons_layout.add_widget(stars_image)
        icons_layout.add_widget(stars_text)
        icons_layout.add_widget(hearts_layout)

        self.add_widget(icons_layout)

    def get_level_scores(self):
        progress = GameUtils.get_user_progress()
        return progress.get(f"{self.zone_name}_{self.difficulty}_level_scores", {})

    def get_level_image_path(self, level):
        return GameUtils.get_level_image_path(
            level, self.current_level, self.level_scores
        )

    def calculate_total_stars(self):
        return GameUtils.calculate_total_stars(self.level_scores)

    def get_current_level(self):
        progress = GameUtils.get_user_progress()
        return progress.get(f"{self.zone_name}_{self.difficulty}_current_level", 1)

    def show_locked_popup(self):
        SoundManager.play_arrow_sound()
        popup = LockedLevel(path="./assets/popup.png")
        popup.open()

    def on_level_select(self, level):
        SoundManager.play_arrow_sound()
        if level <= self.current_level:
            remaining_hearts = UserDataUtils.get_remaining_hearts()
            if remaining_hearts <= 0:
                max_hearts = 5
                hearts_needed = max_hearts - remaining_hearts
                time_per_heart = 5 * 60  # 5 menit dalam detik
                total_time_needed = hearts_needed * time_per_heart

                popup = HeartsEmptyPopup(time_remaining=total_time_needed)
                popup.open()
            else:
                App.get_running_app().stop()
                SoalApp(
                    zone=self.zone_name,
                    difficulty=self.difficulty,
                    level=level,
                    avatar_path=self.avatar_path,
                ).run()
        else:
            self.show_locked_popup()

    def update_current_level(self, new_level):
        progress = (
            self.store.get("user_progress")
            if self.store.exists("user_progress")
            else {}
        )
        progress[f"{self.zone_name}_{self.difficulty}_current_level"] = new_level
        self.store.put("user_progress", **progress)
        self.current_level = new_level

    def add_level_buttons(self):
        grid_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter("height"))
        for i in range(1, 10):
            level_image = self.get_level_image_path(i)
            level_btn = ImageButton(
                source=level_image,
                size_hint=(None, None),
                size=(Window.width * 0.25, Window.width * 0.25),
            )
            level_btn.bind(on_press=lambda x, level=i: self.on_level_select(level))
            grid_layout.add_widget(level_btn)
        return grid_layout

    def play_sound_and_go_back(self, instance):
        SoundManager.play_arrow_sound()
        self.go_back(instance)

    def go_back(self, instance):
        App.get_running_app().stop()
        from zone_screen import ModeApp

        ModeApp(
            avatar_path=self.avatar_path, static_avatar_path=self.static_avatar_path
        ).run()


class LevelScreenApp(App):
    def __init__(
        self, zone_name, difficulty, avatar_path, static_avatar_path, **kwargs
    ):
        super().__init__(**kwargs)
        self.zone_name = zone_name
        self.difficulty = difficulty
        self.avatar_path = avatar_path
        self.static_avatar_path = static_avatar_path

    def build(self):
        return LevelScreen(
            zone_name=self.zone_name,
            difficulty=self.difficulty,
            avatar_path=self.avatar_path,
            static_avatar_path=self.static_avatar_path,
        )


if __name__ == "__main__":
    LevelScreenApp().run()
