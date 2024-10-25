import time
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.clock import Clock
from components.animated_widget import AnimatedImage
from components.common_ui import ImageButton
from components.popup.result_popup import ResultPopup
from components.popup.show_result_finish_popup import ResultPopupFinish
from components.popup.unlocked_popup import UnlockedPopup
from config import Config
from utils.game_utils import GameUtils
from utils.user_data_utils import UserDataUtils
from utils.constants import *
from utils.sound_manager import SoundManager
from components.ui.background import Background

resource_add_path("./assets/fonts/Bungee/")
LabelBase.register(name="Bungee", fn_regular=FONTS_PATH)


class SoalScreen(Screen):
    def __init__(self, zone, difficulty, level, avatar_path, **kwargs):
        super(SoalScreen, self).__init__(**kwargs)
        self.result_shown = False
        self.question_start_time = None
        self.time_threshold = 10
        self.zone = zone
        self.difficulty = difficulty
        self.level = level
        self.avatar_path = avatar_path
        self.current_question = 0
        self.score = 0
        self.level_score = 0
        self.wrong_answers = 0
        self.empty_heart_image = "./assets/kosong.png"
        self.remaining_hearts = UserDataUtils.get_remaining_hearts()
        self.max_hearts = 5
        self.heart_regen_interval = 15
        self.last_heart_regen_time = UserDataUtils.get_last_heart_regen_time()
        self.hearts = []
        self.heart_positions = []
        self.questions_data = UserDataUtils.load_questions(
            self.difficulty, self.zone, self.level
        )
        self.questions = self.questions_data["questions"]
        self.popup = None
        self.user_score = GameUtils.get_user_score()

        self.main_layout = RelativeLayout()

        self.background = Background()
        self.main_layout.add_widget(self.background)

        Clock.schedule_interval(self.check_heart_regeneration, 1)
        self.setup_ui()

    def setup_ui(self):
        hearts_y_position = 0.2
        back_btn = ImageButton(
            source="./assets/backk.png",
            size_hint=(None, None),
            size=Config.get_button_back_size(80, 80),
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

        self.hearts_layout = FloatLayout(
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.74, "center_y": 0.967},
        )
        for i in range(1, 5 + 1):
            if i <= self.remaining_hearts:
                heart_image = Image(
                    source=f"./assets/heart{i}.png",
                    size_hint=(None, None),
                    size=(100, 100),
                    pos_hint={
                        "center_x": 0.25 * i,
                        "center_y": hearts_y_position,
                    },
                )
            else:
                heart_image = Image(
                    source="./assets/kosong.png",
                    size_hint=(None, None),
                    size=(100, 100),
                    pos_hint={
                        "center_x": 0.25 * i,
                        "center_y": hearts_y_position,
                    },
                )

            self.hearts.append(heart_image)
            self.heart_positions.append(
                {"center_x": 0.2 * i, "center_y": hearts_y_position}
            )
            self.hearts_layout.add_widget(heart_image)

        self.animated_heart = AnimatedImage(
            base_path="./assets/avatar/gif/heart/frame_",
            frame_count=91,
            fps=30,
            size_hint=(None, None),
            image_size=(None, None),
            size=(100, 100),
        )
        self.animated_heart.opacity = 0

        self.main_layout.add_widget(self.hearts_layout)
        self.main_layout.add_widget(self.animated_heart)

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
        if not is_correct:
            self.handle_wrong_answer()
            if self.remaining_hearts <= 0:
                return

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

        if self.remaining_hearts > 0:
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
        self.update_user_progress()
        if self.result_shown:
            return
        self.result_shown = True
        total_score = self.score
        star_rating = self.calculate_star_rating()
        progress = UserDataUtils.load_user_progress()
        UserDataUtils.check_unlocked_avatars()

        unlocked_avatar = UserDataUtils.check_newly_unlocked_avatar(
            progress, self.zone, self.difficulty
        )
        print(f"ini uncloded avatar {unlocked_avatar}")
        if unlocked_avatar:

            def show_result_popup():
                self.popup = ResultPopupFinish(
                    total_score=total_score,
                    star_rating=star_rating,
                    level=self.level,
                    zone=self.zone,
                    level_score=self.level_score,
                    on_play_again=self.restart_quiz,
                    on_next_level=self.go_to_next_level,
                    on_menu_level=self.play_sound_and_go_back,
                )
                self.popup.open()

            unlocked_popup = UnlockedPopup(
                unlocked_avatar=unlocked_avatar, on_close_callback=show_result_popup
            )
            unlocked_popup.open()
        else:
            self.popup = ResultPopupFinish(
                total_score=total_score,
                star_rating=star_rating,
                level=self.level,
                zone=self.zone,
                level_score=self.level_score,
                on_play_again=self.restart_quiz,
                on_next_level=self.go_to_next_level,
                on_menu_level=self.play_sound_and_go_back,
            )
            self.popup.open()

    def check_heart_regeneration(self, dt):
        current_time = time.time()
        time_since_last_regen = current_time - self.last_heart_regen_time

        if (
            self.remaining_hearts < self.max_hearts
            and time_since_last_regen >= self.heart_regen_interval
        ):
            self.regenerate_heart()
            self.last_heart_regen_time = current_time
            UserDataUtils.save_last_heart_regen_time(current_time)

    def regenerate_heart(self):
        if self.remaining_hearts < self.max_hearts:
            self.remaining_hearts += 1
            UserDataUtils.save_remaining_hearts(self.remaining_hearts)

            # Update heart display
            heart_index = self.remaining_hearts - 1
            if heart_index >= 0 and heart_index < len(self.hearts):
                self.hearts[heart_index].source = f"./assets/heart{heart_index + 1}.png"
                self.hearts[heart_index].opacity = 1

    def handle_wrong_answer(self):
        self.wrong_answers += 1
        if self.wrong_answers == 3:
            hearts_x_positions = [0.668, 0.741, 0.814, 0.887, 0.96]
            self.remaining_hearts -= 1

            self.last_heart_regen_time = time.time()
            UserDataUtils.save_last_heart_regen_time(self.last_heart_regen_time)

            self.animated_heart.pos_hint = {
                "center_x": hearts_x_positions[self.remaining_hearts],
                "center_y": 0.955,
            }
            self.animated_heart.opacity = 1
            self.animated_heart.update_animation("./assets/avatar/gif/heart/frame_", 91)
            self.hearts[self.remaining_hearts].opacity = 0
            Clock.schedule_once(self.hide_animated_heart, 1)

            self.wrong_answers = 0
            Clock.schedule_once(self.reset_hearts, 1.5)
        if self.remaining_hearts <= 0:
            self.show_result()

    def reset_hearts(self, dt):
        for i in range(self.remaining_hearts):
            self.hearts[i].source = f"./assets/heart{i+1}.png"

    def hide_animated_heart(self, dt):
        self.animated_heart.opacity = 0
        Clock.schedule_once(self.show_empty_heart, 0.1)

    def show_empty_heart(self, dt):
        self.hearts[self.remaining_hearts].opacity = 1
        self.hearts[self.remaining_hearts].source = self.empty_heart_image

    def on_menu_level(self):
        pass

    def go_to_next_level(self, instance):
        SoundManager.play_arrow_sound()
        UserDataUtils.save_remaining_hearts(self.remaining_hearts)
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
        self.wrong_answers = 0
        self.result_shown = False
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

        self.wrong_answers = 0
        UserDataUtils.save_remaining_hearts(self.remaining_hearts)
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
