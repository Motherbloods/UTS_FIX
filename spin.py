from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path

# Ensure the font path is correct
resource_add_path("./assets/fonts/Bungee/")  # Adjust to the actual font folder location

# Register the Bungee font
LabelBase.register(name="Bungee", fn_regular="Bungee-Regular.ttf")


class SpinnerLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 100
        self.font_name = "Bungee"
        self.start_value = 100
        self.end_value = 1000
        self.current_value = self.start_value
        self.update_text()
        Clock.schedule_once(self.start_spin, 1)

    def update_text(self):
        self.text = str(self.current_value)

    def start_spin(self, *args):
        self.spin_animation()

    def spin_animation(self, *args):
        if self.current_value < self.end_value:
            # Adjust duration to complete in about 4 seconds
            duration = (
                4
                * (self.end_value - self.current_value)
                / (self.end_value - self.start_value)
            )
            anim = Animation(current_value=self.end_value, duration=duration)
            anim.bind(on_progress=self.on_value_change)
            anim.bind(on_complete=self.show_checkmark)
            anim.start(self)

    def on_value_change(self, animation, widget, progress):
        self.current_value = int(
            self.start_value + (self.end_value - self.start_value) * progress
        )
        self.update_text()

    def show_checkmark(self, *args):
        if self.parent:
            self.parent.clear_widgets()
            checkmark = Image(source="./assets/backk.png")
            self.parent.add_widget(checkmark)


class SpinnerApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")
        self.spinner = SpinnerLabel()
        layout.add_widget(self.spinner)
        return layout


if __name__ == "__main__":
    SpinnerApp().run()
