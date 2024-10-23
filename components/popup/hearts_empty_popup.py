from kivy.uix.modalview import ModalView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from datetime import datetime, timedelta


class HeartsEmptyPopup(ModalView):
    def __init__(self, time_remaining, **kwargs):
        super(HeartsEmptyPopup, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.6)
        self.background = "./assets/popup.png"

        layout = FloatLayout()

        # Tambahkan gambar hati
        heart_image = Image(
            source="./assets/kosong.png",
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )

        # Hitung waktu yang diperlukan dalam format yang mudah dibaca
        hours = time_remaining // 3600
        minutes = (time_remaining % 3600) // 60

        # Label untuk pesan
        message_label = Label(
            text="Nyawa Kamu Habis!",
            font_name="Bungee",
            font_size="24sp",
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # Label untuk waktu
        time_label = Label(
            text=f"Waktu yang diperlukan\nuntuk nyawa penuh:\n{int(hours)} jam {int(minutes)} menit",
            font_name="Bungee",
            font_size="18sp",
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            halign="center",
        )

        layout.add_widget(heart_image)
        layout.add_widget(message_label)
        layout.add_widget(time_label)
        self.add_widget(layout)
