from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.core.audio import SoundLoader
from components.animated_widget import AnimatedImage
from components.common_ui import ImageButton
from config import Config
from components.popup.settings_popup import SettingsManager
from kivy.clock import Clock
from main import MainApp


class MainWidget(RelativeLayout):
    def __init__(self, avatar_path, static_avatar_path, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        print("Initializing MainWidget")
        self.current_selection = 0
        self.max_selection = 2
        self.avatar_path = avatar_path
        self.static_avatar_path = static_avatar_path

        self.arrow_sound = SoundLoader.load("./assets/arrow_music.mp3")

        Window.size = MainApp.get_window_size()

        with self.canvas.before:
            self.background = Rectangle(
                source="./assets/bg.png",
                pos=self.pos,
                size=self.size,
            )
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.animated_avatar = AnimatedImage(
            size_hint=(None, None),
            size=Config.get_avatar_size(500, 500),
            base_path=self.avatar_path,
            frame_count=6,
            fps=10,
            pos_hint={"center_x": 0.73, "center_y": 0.8},
        )
        self.add_widget(self.animated_avatar)

        self.back_btn = ImageButton(
            source="./assets/backk.png",
            size_hint=(None, None),
            size=Config.get_button_back_size(),
            pos_hint={"center_x": 0.1, "top": 0.965},
        )
        print("Back button created")
        self.back_btn.bind(on_release=self.play_sound_and_go_back)
        print("Back button bound")
        self.add_widget(self.back_btn)

        title_img = ImageButton(
            source="assets/pilih_mode2.png",
            size_hint=(None, None),
            size=Config.get_title_image_size(550, 40),
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        self.add_widget(title_img)

        # self.zone_names = ["aritmatika", "bangun", "pecahan"]
        self.zone_names = ["kelas_1", "kelas_2", "kelas_3"]
        self.zone_buttons = []
        button_sources = [
            ("./assets/zone/aritmatika.png", 0.38, 0.78),
            ("./assets/zone/bangun.png", 0.62, 0.55),
            ("./assets/zone/pecaha.png", 0.38, 0.322),
        ]

        self.avatar_positions = [
            {"center_x": 0.79, "center_y": 0.82},
            {"center_x": 0.22, "center_y": 0.55},
            {"center_x": 0.79, "center_y": 0.322},
        ]

        for index, (image_source, x_pos, y_pos) in enumerate(button_sources):
            button = ImageButton(
                source=image_source,
                size_hint=(None, None),
                size=Config.get_image_zone_size(),
                pos_hint={"center_x": x_pos, "center_y": y_pos},
            )
            button.index = index
            button.bind(on_release=self.on_zone_button_press)
            self.zone_buttons.append(button)
            self.add_widget(button)

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

        self.update_selection()

        self.loading_animation = AnimatedImage(
            base_path="./gif/frame_",
            frame_count=150,
            fps=16,
            loop_reverse=False,
            size_hint=(1, 1),
            size=(500, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            opacity=0,
        )
        self.add_widget(self.loading_animation)

    def on_touch_down(self, touch):
        print(f"Touch at {touch.pos}")
        for child in self.children:
            if child.collide_point(*touch.pos):
                print(f"Touched {child}")
                if isinstance(child, ImageButton):
                    child.dispatch("on_release")
        return super(MainWidget, self).on_touch_down(touch)

    def on_zone_button_press(self, instance):
        print(f"Zone button pressed: {instance.index}")
        if self.arrow_sound:
            self.arrow_sound.play()
        self.current_selection = instance.index
        self.update_selection()
        self.show_loading_animation()

    def show_loading_animation(self):
        self.loading_animation.opacity = 1
        Clock.schedule_once(self.transition_to_level_screen, 1)

    def transition_to_level_screen(self, dt):
        App.get_running_app().stop()
        from level_screen import LevelScreenApp

        LevelScreenApp(
            zone_name=self.zone_names[self.current_selection],
            difficulty=SettingsManager.get_difficulty(),
            avatar_path=self.avatar_path,
            static_avatar_path=self.static_avatar_path,
        ).run()

    def _update_rect(self, instance, value):
        self.background.pos = instance.pos
        self.background.size = instance.size

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "down":
            self.move_selection_down()
            return True
        elif keycode[1] == "up":
            self.move_selection_up()
            return True
        elif keycode[1] == "enter":
            self.activate_current_selection()
            return True
        return False

    def move_selection_down(self):
        if self.arrow_sound:
            self.arrow_sound.play()
        self.current_selection = min(self.max_selection, self.current_selection + 1)
        self.update_selection()

    def move_selection_up(self):
        if self.arrow_sound:
            self.arrow_sound.play()
        self.current_selection = max(0, self.current_selection - 1)
        self.update_selection()

    def update_selection(self):
        self.animated_avatar.pos_hint = self.avatar_positions[self.current_selection]

    def activate_current_selection(self):
        self.show_loading_animation()

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
            from main import MainApp

            MainApp().run()
        except Exception as e:
            print(f"Error in go_back: {e}")


class ModeApp(App):
    def __init__(self, avatar_path, static_avatar_path, **kwargs):
        super().__init__(**kwargs)
        self.avatar_path = avatar_path
        self.static_avatar_path = static_avatar_path

    def build(self):
        return MainWidget(
            avatar_path=self.avatar_path, static_avatar_path=self.static_avatar_path
        )


if __name__ == "__main__":
    ModeApp().run()
