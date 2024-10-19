from kivy.uix.label import Label
from kivy.animation import Animation


class SpinnerLabel(Label):
    def __init__(self, start_value, end_value, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 40
        self.font_name = "Bungee"
        self.start_value = start_value
        self.end_value = end_value
        self.current_value = self.start_value
        self.update_text()

    def update_text(self):
        self.text = f"+ {str(self.current_value)}"

    def start_spin(self):
        self.spin_animation()

    def spin_animation(self):
        duration = 2  # 2 seconds for the animation
        anim = Animation(current_value=self.end_value, duration=duration)
        anim.bind(on_progress=self.on_value_change)
        anim.start(self)

    def on_value_change(self, animation, widget, progress):
        self.current_value = int(
            self.start_value + (self.end_value - self.start_value) * progress
        )
        self.update_text()
