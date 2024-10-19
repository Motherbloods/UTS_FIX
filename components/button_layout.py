# components/button_layout.py

from kivy.uix.boxlayout import BoxLayout
from components.common_ui import ImageButton
from config import Config


class ButtonLayout(BoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint=(None, None),
            size=Config.get_button_layout_size(),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            spacing=20,
            **kwargs
        )

        self.pilih_mode_btn = ImageButton(source="assets/pilih_mode2.png")
        self.pilih_mode_btn.index = 0
        self.pilih_mode_btn.bind(on_press=main_app.on_button_press)

        self.keluar_game_btn = ImageButton(source="assets/keluar_game2.png")
        self.keluar_game_btn.index = 1
        self.keluar_game_btn.bind(on_press=main_app.on_button_press)

        self.add_widget(self.pilih_mode_btn)
        self.add_widget(self.keluar_game_btn)
