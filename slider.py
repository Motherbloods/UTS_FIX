from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.lang import Builder

# Define the KV string for both sliders
kv = """
<CustomSlider@Slider>:
    cursor_image: 'knob.png'
    cursor_size: (250, 250)
    background_width: 0
    padding: 20
    background_horizontal: ''
    background_disabled_horizontal: ''
    background_vertical: ''
    background_disabled_vertical: ''

<SliderLayout>:
    canvas.before:
        Rectangle:
            pos: self.pos[0], self.pos[1] - self.size[1]/4
            size: self.size[0], self.size[1] * 1.5
            source: 'sliderisi.png'
    
    CustomSlider:
        id: slider
        size_hint: 0.6, 0.1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        min: 0
        max: 1
        value: 0.5
"""


class ClickableImage(ButtonBehavior, Image):
    pass


class SliderLayout(FloatLayout):
    pass


# Memuat KV string saat aplikasi dimulai
Builder.load_string(kv)


class SplashScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class menuGame(Screen):
    pass


class homeScreen(Screen):
    def __init__(self, **kwargs):
        super(homeScreen, self).__init__(**kwargs)
        self.button_sound = SoundLoader.load("assets/music/soundButton/soundButton.MP3")
        if not self.button_sound:
            print("Error: Sound file not found or failed to load.")
        Clock.schedule_once(self.build_ui, 0.5)

    def on_enter(self):
        print("Home screen muncul, mulai musik in-game")
        app = App.get_running_app()
        app.start_background_music()

    def play_button_sound(self):
        app = App.get_running_app()
        if self.button_sound:
            self.button_sound.volume = app.sfx_volume
            self.button_sound.play()

    def build_ui(self, dt):
        main_menu_layout = FloatLayout()

        # Background dan logo
        bgAwal = Image(
            source="assets/img/background.JPG", allow_stretch=True, keep_ratio=False
        )
        main_menu_layout.add_widget(bgAwal)
        logoTebakGambar = Image(
            source="assets/img/logo.png",
            size_hint=(None, None),
            size=(500, 500),
            pos_hint={"center_x": 0.5, "center_y": 0.8},
        )
        main_menu_layout.add_widget(logoTebakGambar)

        # Tombol Play dengan animasi Zoom In dan Zoom Out
        self.mulaiBTn = ClickableImage(
            size_hint=(None, None),
            size=(500, 500),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            source="assets/img/play.png",
        )

        # Tombol Exit
        keluarBTn = ClickableImage(
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={"right": 1, "top": 1},
            source="assets/img/exit.png",
        )

        # Bind tombol ke fungsi
        self.mulaiBTn.bind(on_press=self.play_button_and_switch)
        keluarBTn.bind(on_press=self.play_button_and_exit_confirm)

        # Tambahkan tombol ke layout
        main_menu_layout.add_widget(self.mulaiBTn)
        main_menu_layout.add_widget(keluarBTn)

        # Tombol settings dengan gambar options.png
        print("Menambahkan tombol settings...")
        try:
            self.settings_button = ClickableImage(
                source="assets/gif/setting.gif",
                size_hint=(None, None),
                size=(100, 100),
                pos_hint={"x": 0.02, "top": 1},
            )
            self.settings_button.bind(on_press=self.play_button_and_settings)
            main_menu_layout.add_widget(self.settings_button)
            print("Tombol settings ditambahkan.")
        except Exception as e:
            print(f"Error loading settings button: {e}")

        self.add_widget(main_menu_layout)
        self.animate_play_button()

    def animate_play_button(self):
        anim = Animation(size=(450, 450), duration=1) + Animation(
            size=(400, 400), duration=1
        )
        anim.repeat = True
        anim.start(self.mulaiBTn)

    def play_button_and_switch(self, instance):
        self.play_button_sound()
        Clock.schedule_once(self.switch_to_menu_game, 0.3)

    def switch_to_menu_game(self, dt):
        self.manager.current = "menu_game"

    def play_button_and_exit_confirm(self, instance):
        self.play_button_sound()
        Clock.schedule_once(self.show_exit_popup, 0.3)

    def show_exit_popup(self, dt):
        try:
            # Layout pop-up
            popup_layout = FloatLayout()

            # Tombol untuk 'Ya' dan 'Tidak' menggunakan gambar
            ya_button = ClickableImage(
                source="assets/img/Keluar/iya.png",
                size_hint=(None, None),
                size=(300, 150),
                pos_hint={"center_x": 0.3, "y": 0.4},
            )
            ya_button.bind(on_press=self.exit_app)

            tidak_button = ClickableImage(
                source="assets/img/Keluar/tidak.png",
                size_hint=(None, None),
                size=(300, 150),
                pos_hint={"center_x": 0.7, "y": 0.4},
            )
            tidak_button.bind(on_press=lambda x: exit_popup.dismiss())

            popup_layout.add_widget(ya_button)
            popup_layout.add_widget(tidak_button)

            exit_popup = Popup(
                title="",
                title_size=0,
                separator_height=0,
                content=popup_layout,
                size_hint=(0.75, 0.5),
                auto_dismiss=True,
                background="assets/img/Keluar/bg.png",
            )
            exit_popup.open()

        except Exception as e:
            print(f"Error showing exit popup: {e}")

    def play_button_and_settings(self, instance):
        self.play_button_sound()
        self.show_settings_popup(instance)

    def show_settings_popup(self, instance):
        try:
            app = App.get_running_app()

            popup_layout = FloatLayout()

            # Gambar untuk SFX dan BGM
            sfx_bg = Image(
                source="assets/img/options/sfx.png",
                size_hint=(None, None),
                size=(100, 100),
                pos_hint={"x": 0.1, "y": 0.55},
            )
            bgm_bg = Image(
                source="assets/img/options/bgm.png",
                size_hint=(None, None),
                size=(100, 100),
                pos_hint={"x": 0.1, "y": 0.45},
            )

            popup_layout.add_widget(sfx_bg)
            popup_layout.add_widget(bgm_bg)

            # Slider SFX kustom dengan SliderLayout
            sfx_slider_layout = SliderLayout()
            sfx_slider_layout.size_hint = (0.5, 0.2)
            sfx_slider_layout.pos_hint = {"x": 0.35, "y": 0.5}
            # Bind slider value ke fungsi update volume
            sfx_slider_layout.ids.slider.value = app.sfx_volume
            sfx_slider_layout.ids.slider.bind(
                value=lambda instance, value: app.update_sfx_volume(value)
            )
            popup_layout.add_widget(sfx_slider_layout)

            # Slider BGM kustom dengan SliderLayout
            bgm_slider_layout = SliderLayout()
            bgm_slider_layout.size_hint = (0.5, 0.2)
            bgm_slider_layout.pos_hint = {"x": 0.35, "y": 0.4}
            # Bind slider value ke fungsi update volume
            bgm_slider_layout.ids.slider.value = app.bgm_volume
            bgm_slider_layout.ids.slider.bind(
                value=lambda instance, value: app.update_bgm_volume(value)
            )
            popup_layout.add_widget(bgm_slider_layout)

            # Tombol tutup
            close_button = ClickableImage(
                source="assets/img/x.png",
                size_hint=(None, None),
                size=(150, 150),
                pos_hint={"right": 0.97, "top": 0.80},
            )
            close_button.bind(on_press=lambda x: settings_popup.dismiss())
            popup_layout.add_widget(close_button)

            settings_popup = Popup(
                title="",
                title_size=0,
                separator_height=0,
                content=popup_layout,
                size_hint=(1, 0.8),
                auto_dismiss=True,
                background="assets/img/options/bgOptions.png",
            )
            settings_popup.open()

        except Exception as e:
            print(f"Error showing settings popup: {e}")

    def exit_app(self, instance):
        App.get_running_app().stop()


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.bgm_volume = 0.5
        self.sfx_volume = 0.5
        self.background_music = None

    def build(self):
        # Create the screen manager
        sm = ScreenManager(transition=FadeTransition())

        # Add screens
        sm.add_widget(homeScreen(name="home"))
        sm.add_widget(menuGame(name="menu_game"))
        sm.add_widget(GameScreen(name="game"))

        return sm

    def start_background_music(self):
        if not self.background_music:
            self.background_music = SoundLoader.load("assets/music/bgm/bgm.MP3")
            if self.background_music:
                self.background_music.volume = self.bgm_volume
                self.background_music.loop = True
                self.background_music.play()

    def update_bgm_volume(self, value):
        self.bgm_volume = value
        if self.background_music:
            self.background_music.volume = value

    def update_sfx_volume(self, value):
        self.sfx_volume = value


if __name__ == "__main__":
    MainApp().run()
