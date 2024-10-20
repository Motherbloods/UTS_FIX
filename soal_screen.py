import json
import os
import time
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.storage.jsonstore import JsonStore
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from components.animated_widget import AnimatedImage
from components.common_ui import ImageButton
from components.popup.result_popup import ResultPopup
from components.popup.show_result_finish_popup import ResultPopupFinish
from config import Config
from utils.game_utils import GameUtils
from utils.user_data_utils import UserDataUtils
from utils.constants import *
from utils.sound_manager import SoundManager
from components.background import Background

resource_add_path("./assets/fonts/Bungee/")
LabelBase.register(name="Bungee", fn_regular=FONTS_PATH)


class SoalScreen(Screen):
    def __init__(self, zone, difficulty, level, avatar_path, **kwargs):
        super(SoalScreen, self).__init__(**kwargs)
        self.question_start_time = None
        self.time_threshold = 10
        self.zone = zone
        self.difficulty = difficulty
        self.level = level
        self.avatar_path = avatar_path
        self.current_question = 0
        self.score = 0
        self.level_score = 0
        self.questions_data = UserDataUtils.load_questions(
            self.difficulty, self.zone, self.level
        )
        self.questions = self.questions_data["questions"]
        self.popup = None
        self.user_score = GameUtils.get_user_score()

        self.main_layout = RelativeLayout()

        self.background = Background()
        self.main_layout.add_widget(self.background)
        self.setup_ui()

    def setup_ui(self):
        back_btn = ImageButton(
            source="./assets/backk.png",
            size_hint=(None, None),
            size=Config.get_button_back_size(),
            pos_hint={"center_x": 0.12, "center_y": 0.95},
        )
        back_btn.bind(on_press=self.play_sound_and_go_back)
        self.main_layout.add_widget(back_btn)

        title_image = Image(
            source=self.questions_data["title"],
            size_hint=(None, None),
            size=Config.get_title_image_size(250, 90),
            pos_hint={"center_x": 0.5, "center_y": 0.95},
        )
        self.main_layout.add_widget(title_image)

        hearts_layout = FloatLayout(
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.74, "center_y": 0.967},
        )
        for i in range(1, 6):
            heart_image = Image(
                source=f"./assets/heart{i}.png",
                size_hint=(None, None),
                size=(100, 100),
                pos_hint={
                    "center_x": 0.25 * i,
                    "center_y": 0.2,
                },
            )
            hearts_layout.add_widget(heart_image)
        self.main_layout.add_widget(hearts_layout)

        self.soal_id_image = Image(
            size_hint=(None, None),
            size=Config.get_title_id_size(300, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.84},
        )
        self.main_layout.add_widget(self.soal_id_image)

        self.content_layout = FloatLayout(
            size_hint=(0.9, 0.7),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
        )
        self.question_image = Image(
            size_hint=(0.8, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.85},
        )
        self.options_layout = GridLayout(
            cols=2,
            size_hint=(1.1, 0.22),
            pos_hint={"center_x": 0.5, "center_y": 0.54},
        )

        self.content_layout.add_widget(self.question_image)
        self.content_layout.add_widget(self.options_layout)

        self.main_layout.add_widget(self.content_layout)

        self.animated_avatar = AnimatedImage(
            size_hint=(None, None),
            size=Config.get_animated_avatar_size(),
            base_path=self.avatar_path,
            frame_count=6,
            fps=10,
            pos_hint=AVATAR_POSITIONS[1],
            opacity=0,
        )
        self.main_layout.add_widget(self.animated_avatar)

        self.add_widget(self.main_layout)
        self.load_question()

    def load_user_score(self):
        return UserDataUtils.load_user_score()

    def load_questions(self):
        return UserDataUtils.load_questions(self.difficulty, self.zone, self.level)

    def load_question(self):
        return UserDataUtils.load_question(self)

    def check_answer(self, instance, option_number):
        SoundManager.play_arrow_sound()
        self.animated_avatar.opacity = 1
        self.animated_avatar.pos_hint = AVATAR_POSITIONS[option_number]
        time_taken = time.time() - self.question_start_time
        correct_answer = self.questions[self.current_question]["answer"]

        is_correct = instance.source == correct_answer
        if is_correct:
            score_increase = (
                SCORE_FAST_CORRECT
                if time_taken <= QUESTION_TIME_THRESHOLD
                else SCORE_CORRECT
            )
            self.score += 1
        else:
            score_increase = SCORE_INCORRECT
        self.level_score += score_increase
        self.user_score += score_increase
        GameUtils.save_user_score(self.user_score)

        if self.current_question == len(self.questions) - 1:
            self.show_result()
        else:
            self.show_answer_popup(is_correct, score_increase, time_taken)

    def show_answer_popup(self, is_correct, score_increase, time_taken):
        popup = ResultPopup(
            is_correct=is_correct,
            score_increase=score_increase,
            time_taken=time_taken,
            user_score=self.user_score,
            on_next=self.next_question,
            on_play_again=self.play_again,
        )
        popup.open()
        self.popup = popup

    def play_again(self, instance):
        SoundManager.play_arrow_sound()
        self.load_question()
        self.dismiss_popup()

    def next_question(self, instance):
        SoundManager.play_arrow_sound()
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.show_result()
        self.dismiss_popup()

    def dismiss_popup(self):
        if self.popup:
            self.popup.dismiss()
            self.popup = None

    def show_result(self):
        total_score = self.score
        star_rating = self.calculate_star_rating()

        self.popup = ResultPopupFinish(
            total_score=total_score,
            star_rating=star_rating,
            level=self.level,
            level_score=self.level_score,
            on_play_again=self.restart_quiz,
            on_next_level=self.go_to_next_level,
        )
        self.popup.open()

        self.update_user_progress()

    def go_to_next_level(self, instance):
        SoundManager.play_arrow_sound()
        self.dismiss_popup()
        next_level = self.level + 1
        App.get_running_app().stop()
        SoalApp(
            zone=self.zone,
            difficulty=self.difficulty,
            level=next_level,
            avatar_path=self.avatar_path,
        ).run()

    def calculate_star_rating(self):
        return GameUtils.calculate_star_rating(self.score, len(self.questions))

    def restart_quiz(self, instance):
        SoundManager.play_arrow_sound()
        self.dismiss_popup()
        self.current_question = 0
        self.score = 0
        self.level_score = 0
        self.content_layout.clear_widgets()
        self.content_layout.add_widget(self.question_image)
        self.content_layout.add_widget(self.options_layout)
        self.load_question()

    def update_user_progress(self):
        UserDataUtils.update_user_progress(
            zone=self.zone,
            difficulty=self.difficulty,
            level=self.level,
            score=self.score,
            questions=self.questions,
            calculate_star_rating_func=self.calculate_star_rating,
            compare_star_ratings_func=self.compare_star_ratings,
        )

    def compare_star_ratings(self, rating1, rating2):
        return GameUtils.compare_star_ratings(rating1, rating2)

    def play_sound_and_go_back(self, instance):
        SoundManager.play_arrow_sound()
        self.go_back(instance)

    def go_back(self, instance):
        App.get_running_app().stop()
        from level_screen import LevelScreenApp

        LevelScreenApp(
            zone_name=self.zone,
            difficulty=self.difficulty,
            avatar_path=self.avatar_path,
            static_avatar_path="path/to/static_avatar",
        ).run()


class SoalApp(App):
    def __init__(self, zone, difficulty, level, avatar_path, **kwargs):
        super(SoalApp, self).__init__(**kwargs)
        self.zone = zone
        self.difficulty = difficulty
        self.level = level
        self.avatar_path = avatar_path

    def build(self):
        return SoalScreen(
            zone=self.zone,
            difficulty=self.difficulty,
            level=self.level,
            avatar_path=self.avatar_path,
        )


if __name__ == "__main__":
    SoalApp(zone="aritmatika", difficulty="mudah", level=3).run()
