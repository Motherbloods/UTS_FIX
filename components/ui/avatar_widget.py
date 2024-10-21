# components/avatar.py

from kivy.uix.relativelayout import RelativeLayout
from components.common_ui import ClickableImage
from components.animated_widget import AnimatedImage


class Avatar(RelativeLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app

        self.static_avatar = ClickableImage(
            source=main_app.current_static_avatar,
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={"x": 0.02, "top": 0.95},
            on_click=main_app.show_avatar_popup,
        )
        self.add_widget(self.static_avatar)

        self.animated_avatar = AnimatedImage(
            size_hint=(None, None),
            size=(100, 100),
            base_path=main_app.current_avatar_path,
            frame_count=6,
            fps=10,
            pos_hint={"center_x": 0.8, "center_y": 0.5},
        )
        self.add_widget(self.animated_avatar)

    def update_avatar(self, static_path, animated_base_path):
        self.static_avatar.update_source(static_path)
        self.animated_avatar.update_animation(animated_base_path, 6)

    def update_position(self, selection):
        if selection == 0:
            self.animated_avatar.pos_hint = {"center_x": 0.73, "center_y": 0.573}
        else:
            self.animated_avatar.pos_hint = {"center_x": 0.73, "center_y": 0.473}
