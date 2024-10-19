from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button


class ResultPopupFinish(Popup):
    def __init__(
        self, total_score, star_rating, level, on_play_again, on_next_level, **kwargs
    ):
        super(ResultPopupFinish, self).__init__(**kwargs)
        self.title = "Quiz Completed!"
        self.size_hint = (None, None)
        self.size = (300, 400)

        content = FloatLayout()

        # Total score label
        score_label = Label(
            text=f"Total Score: {total_score}",
            font_size=24,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.8},
        )
        content.add_widget(score_label)

        # Star rating image
        star_image = Image(
            source=f"./assets/level/{star_rating}/{level}.png",
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        content.add_widget(star_image)

        # Play Again button
        play_again_btn = Button(
            text="Play Again",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={"center_x": 0.3, "center_y": 0.3},
        )
        play_again_btn.bind(on_release=on_play_again)
        content.add_widget(play_again_btn)

        # Next Level button
        next_level_btn = Button(
            text="Next Level",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={"center_x": 0.7, "center_y": 0.3},
        )
        next_level_btn.bind(on_release=on_next_level)
        content.add_widget(next_level_btn)

        self.content = content
