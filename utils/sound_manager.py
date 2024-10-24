from kivy.core.audio import SoundLoader


class SoundManager:
    bgm_instance = None
    arrow_sound = None

    @classmethod
    def initialize_bgm(cls):
        if cls.bgm_instance is None:
            cls.bgm_instance = SoundLoader.load("./assets/bgm.mp3")
            if cls.bgm_instance:
                cls.bgm_instance.loop = True
                cls.bgm_instance.play()

    @classmethod
    def stop_bgm(cls):
        if cls.bgm_instance:
            cls.bgm_instance.stop()
            cls.bgm_instance = None

    @classmethod
    def initialize_arrow_sound(cls):
        if cls.arrow_sound is None:
            cls.arrow_sound = SoundLoader.load("./assets/arrow_music.mp3")

    @classmethod
    def play_arrow_sound(cls):
        if cls.arrow_sound:
            cls.arrow_sound.play()

    @staticmethod
    def play_sound(sound_path):
        sound = SoundLoader.load("./assets/aplause.mp3")
        if sound:
            sound.play()
