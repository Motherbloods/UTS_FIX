import json
import os
import time
from components.common_ui import ImageButton
from kivy.storage.jsonstore import JsonStore


class UserDataUtils:
    @staticmethod
    def load_user_score():
        store = JsonStore("user_progress.json")
        if store.exists("user_score"):
            return store.get("user_score")["score"]
        else:
            store.put("user_score", score=0)
            return 0

    @staticmethod
    def load_questions(difficulty, zone, level):
        file_path = f"./soal/{difficulty}/{zone}.json"
        with open(file_path, "r") as file:
            data = json.load(file)
        return data[f"lessons_{zone}"][level - 1]

    @staticmethod
    def setup_question(
        question_data, options_layout, question_image, soal_id_image, current_question
    ):
        question = question_data["questions"][current_question]
        question_image.source = question["question"]
        soal_id_image.source = question["soal_id"]
        options_layout.clear_widgets()

        base_path = f"./assets/soal/{question_data['difficulty']}/{question_data['zone']}/option/{question_data['level']}/soal_{current_question + 1}/"

        return {"question": question, "base_path": base_path}

    @staticmethod
    def update_user_progress(
        zone,
        difficulty,
        level,
        score,
        questions,
        calculate_star_rating_func,
        compare_star_ratings_func,
    ):
        store = JsonStore("user_progress.json")
        current_progress = (
            store.get("user_progress") if store.exists("user_progress") else {}
        )

        current_level_key = f"{zone}_{difficulty}_current_level"
        level_scores_key = f"{zone}_{difficulty}_level_scores"

        current_level = current_progress.get(current_level_key, 1)
        level_scores = current_progress.get(level_scores_key, {})

        star_rating = calculate_star_rating_func()

        level_key = f"{zone}_{difficulty}_{level}"
        existing_score = level_scores.get(level_key, {})
        existing_star_rating = existing_score.get("star_rating", "0B")
        if compare_star_ratings_func(star_rating, existing_star_rating) > 0:

            level_scores[level_key] = {
                "score": score,
                "total_questions": len(questions),
                "star_rating": star_rating,
            }
        else:

            if level_key not in level_scores:

                level_scores[level_key] = {
                    "score": score,
                    "total_questions": len(questions),
                    "star_rating": star_rating,
                }

        if level == current_level and score > 0:
            current_progress[current_level_key] = current_level + 1

        current_progress[level_scores_key] = level_scores
        store.put("user_progress", **current_progress)

    def load_question(screen_instance):
        if screen_instance.current_question < len(screen_instance.questions):
            screen_instance.question_start_time = time.time()
            question = screen_instance.questions[screen_instance.current_question]
            screen_instance.question_image.source = question["question"]
            screen_instance.soal_id_image.source = question["soal_id"]
            screen_instance.options_layout.clear_widgets()

            base_path = f"./assets/soal/{screen_instance.difficulty}/{screen_instance.zone}/option/{screen_instance.level}/soal_{screen_instance.current_question + 1}/"

            for i in range(1, 5):
                option_path = os.path.join(base_path, f"{i}.png")
                option_button = ImageButton(
                    source=option_path,
                    size_hint=(0.4, 0.5),
                    allow_stretch=True,
                    keep_ratio=True,
                )
                option_button.bind(
                    on_press=lambda instance, i=i: screen_instance.check_answer(
                        instance, i
                    )
                )
                screen_instance.options_layout.add_widget(option_button)
            screen_instance.animated_avatar.opacity = 0
        else:
            screen_instance.show_result()

    @staticmethod
    def get_remaining_hearts():
        store = JsonStore("user_progress.json")
        if store.exists("hearts"):
            return store.get("hearts")["value"]
        else:
            # Default value if not set
            return 5

    @staticmethod
    def save_remaining_hearts(hearts):
        store = JsonStore("user_progress.json")
        store.put("hearts", value=hearts)
