from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from components.common_ui import ImageButton, ClickableImage, LabeledAvatar
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from components.animated_widget import AnimatedImage
from utils.sound_manager import SoundManager
from config import Config

# Register the custom font
LabelBase.register(name="Bungee", fn_regular="./assets/fonts/Bungee/Bungee-Regular.ttf")

CUSTOM_COLOR = get_color_from_hex("#050a30")


class AvatarPopup(Popup):
    def __init__(self, current_avatar, on_avatar_change, **kwargs):
        super().__init__(**kwargs)
        self.title = " "
        self.size_hint = (None, None)
        self.size = (600, 600)
        self.separator_height = 0
        self.current_avatar = current_avatar
        self.on_avatar_change = on_avatar_change
        self.background = "./assets/bg_avatar.png"

        self.content = self.create_content()

    def create_content(self):
        popup_layout = FloatLayout()

        pilih_avatar_image = Image(
            source="./assets/pilih_avatar.png",
            size_hint=(None, None),
            size=(400, 82),
            pos_hint={"center_x": 0.5, "top": 1.05},
        )
        popup_layout.add_widget(pilih_avatar_image)

        current_avatar_image = Image(
            source=self.current_avatar,
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )
        popup_layout.add_widget(current_avatar_image)

        pilih_avatar_label = Label(
            text="Pilih Avatar Lain",
            size_hint=(None, None),
            size=Config.get_avatar_popup_size(),
            font_size=18,
            bold=True,
            halign="center",
            font_name="Bungee",
            color=CUSTOM_COLOR,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        popup_layout.add_widget(pilih_avatar_label)

        avatar_grid = GridLayout(
            cols=3,
            spacing=50,
            size_hint=(0.8, 0.3),
            pos_hint={"center_x": 0.55, "center_y": 0.3},
        )

        avatar_options = {
            (
                "./assets/avatar/png/male.png",
                "Veldora",
            ): "./assets/avatar/gif/male/male-",
            (
                "./assets/avatar/png/female.png",
                "Asismant",
            ): "./assets/avatar/gif/female/female-",
            (
                "./assets/avatar/png/ninja.png",
                "Tuple",
            ): "./assets/avatar/gif/ninja/ninja-",
        }

        for (static_path, label_text), animated_base_path in avatar_options.items():
            labeled_avatar = LabeledAvatar(source=static_path, label_text=label_text)
            labeled_avatar.avatar.bind(
                on_press=lambda instance, path=static_path, anim_path=animated_base_path: self.change_avatar(
                    self.on_avatar_change, path, anim_path
                )
            )
            avatar_grid.add_widget(labeled_avatar)

        popup_layout.add_widget(avatar_grid)

        animated_avatar = AnimatedImage(
            size_hint=(None, None),
            size=(300, 200),
            base_path="./assets/avatar/gif/button/frame_",
            frame_count=2,
            fps=4,
            pos_hint={"center_x": 0.5, "center_y": 0.13},
        )

        animated_avatar.bind(on_press=self.click_button_with_sound)
        popup_layout.add_widget(animated_avatar)

        return popup_layout

    def change_avatar(self, on_avatar_change, static_path, animated_base_path):
        SoundManager.play_arrow_sound()
        on_avatar_change(static_path, animated_base_path)
        self.dismiss()

    def click_button_with_sound(self, instance):
        SoundManager.play_arrow_sound()
        self.dismiss()
