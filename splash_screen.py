from kivy.app import App
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from main import MainApp
from kivy.uix.progressbar import ProgressBar
from components.animated_widget import AnimatedImage
import math


class SplashScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background = Image(
            source="./assets/logo2.png", allow_stretch=True, keep_ratio=False
        )
        self.add_widget(self.background)

        self.animated_widgets = []
        avatar_types = ["ninja", "male", "female"]

        for i, avatar in enumerate(avatar_types):
            widget = AnimatedImage(
                base_path=f"./assets/avatar/gif/{avatar}/{avatar}-",
                frame_count=6,
                fps=10,
                size_hint=(None, None),
                size=(150, 150),
                pos_hint={"center_x": 0.35 + i * 0.15, "center_y": 0.5},
            )
            self.add_widget(widget)
            self.animated_widgets.append(widget)

        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint=(0.5, None),
            height=20,
            pos_hint={"center_x": 0.5, "y": 0.1},
        )
        self.add_widget(self.progress_bar)

        Clock.schedule_interval(self.animate_widgets, 1 / 30)

    def animate_widgets(self, dt):
        for i, widget in enumerate(self.animated_widgets):

            y_offset = math.sin(Clock.get_time() * 3 + i * math.pi / 2) * 0.02
            widget.pos_hint = {
                "center_x": 0.35 + i * 0.15,
                "center_y": 0.2 + y_offset,
            }


class SplashApp(App):
    def build(self):
        Window.size = MainApp.get_window_size()
        self.splash_screen = SplashScreen()
        self.total_time = 5
        self.elapsed_time = 0
        Clock.schedule_interval(self.update_progress, 1 / 30)
        return self.splash_screen

    def on_start(self):
        self.sound = SoundLoader.load("./assets/splash.mp3")
        if self.sound:
            self.sound.play()
        Clock.schedule_once(self.switch_to_main_app, self.total_time)

    def switch_to_main_app(self, dt):
        if self.sound:
            self.sound.stop()
        self.stop()
        MainApp().run()

    def update_progress(self, dt):
        self.elapsed_time += dt
        progress = min(100, (self.elapsed_time / self.total_time) * 100)
        self.splash_screen.progress_bar.value = progress


if __name__ == "__main__":
    SplashApp().run()
