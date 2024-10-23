from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from kivy.graphics import Rectangle


class GameUtils:

    @staticmethod
    def update_rect(instance, value, background):
        """Update rectangle position and size"""
        background.pos = instance.pos
        background.size = instance.size

    @staticmethod
    def get_user_score():
        """Get user score from storage"""
        store = JsonStore("user_progress.json")
        if store.exists("user_score"):
            return store.get("user_score")["score"]
        else:
            store.put("user_score", score=0)
            return 0

    @staticmethod
    def save_user_score(score):
        """Save user score to storage"""
        store = JsonStore("user_progress.json")
        store.put("user_score", score=score)

    @staticmethod
    def get_user_progress():
        """Get user progress from storage"""
        store = JsonStore("user_progress.json")
        if store.exists("user_progress"):
            return store.get("user_progress")
        return {}

    @staticmethod
    def save_user_progress(progress):
        """Save user progress to storage"""
        store = JsonStore("user_progress.json")
        store.put("user_progress", **progress)

    @staticmethod
    def compare_star_ratings(rating1, rating2):
        rating_order = ["0B", "1B", "1_5B", "2B", "2_5B", "3B"]
        return rating_order.index(rating1) - rating_order.index(rating2)

    @staticmethod
    def calculate_star_rating(score, total_questions):
        score_percentage = (score / total_questions) * 100
        if score_percentage == 100:
            return "3B"
        elif score_percentage >= 80:
            return "2_5B"
        elif score_percentage >= 60:
            return "2B"
        elif score_percentage >= 40:
            return "1_5B"
        elif score_percentage >= 20:
            return "1B"
        else:
            return "0B"

    @staticmethod
    def calculate_total_stars(level_scores):
        total_stars = 0
        for level_data in level_scores.values():
            star_rating = level_data.get("star_rating", "0B")
            if star_rating == "3B":
                total_stars += 3
            elif star_rating == "2_5B":
                total_stars += 2.5
            elif star_rating == "2B":
                total_stars += 2
            elif star_rating == "1_5B":
                total_stars += 1.5
            elif star_rating == "1B":
                total_stars += 1
        return total_stars

    @staticmethod
    def get_level_image_path(level, current_level, level_scores):
        if level > current_level:
            return "./assets/level/kunci.png"

        level_key = f"{level}"
        level_data = level_scores.get(level_key, {})
        star_rating = level_data.get("star_rating", "0B")

        if star_rating == "0B":
            return f"./assets/level/0B/{level}.png"
        elif star_rating == "1B":
            return f"./assets/level/1B/{level}.png"
        elif star_rating == "1_5B":
            return f"./assets/level/1_5B/{level}.png"
        elif star_rating == "2B":
            return f"./assets/level/2B/{level}.png"
        elif star_rating == "2_5B":
            return f"./assets/level/2_5B/{level}.png"
        elif star_rating == "3B":
            return f"./assets/level/3B/{level}.png"
        else:
            return f"./assets/level/0B/{level}.png"
