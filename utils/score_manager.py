from kivy.storage.jsonstore import JsonStore


class ScoreManager:
    def __init__(self):
        self.store = JsonStore("user_progress.json")

    def get_current_level(self):
        if self.store.exists("user_progress"):
            return self.store.get("user_progress")["current_level"]
        else:
            self.store.put("user_progress", current_level=1)
            return 1

    def get_level_scores(self):
        if self.store.exists("user_progress"):
            progress = self.store.get("user_progress")
            return progress.get("level_scores", {})
        return {}

    def get_user_score(self):
        if self.store.exists("user_score"):
            return self.store.get("user_score")["score"]
        else:
            self.store.put("user_score", score=0)
            return 0

    def calculate_total_stars(self):
        total_stars = 0
        for level_data in self.get_level_scores().values():
            star_rating = level_data.get("star_rating", "0B")
            total_stars += self.convert_star_rating_to_number(star_rating)
        return total_stars

    def convert_star_rating_to_number(self, star_rating):
        star_values = {"3B": 3, "2_5B": 2.5, "2B": 2, "1_5B": 1.5, "1B": 1, "0B": 0}
        return star_values.get(star_rating, 0)

    def update_user_score(self, score):
        self.store.put("user_score", score=score)

    def update_level_progress(
        self, zone, difficulty, level, score, total_questions, star_rating
    ):
        current_progress = self.store.get("user_progress")

        if "level_scores" not in current_progress:
            current_progress["level_scores"] = {}

        level_key = f"{zone}_{difficulty}_{level}"
        existing_score = current_progress["level_scores"].get(level_key, {})
        existing_star_rating = existing_score.get("star_rating", "0B")

        if self.compare_star_ratings(star_rating, existing_star_rating) > 0:
            current_progress["level_scores"][level_key] = {
                "score": score,
                "total_questions": total_questions,
                "star_rating": star_rating,
            }

        if level == current_progress["current_level"] and score > 0:
            current_progress["current_level"] = current_progress["current_level"] + 1

        self.store.put("user_progress", **current_progress)

    def compare_star_ratings(self, rating1, rating2):
        rating_order = ["0B", "1B", "1_5B", "2B", "2_5B", "3B"]
        return rating_order.index(rating1) - rating_order.index(rating2)
