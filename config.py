from kivy.core.window import Window


class Config:

    BASE_WIDTH = 450
    BASE_HEIGHT = int(BASE_WIDTH * (16 / 9))

    SCREEN_WIDTH, SCREEN_HEIGHT = Window.size

    SCALE_X = SCREEN_WIDTH / BASE_WIDTH
    SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT

    @classmethod
    def scaled_size(cls, width, height):
        return (width * cls.SCALE_X, height * cls.SCALE_Y)

    @classmethod
    def scaled_pos(cls, x, y):
        return (x * cls.SCALE_X, y * cls.SCALE_Y)

    @classmethod
    def scaled_font_size(cls, size):
        return size * min(cls.SCALE_X, cls.SCALE_Y)

    @classmethod
    def get_avatar_size(cls, x, y):
        return cls.scaled_size(x, y)

    @classmethod
    def get_settings_icon_size(cls):
        return cls.scaled_size(65, 65)

    @classmethod
    def get_title_id_size(cls, x, y):
        return cls.scaled_size(x, y)

    @classmethod
    def get_title_image_size(cls, x, y):
        return cls.scaled_size(x, y)

    @classmethod
    def get_animated_avatar_size(cls):
        return cls.scaled_size(100, 100)

    @classmethod
    def get_button_layout_size(cls):
        return cls.scaled_size(150, 150)

    @classmethod
    def get_button_back_size(cls, x, y):
        return cls.scaled_size(x, y)

    @classmethod
    def get_image_zone_size(cls):
        return cls.scaled_size(500, 240)

    @classmethod
    def get_avatar_popup_size(cls):
        return cls.scaled_size(600, 600)

    @classmethod
    def get_settings_popup_size(cls):
        width = cls.SCREEN_WIDTH * 0.92
        height = width * (625 / 1080)
        return (width, height)

    @classmethod
    def get_title_font_size(cls):
        return cls.scaled_font_size(32)

    @classmethod
    def get_label_font_size(cls):
        return cls.scaled_font_size(24)

    CUSTOM_COLOR = "#050a30"
