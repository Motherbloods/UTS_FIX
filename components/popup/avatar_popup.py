from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from components.common_ui import LabeledAvatar
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from components.animated_widget import AnimatedImage
from components.common_ui import ImageButton, HoverAvatar
from utils.user_data_utils import *
from utils.sound_manager import SoundManager
from config import Config
from kivy.core.window import Window

from utils.constants import AVATAR_OPTIONS, LOCKED_AVATARS

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
        self.show_locked = False

        self.content = self.create_content()

    def create_content(self):
        popup_layout = FloatLayout()

        self.preview_layout = FloatLayout(
            size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(None, None),
            size=(660, 68),
            pos_hint={"center_x": 0.62, "top": 0.95},
        )
        self.pilih_avatar_image = ImageButton(
            source="./assets/pilih_avatar.png",
            size_hint=(None, None),
            size=(250, 68),
            pos_hint={"center_x": 0.5, "top": 1.05},
        )
        self.pilih_avatar_image.bind(on_press=self.show_available_avatars)

        self.shop_avatar = ImageButton(
            source="./assets/avatar_terkunci.png",
            size_hint=(None, None),
            size=(250, 68),
            pos_hint={"center_x": 0.5, "top": 1.05},
        )
        self.shop_avatar.bind(on_press=self.show_locked_avatars)

        button_layout.add_widget(self.pilih_avatar_image)
        button_layout.add_widget(self.shop_avatar)
        popup_layout.add_widget(button_layout)

        self.content_layout = FloatLayout()
        self.update_content_layout()
        popup_layout.add_widget(self.content_layout)

        popup_layout.add_widget(self.preview_layout)

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

    def update_content_layout(self):
        self.content_layout.clear_widgets()

        if not self.show_locked:
            self.show_available_content()
        else:
            self.show_locked_content()

    def show_available_content(self):
        UserDataUtils.check_unlocked_avatars()
        self.content_layout.pos_hint = {"center_x": 0.52, "center_y": 0.53}
        current_avatar_image = Image(
            source=self.current_avatar,
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )
        self.content_layout.add_widget(current_avatar_image)

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
        self.content_layout.add_widget(pilih_avatar_label)

        avatar_grid = GridLayout(
            cols=3,
            spacing=50,
            size_hint=(0.8, 0.3),
            pos_hint={"center_x": 0.55, "center_y": 0.3},
        )

        for (static_path, label_text), animated_base_path in AVATAR_OPTIONS.items():
            labeled_avatar = LabeledAvatar(source=static_path, label_text=label_text)
            labeled_avatar.avatar.bind(
                on_press=lambda instance, path=static_path, anim_path=animated_base_path: self.change_avatar(
                    self.on_avatar_change, path, anim_path
                )
            )

            avatar_grid.add_widget(labeled_avatar)

        self.content_layout.add_widget(avatar_grid)

    def show_locked_content(self):
        self.content_layout.pos_hint = {"center_x": 0.52, "center_y": 0.6}
        locked_label = Label(
            text="Avatar Terkunci",
            size_hint=(None, None),
            size=Config.get_avatar_popup_size(),
            font_size=18,
            bold=True,
            halign="center",
            font_name="Bungee",
            color=CUSTOM_COLOR,
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )
        self.content_layout.add_widget(locked_label)

        locked_grid = GridLayout(
            cols=3,
            spacing=50,
            size_hint=(0.8, 0.5),
            pos_hint={"center_x": 0.55, "center_y": 0.4},
        )

        for static_path, label_text, hover_path, gif_path in LOCKED_AVATARS:
            labeled_avatar = HoverAvatar(
                source=static_path,
                label_text=label_text,
                hover_source=hover_path,
                gif_path=gif_path,
            )
            locked_grid.add_widget(labeled_avatar)

        self.content_layout.add_widget(locked_grid)

    def show_available_avatars(self, instance):
        SoundManager.play_arrow_sound()
        self.show_locked = False
        self.update_content_layout()

    def show_locked_avatars(self, instance):
        SoundManager.play_arrow_sound()
        self.show_locked = True
        self.update_content_layout()

    def change_avatar(self, on_avatar_change, static_path, animated_base_path):
        SoundManager.play_arrow_sound()
        self.current_avatar = static_path
        on_avatar_change(static_path, animated_base_path)
        self.dismiss()

    def click_button_with_sound(self, instance):
        SoundManager.play_arrow_sound()
        self.dismiss()
