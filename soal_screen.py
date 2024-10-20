import json
import os
import time
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.clock import Clock
from components.animated_widget import AnimatedImage
from components.common_ui import ImageButton
from components.popup.result_popup import ResultPopup
from components.popup.show_result_finish_popup import ResultPopupFinish
from config import Config
from utils.game_utils import GameUtils
from utils.constants import *

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
        self.questions_data = self.load_questions()
        self.questions = self.questions_data["questions"]
        self.popup = None
        self.user_score = GameUtils.get_user_score()

        self.main_layout = RelativeLayout()

        self.background = GameUtils.setup_background(self.main_layout)
        self.setup_ui()

    def setup_ui(self):
        back_btn = ImageButton(
            source="./assets/backk.png",
            size_hint=(None, None),
            size=Config.get_button_back_size(),
            pos_hint={"center_x": 0.12, "center_y": 0.95},
        )
        back_btn.bind(on_press=self.go_back)
        self.main_layout.add_widget(back_btn)

        title_image = Image(
            source=self.questions_data["title"],
            size_hint=(None, None),
            size=Config.get_title_image_size(250, 90),
            pos_hint={"center_x": 0.5, "center_y": 0.95},
        )
        self.main_layout.add_widget(title_image)

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
        store = JsonStore("user_progress.json")
        if store.exists("user_score"):
            return store.get("user_score")["score"]
        else:
            store.put("user_score", score=0)
            return 0

    def save_user_score(self):
        store = JsonStore("user_progress.json")
        store.put("user_score", score=self.user_score)

    def load_questions(self):
        file_path = f"./soal/{self.difficulty}/{self.zone}.json"
        with open(file_path, "r") as file:
            data = json.load(file)
        return data[f"lessons_{self.zone}"][self.level - 1]

    def load_question(self):
        if self.current_question < len(self.questions):
            self.question_start_time = time.time()
            question = self.questions[self.current_question]
            self.question_image.source = question["question"]
            self.soal_id_image.source = question["soal_id"]
            self.options_layout.clear_widgets()

            base_path = f"./assets/soal/{self.difficulty}/{self.zone}/option/{self.level}/soal_{self.current_question + 1}/"

            for i in range(1, 5):
                option_path = os.path.join(base_path, f"{i}.png")
                option_button = ImageButton(
                    source=option_path,
                    size_hint=(0.4, 0.5),
                    allow_stretch=True,
                    keep_ratio=True,
                )
                option_button.bind(
                    on_press=lambda instance, i=i: self.check_answer(instance, i)
                )
                self.options_layout.add_widget(option_button)
            self.animated_avatar.opacity = 0
        else:
            self.show_result()

    def check_answer(self, instance, option_number):
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
        self.load_question()
        self.dismiss_popup()

    def next_question(self, instance):
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
        self.dismiss_popup()
        self.current_question = 0
        self.score = 0
        self.level_score = 0
        self.content_layout.clear_widgets()
        self.content_layout.add_widget(self.question_image)
        self.content_layout.add_widget(self.options_layout)
        self.load_question()

    def update_user_progress(self):
        store = JsonStore("user_progress.json")
        current_progress = (
            store.get("user_progress") if store.exists("user_progress") else {}
        )

        current_level_key = f"{self.zone}_{self.difficulty}_current_level"
        level_scores_key = f"{self.zone}_{self.difficulty}_level_scores"

        current_level = current_progress.get(current_level_key, 1)
        level_scores = current_progress.get(level_scores_key, {})

        star_rating = self.calculate_star_rating()

        level_key = f"{self.zone}_{self.difficulty}_{self.level}"
        existing_score = level_scores.get(level_key, {})
        existing_star_rating = existing_score.get("star_rating", "0B")
        if self.compare_star_ratings(star_rating, existing_star_rating) > 0:

            level_scores[level_key] = {
                "score": self.score,
                "total_questions": len(self.questions),
                "star_rating": star_rating,
            }
        else:

            if level_key not in level_scores:

                level_scores[level_key] = {
                    "score": self.score,
                    "total_questions": len(self.questions),
                    "star_rating": star_rating,
                }

        if self.level == current_level and self.score > 0:
            current_progress[current_level_key] = current_level + 1

        current_progress[level_scores_key] = level_scores
        store.put("user_progress", **current_progress)

    def compare_star_ratings(self, rating1, rating2):

        rating_order = ["0B", "1B", "1_5B", "2B", "2_5B", "3B"]
        return rating_order.index(rating1) - rating_order.index(rating2)

    def _update_rect(self, instance, value):
        self.background.pos = instance.pos
        self.background.size = instance.size

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
