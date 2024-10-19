from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Rectangle
from components.common_ui import ImageButton
from config import Config
from kivy.uix.scrollview import ScrollView
from main import MainApp
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from components.popup.locked_level_popup import LockedLevel
from kivy.uix.boxlayout import BoxLayout
from soal_screen import SoalApp

LabelBase.register(name="Bungee", fn_regular="./assets/fonts/Bungee/Bungee-Regular.ttf")
CUSTOM_COLOR = get_color_from_hex("#050a30")


class LevelScreen(RelativeLayout):
    def __init__(
        self, zone_name, difficulty, avatar_path, static_avatar_path, **kwargs
    ):
        super(LevelScreen, self).__init__(**kwargs)

        self.zone_name = zone_name
        self.difficulty = difficulty
        self.avatar_path = avatar_path
        self.static_avatar_path = static_avatar_path
        self.arrow_sound = SoundLoader.load("./assets/arrow_music.mp3")

        self.store = JsonStore("user_progress.json")
        self.current_level = self.get_current_level()
        self.level_scores = self.get_level_scores()

        Window.size = MainApp.get_window_size()

        with self.canvas.before:
            self.background = Rectangle(
                source="./assets/bg.png",
                pos=self.pos,
                size=self.size,
            )
        self.bind(size=self._update_rect, pos=self._update_rect)
        back_btn = ImageButton(
            source="./assets/backk.png",
            size_hint=(None, None),
            size=Config.get_button_back_size(),
            pos_hint={"center_x": 0.1, "top": 0.965},
        )
        back_btn.bind(on_press=self.play_sound_and_go_back)
        self.add_widget(back_btn)

        title_image_path = (
            f"./assets/level/title/{self.zone_name}/{self.difficulty}.png"
        )
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
                level_image = "./assets/level/kunci.png"
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
        icons_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=(Window.width * 0.4, Window.height * 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            spacing=20,
        )

        trophy_layout = BoxLayout(
            orientation="vertical", size_hint=(None, None), spacing=0
        )
        trophy_image = Image(
            source="./assets/piala.png",
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"center_y": 1},
        )
        user_score = 0
        if self.store.exists("user_score"):
            user_score = self.store.get("user_score")["score"]
        trophy_text = Label(
            text=str(user_score),
            size_hint=(None, None),
            pos_hint={
                "center_x": 0.2,
                "center_y": 0,
            },
            color=CUSTOM_COLOR,
            font_name="Bungee",
            font_size="20",
        )
        trophy_layout.add_widget(trophy_image)
        trophy_layout.add_widget(trophy_text)

        stars_layout = BoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            spacing=5,
        )

        # Stars image
        stars_image = Image(
            source="./assets/stars.png", size_hint=(None, None), size=(40, 40)
        )

        # Stars label
        total_stars = self.calculate_total_stars()
        stars_text = Label(
            text=f"{total_stars:.1f}",
            size_hint=(None, None),
            color=CUSTOM_COLOR,
            font_name="Bungee",
            font_size="16sp",
        )

        # Add the image and label to the stars layout
        stars_layout.add_widget(stars_image)
        stars_layout.add_widget(stars_text)

        # Add trophy and stars layouts to the horizontal layout
        icons_layout.add_widget(trophy_layout)
        icons_layout.add_widget(stars_layout)

        # Add the horizontal layout to the main widget
        self.add_widget(icons_layout)

    def get_level_scores(self):
        if self.store.exists("user_progress"):
            progress = self.store.get("user_progress")
            return progress.get("level_scores", {})
        return {}

    def get_level_image_path(self, level):
        if level > self.current_level:
            return "./assets/level/kunci.png"

        level_key = f"{self.zone_name}_{self.difficulty}_{level}"
        level_data = self.level_scores.get(level_key, {})
        star_rating = level_data.get("star_rating", "0B")

        if star_rating == "0B":
            return f"./assets/level/0B/{level}.png"

        return f"./assets/level/{star_rating}/{level}.png"

    def calculate_total_stars(self):
        total_stars = 0
        for level_data in self.level_scores.values():
            star_rating = level_data.get("star_rating", "0B")
            if star_rating == "3B":
                total_stars += 3
            elif star_rating == "2_5B":
                total_stars += 2.5
            elif star_rating == "2B":
                total_stars += 2
            elif star_rating == "1_5B":
                total_stars += 1.5
            elif star_rating == "1B":
                total_stars += 1
        return total_stars

    def get_current_level(self):
        if self.store.exists("user_progress"):
            print("ini kepanggil")
            return self.store.get("user_progress")["current_level"]
        else:
            self.store.put("user_progress", current_level=1)
            return 1

    def show_locked_popup(self):
        popup = LockedLevel(path="./assets/popup.png")
        popup.open()

    def on_level_select(self, level):
        if level <= self.current_level:
            print(f"Level {level} selected")
            App.get_running_app().stop()
            SoalApp(
                zone=self.zone_name,
                difficulty=self.difficulty,
                level=level,
                avatar_path=self.avatar_path,
            ).run()
        else:
            print(f"Level {level} is locked")
            self.show_locked_popup()

    def update_current_level(self, new_level):
        self.store.put("user_progress", current_level=new_level)
        self.current_level = new_level

    def _update_rect(self, instance, value):
        self.background.pos = instance.pos
        self.background.size = instance.size

    def play_sound_and_go_back(self, instance):
        try:
            print("ini klikk")
            if self.arrow_sound:
                self.arrow_sound.play()
            self.go_back(instance)
        except Exception as e:
            print(f"Error in play_sound_and_go_back: {e}")

    def go_back(self, instance):
        try:
            print("ini diklik")
            App.get_running_app().stop()
            from zone_screen import ModeApp

            ModeApp(
                avatar_path=self.avatar_path, static_avatar_path=self.static_avatar_path
            ).run()
        except Exception as e:
            print(f"Error in go_back: {e}")


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
