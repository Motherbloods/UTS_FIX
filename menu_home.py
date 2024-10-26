from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from utils.sound_manager import SoundManager
from components.animated_widget import AnimatedImage
from components.common_ui import ClickableImage
from components.popup.avatar_popup import AvatarPopup
from components.popup.settings_popup import SettingsPopup
from utils.keyboard_manager import KeyboardManager
from components.ui.background import Background
from components.ui.title_image import TitleImage
from components.ui.button_layout import ButtonLayout
from components.ui.settings_widget import SettingsIcon
from utils.user_data_utils import UserDataUtils
from config import Config
from kivy.metrics import Metrics


class MainApp(App):
    @staticmethod
    def get_window_size():
        base_width = 450
        window_height = int(base_width * (16 / 9))
        return base_width, window_height

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        static_path, animated_path = UserDataUtils.load_avatar_selection()
        self.current_avatar_path = animated_path
        self.current_static_avatar = static_path
        self.avatar_popup = None
        self.settings_popup = None
        self.keyboard_manager = None
        self.current_selection = 0

    def build(self):

        SoundManager.initialize_bgm()
        SoundManager.initialize_arrow_sound()
        UserDataUtils.check_unlocked_avatars()
        self.original_size = Window.size
        self.original_dpi = Metrics.dpi

        base_width = 450
        window_height = int(base_width * (16 / 9))
        Window.size = (base_width, window_height)
        self.root = RelativeLayout()

        self.keyboard_manager = KeyboardManager(self)

        self.background = Background()

        self.root.add_widget(self.background)

        self.static_avatar = ClickableImage(
            source=self.current_static_avatar,
            size_hint=(None, None),
            size=Config.get_avatar_size(50, 50),
            pos_hint={"x": 0.02, "top": 0.95},
            on_click=self.show_avatar_popup,
        )

        self.root.add_widget(self.static_avatar)

        self.settings_icon = SettingsIcon(self.show_settings_popup)

        self.root.add_widget(self.settings_icon)

        self.title_image = TitleImage()
        self.root.add_widget(self.title_image)

        self.animated_avatar = AnimatedImage(
            size_hint=(None, None),
            size=Config.get_animated_avatar_size(),
            base_path=self.current_avatar_path,
            frame_count=6,
            fps=10,
            pos_hint={"center_x": 0.8, "center_y": 0.5},
        )
        self.root.add_widget(self.animated_avatar)

        self.button_layout = ButtonLayout(self)

        self.root.add_widget(self.button_layout)

        self.update_selection()

        return self.root

    def on_settings_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            SoundManager.play_arrow_sound()
            self.show_settings_popup()

    def show_settings_popup(self, instance):
        SoundManager.play_arrow_sound()
        if not self.settings_popup:
            self.settings_popup = SettingsPopup(
                current_avatar_path=self.current_avatar_path
            )
        self.settings_popup.open()

    def play_sound_and_show_avatar(self, instance):
        SoundManager.play_arrow_sound()
        self.show_avatar_options(instance)

    def on_button_press(self, instance):
        SoundManager.play_arrow_sound()
        self.current_selection = instance.index
        self.update_selection()
        self.activate_current_selection()

    def move_selection_down(self):
        SoundManager.play_arrow_sound()
        self.current_selection = min(1, self.current_selection + 1)
        self.update_selection()

    def move_selection_up(self):
        SoundManager.play_arrow_sound()
        self.current_selection = max(0, self.current_selection - 1)
        self.update_selection()

    def update_selection(self):
        if self.current_selection == 0:
            self.animated_avatar.pos_hint = {"center_x": 0.73, "center_y": 0.573}
        else:
            self.animated_avatar.pos_hint = {"center_x": 0.73, "center_y": 0.473}

    def activate_current_selection(self):
        if self.current_selection == 0:
            self.play_sound_and_go_to_mode(None)
        else:
            self.play_sound_and_exit(None)

    def show_avatar_popup(self, instance):
        SoundManager.play_arrow_sound()
        self.avatar_popup = AvatarPopup(
            current_avatar=self.current_static_avatar,
            on_avatar_change=self.change_avatar,
        )
        self.avatar_popup.open()

    def change_avatar(self, static_path, animated_base_path):
        SoundManager.play_arrow_sound()
        self.static_avatar.update_source(static_path)
        self.current_static_avatar = static_path
        self.current_avatar_path = animated_base_path
        self.static_avatar.update_source(static_path)
        self.animated_avatar.update_animation(animated_base_path, 6)
        UserDataUtils.save_avatar_selection(static_path, animated_base_path)

        if self.avatar_popup:
            self.avatar_popup.current_avatar = static_path
            self.avatar_popup.dismiss()
        if self.settings_popup:
            self.settings_popup.current_avatar_path = animated_base_path
            self.settings_popup.animated_avatar.update_animation(animated_base_path, 6)

    def play_sound_and_go_to_mode(self, instance):
        SoundManager.play_arrow_sound()
        self.go_to_mode(instance)

    def play_sound_and_exit(self, instance):
        SoundManager.play_arrow_sound()
        self.exit_game(instance)

    def go_to_mode(self, instance):
        App.get_running_app().stop()
        from zone_screen import ModeApp

        ModeApp(
            avatar_path=self.current_avatar_path,
            static_avatar_path=self.current_static_avatar,
        ).run()

    def exit_game(self, instance):
        App.get_running_app().stop()


if __name__ == "__main__":
    MainApp().run()
