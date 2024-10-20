from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from kivy.graphics import Rectangle


class GameUtils:
    @staticmethod
    def setup_background(widget, background_path="./assets/bg.png"):
        """Setup background for a widget"""
        with widget.canvas.before:
            background = Rectangle(
                source=background_path,
                pos=widget.pos,
                size=widget.size,
            )
        widget.bind(
            size=lambda instance, value: GameUtils.update_rect(
                instance, value, background
            ),
            pos=lambda instance, value: GameUtils.update_rect(
                instance, value, background
            ),
        )
        return background

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
        """Compare two star ratings"""
        rating_order = ["0B", "1B", "1_5B", "2B", "2_5B", "3B"]
        return rating_order.index(rating1) - rating_order.index(rating2)

    @staticmethod
    def calculate_star_rating(score, total_questions):
        """Calculate star rating based on score percentage"""
        score_percentage = (score / total_questions) * 100
        if score_percentage == 100:
            return "3B"
        elif score_percentage >= 80:
            return "2_5B"
        elif score_percentage >= 60:
            return "2B"
        elif score_percentage >= 40:
            return "1_5B"
        else:
            return "1B"
