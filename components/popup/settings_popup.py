from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior
from utils.sound_manager import SoundManager
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.uix.widget import Widget
from components.common_ui import ClickableImage
from utils.sound_manager import SoundManager
from components.animated_widget import AnimatedImage

# Register the custom font
LabelBase.register(name="Bungee", fn_regular="./assets/fonts/Bungee/Bungee-Regular.ttf")

# Define the custom color
CUSTOM_COLOR = get_color_from_hex("#050a30")


class SettingsManager:
    difficulty = "mudah"  # Default difficulty

    @classmethod
    def set_difficulty(cls, difficulty):
        cls.difficulty = difficulty

    @classmethod
    def get_difficulty(cls):
        return cls.difficulty


class ImageButton(ToggleButtonBehavior, Image):
    def __init__(self, source, difficulty, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.difficulty = difficulty


class SettingsPopup(Popup):
    def __init__(self, current_avatar_path, **kwargs):
        super().__init__(**kwargs)
        self.current_avatar_path = current_avatar_path
        window_width, window_height = Window.size
        self.width = window_width * 0.92  # 92% of screen width

        aspect_ratio = 625 / 1080
        self.height = self.width * aspect_ratio

        self.title = " "
        self.size_hint = (None, None)
        self.size = (self.width, self.height)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.background_scale = (3, 3)
        self.separator_height = 0
        self.padding = 0
        self.background = "./assets/bg_popup.png"
        self.content = self.create_content()

        self.update_avatar_position(SettingsManager.get_difficulty())

    def create_content(self):
        content = FloatLayout()

        # Calculate font sizes based on window size
        title_font_size = min(self.width, self.height) * 0.082
        label_font_size = min(self.width, self.height) * 0.072
        header_top = BoxLayout(
            orientation="horizontal",
            spacing=0.1,  # Spacing sebagai persentase dari lebar popup
            size_hint=(None, None),
            size=(self.width / 1.57, 100),  # Ukuran relatif terhadap lebar popup
            pos_hint={"center_x": 0.54, "top": 0.85},  # Posisikan di bagian atas popup
        )

        # Pengaturan label (posisi kiri)
        pengaturan_label = Label(
            text="Pengaturan",
            font_size=title_font_size,
            size_hint=(
                None,
                1,
            ),  # Memastikan tinggi menyesuaikan, dan lebarnya otomatis
            halign="left",  # Text berada di kiri
            valign="middle",
            font_name="Bungee",
            color=CUSTOM_COLOR,
        )
        pengaturan_label.bind(
            size=pengaturan_label.setter("text_size")
        )  # Bind untuk memastikan teks dirapikan dalam label
        header_top.add_widget(pengaturan_label)

        # Spacer (pengisi ruang di antara label dan ikon)
        spacer = Widget(
            size_hint=(1, 1)
        )  # Menggunakan Widget kosong untuk mengisi ruang di antara
        header_top.add_widget(spacer)

        # Icon close (posisi kanan)
        icon_close = ClickableImage(
            source="./assets/close.png",
            size_hint=(None, None),
            size=(35, 35),  # Ukuran icon
            pos_hint={"center_y": 0.5},  # Agar berada di tengah vertikal
        )
        icon_close.bind(on_press=self.dismiss_with_sound)
        header_top.add_widget(icon_close)

        # Tambahkan header_top ke konten utama
        content.add_widget(header_top)

        self.animated_avatar = AnimatedImage(
            size_hint=(None, None),
            size=(100, 100),
            base_path=self.current_avatar_path,
            frame_count=6,
            fps=10,
            pos_hint={"center_x": 0.5, "top": 0.2},
        )
        content.add_widget(self.animated_avatar)

        # Tingkat Kesulitan label
        difficulty_label = Label(
            text="Tingkat Kesulitan",
            font_size=label_font_size,
            size_hint=(None, None),
            size=(self.width * 0.5, self.height * 0.1),
            pos_hint={"center_x": 0.4, "top": 0.675},
            font_name="Bungee",
            color=CUSTOM_COLOR,
        )
        content.add_widget(difficulty_label)

        # Difficulty options
        self.difficulty_options = BoxLayout(
            orientation="horizontal",
            spacing=self.width * 0.037,  # Spacing as a percentage of popup width
            size_hint=(None, None),
            size=(360, 100),  # Size relative to popup
            pos_hint={"center_x": 0.4, "top": 0.56},
        )
        difficulties = [
            ("./assets/mudah.png", "mudah"),
            ("./assets/sedang.png", "sedang"),
            ("./assets/su.png", "sulit"),
        ]
        button_size = min(self.width * 0.2, self.height * 0.15)

        button_width = self.width * 0.235
        button_height = button_width * (81 / 285)

        for source, difficulty in difficulties:
            btn_container = BoxLayout(
                size_hint=(None, None),
                size=(button_size * 2.5, button_size * 4),
                padding=button_size * 0.1,
            )
            btn = ImageButton(
                source=source,
                difficulty=difficulty,
                size_hint=(None, None),
                size=(button_width, button_height),
                allow_stretch=True,
                keep_ratio=False,
                group="difficulty",
            )
            btn.bind(on_press=self.on_difficulty_change_with_sound)
            if difficulty == SettingsManager.get_difficulty():
                btn.state = "down"
            btn_container.add_widget(btn)
            self.difficulty_options.add_widget(btn_container)
        content.add_widget(self.difficulty_options)

        # Music toggle
        bottom_layout = BoxLayout(
            orientation="horizontal",
            spacing=200,  # Spacing sebagai persentase dari lebar popup
            size_hint=(None, None),
            size=(500, 100),  # Ukuran relatif terhadap lebar popup
            pos_hint={"center_x": 0.545, "top": 0.28},  # Posisikan di bagian atas popup
        )

        # Label untuk Musik (posisi di kiri)
        music_label = Label(
            text="Musik:",
            font_size=label_font_size,
            size_hint=(None, None),
            size=(self.width * 0.2, 50),  # Tentukan ukuran sesuai kebutuhan
            pos_hint={"center_x": 0.0, "top": 1},  # Tempatkan di kiri
            font_name="Bungee",
            color=CUSTOM_COLOR,
        )
        bottom_layout.add_widget(music_label)

        # Icon Musik (posisi di kanan)
        self.music_icon = ClickableImage(
            source="./assets/on.png",
            size_hint=(None, None),
            size=(50, 50),  # Ukuran icon
            pos_hint={"center_x": 6, "top": 0.97},  # Tempatkan di kanan
        )
        self.music_icon.bind(on_press=self.toggle_music_with_sound)
        bottom_layout.add_widget(self.music_icon)

        # Tambahkan layout ke content
        content.add_widget(bottom_layout)

        return content

    def on_difficulty_change_with_sound(self, instance):
        SoundManager.play_arrow_sound()
        self.on_difficulty_change(instance)
        self.animated_avatar.update_animation(self.current_avatar_path, 6)

    def on_difficulty_change(self, instance):
        if instance.state == "down":
            SettingsManager.set_difficulty(instance.difficulty)
        self.update_avatar_position(instance.difficulty)

    def update_avatar_position(self, difficulty):
        if difficulty == "mudah":
            self.animated_avatar.pos_hint = {"center_x": 0.24, "top": 0.663}
        elif difficulty == "sedang":
            self.animated_avatar.pos_hint = {"center_x": 0.5, "top": 0.663}
        elif difficulty == "sulit":
            self.animated_avatar.pos_hint = {"center_x": 0.76, "top": 0.663}

    def toggle_music_with_sound(self, instance):
        SoundManager.play_arrow_sound()
        self.toggle_music()

    def toggle_music(self):
        if self.music_icon.source == "./assets/off.png":  # Saat ini dalam kondisi 'off'
            if SoundManager.bgm_instance:
                SoundManager.bgm_instance.play()  # Mainkan musik
            else:
                SoundManager.initialize_bgm()  # Inisialisasi musik jika belum ada instance
            # Ubah ikon ke 'on'
            self.music_icon.source = "./assets/on.png"

        # Jika musik dimatikan (dalam state 'off'), ubah gambar dan matikan musik
        else:  # Saat ini dalam kondisi 'on'
            if SoundManager.bgm_instance:
                SoundManager.bgm_instance.stop()  # Matikan musik
            # Ubah ikon ke 'off'
            self.music_icon.source = "./assets/off.png"

    def dismiss_with_sound(self, instance):
        SoundManager.play_arrow_sound()
        self.dismiss()

    def update_avatar(self, new_avatar_path):
        self.current_avatar_path = new_avatar_path
        self.animated_avatar.update_animation(new_avatar_path, 6)
        self.update_avatar_position(SettingsManager.get_difficulty())
