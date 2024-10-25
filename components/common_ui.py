from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.core.window import Window

LabelBase.register(name="Bungee", fn_regular="./assets/fonts/Bungee/Bungee-Regular.ttf")


class ImageButton(ButtonBehavior, Image):
    pass


class ClickableImage(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        self.on_click = kwargs.pop("on_click", None)
        super(ClickableImage, self).__init__(**kwargs)

    def on_press(self):
        if self.on_click:
            self.on_click(self)

    def update_source(self, new_source):
        self.source = new_source


class LabeledAvatar(BoxLayout):
    def __init__(self, source, label_text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 5
        self.size_hint = (None, None)
        self.size = (100, 130)

        self.avatar = ClickableImage(
            source=source,
            size_hint=(None, None),
            size=(100, 100),
        )
        self.add_widget(self.avatar)

        self.label = Label(
            text=label_text,
            size_hint_y=None,
            height=30,
            font_size=17,
            font_name="Bungee",
            color=get_color_from_hex("#050a30"),
        )
        self.add_widget(self.label)


class HoverAvatar(LabeledAvatar):
    def __init__(self, source, label_text, hover_source, gif_path, **kwargs):
        super().__init__(source=source, label_text=label_text, **kwargs)
        self.normal_source = source
        self.hover_source = hover_source
        self.gif_path = gif_path
        self.animated_widget = None
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.avatar.bind(on_press=self.on_avatar_press)

    def on_mouse_pos(self, *args):
        if not self.avatar.get_root_window():
            return

        pos = args[1]
        inside = self.avatar.collide_point(*self.avatar.to_widget(*pos))

        if inside:
            self.avatar.source = self.hover_source
        else:
            self.avatar.source = self.normal_source

    def on_avatar_press(self, instance):
        print(f"ini diklik {self}")


# class HoverAvatar(LabeledAvatar):
#     def __init__(self, source, label_text, hover_source, gif_path, **kwargs):
#         super().__init__(source=source, label_text=label_text, **kwargs)
#         self.normal_source = source
#         self.hover_source = hover_source
#         self.gif_path = gif_path
#         self.animated_widget = None
#         Window.bind(mouse_pos=self.on_mouse_pos)

#         self.avatar.bind(on_press=self.on_avatar_press)

#     def on_mouse_pos(self, *args):
#         if not self.avatar.get_root_window():
#             return

#         pos = args[1]
#         inside = self.avatar.collide_point(*self.avatar.to_widget(*pos))

#         if inside:
#             self.avatar.source = self.hover_source
#         else:
#             self.avatar.source = self.normal_source

#     def on_avatar_press(self, instance):
#         SoundManager.play_arrow_sound()
#         # Cari parent AvatarPopup
#         current = self
#         while current:
#             if isinstance(current.parent, AvatarPopup):
#                 current.parent.toggle_preview_animation(self.gif_path)
#                 break
#             current = current.parent
