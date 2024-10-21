from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from components.common_ui import ClickableImage
from utils.sound_manager import SoundManager


class LockedLevel(Popup):
    def __init__(self, path, **kwargs):
        super(LockedLevel, self).__init__(**kwargs)
        self.title = " "
        self.size_hint = (None, None)
        self.size = (450, 308)
        self.separator_height = 0
        self.background = path

        layout = FloatLayout()

        lock_image = ClickableImage(
            source="./assets/close.png",
            size_hint=(None, None),
            size=(120, 120),
            pos_hint={"center_x": 0.85, "center_y": 0.82},
        )
        lock_image.bind(on_press=self.dismiss_with_sound)
        layout.add_widget(lock_image)

        self.add_widget(layout)

    def dismiss_with_sound(self, *args):
        SoundManager.play_arrow_sound()
        self.dismiss()
