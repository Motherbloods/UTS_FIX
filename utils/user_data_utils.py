import json
import os
import time
from components.common_ui import ImageButton
from kivy.storage.jsonstore import JsonStore
from utils.constants import *


class UserDataUtils:
    _cached_progress = None
    AVATAR_UNLOCK_REQUIREMENTS = {
        "Bee": {"difficulty": "mudah", "class": 1},
        "Knight": {"difficulty": "mudah", "class": 2},
        "Rogue": {"difficulty": "mudah", "class": 3},
        "Punk": {"difficulty": "sedang", "class": 2},
        "Roger": {"difficulty": "sedang", "class": 3},
        "Wizard": {"difficulty": "all", "class": "all"},
    }

    @staticmethod
    def save_avatar_selection(static_path, animated_base_path):
        """Save the user's avatar selection to persistent storage"""
        store = JsonStore("user_progress.json")
        store.put(
            "avatar_selection",
            static_path=static_path,
            animated_base_path=animated_base_path,
        )

    @staticmethod
    def load_avatar_selection():
        """Load the user's saved avatar selection"""
        store = JsonStore("user_progress.json")
        if store.exists("avatar_selection"):
            selection = store.get("avatar_selection")
            return selection["static_path"], selection["animated_base_path"]
        return "./assets/avatar/png/ninja.png", "./assets/avatar/gif/male/male-"

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
        UserDataUtils._cached_progress = current_progress
        return current_progress

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
        DEFAULT_HEARTS = 5
        HEART_REGEN_INTERVAL = 90  # Interval regenerasi dalam detik
        MAX_HEARTS = DEFAULT_HEARTS

        try:
            # Mendapatkan data dari store
            if store.exists("hearts"):
                hearts_data = store.get("hearts")

                # Memeriksa nilai hati dan waktu regenerasi yang tersimpan
                stored_hearts = hearts_data.get(
                    "value", DEFAULT_HEARTS
                )  # Ambil nilai hati atau default
                last_regen_timestamp = hearts_data.get(
                    "last_regen", None
                )  # Ambil last_regen atau None

                # Jika tidak ada last_regen, inisialisasi dengan waktu sekarang
                if last_regen_timestamp is None:
                    print("No last_regen found, initializing with current time")
                    last_regen_timestamp = time.time()
                    store.put(
                        "hearts", value=stored_hearts, last_regen=last_regen_timestamp
                    )

                # Validasi nilai hati yang tersimpan
                if stored_hearts is not None and isinstance(
                    stored_hearts, (int, float)
                ):
                    if stored_hearts < 0:
                        print(
                            "Warning: Invalid negative hearts value found, resetting to 0"
                        )
                        store.put("hearts", value=0, last_regen=time.time())
                        return 0
                    elif stored_hearts > MAX_HEARTS:
                        print(
                            f"Warning: Hearts value {stored_hearts} exceeds maximum, resetting to {MAX_HEARTS}"
                        )
                        store.put("hearts", value=MAX_HEARTS, last_regen=time.time())
                        return MAX_HEARTS

                    # Menghitung waktu yang berlalu sejak regenerasi terakhir
                    current_time = time.time()
                    elapsed_time = current_time - last_regen_timestamp

                    # Debugging: Print nilai waktu yang telah berlalu
                    print(f"Elapsed time since last regen: {elapsed_time} seconds")

                    regen_amount = int(elapsed_time // HEART_REGEN_INTERVAL)

                    # Jika cukup waktu berlalu untuk meregenerasi hati
                    if regen_amount > 0:
                        new_hearts = min(stored_hearts + regen_amount, MAX_HEARTS)

                        # Debugging: Print jumlah hati yang baru dan regenerasi
                        print(
                            f"Regenerated {regen_amount} hearts. New total: {new_hearts}"
                        )

                        # Perbarui waktu regenerasi terakhir
                        if new_hearts == MAX_HEARTS:
                            # Jika hati mencapai maksimum, setel last_regen menjadi waktu sekarang
                            store.put(
                                "hearts", value=new_hearts, last_regen=current_time
                            )
                        else:
                            # Jika belum maksimum, setel last_regen berdasarkan waktu yang tersisa
                            new_last_regen = last_regen_timestamp + (
                                regen_amount * HEART_REGEN_INTERVAL
                            )
                            store.put(
                                "hearts", value=new_hearts, last_regen=new_last_regen
                            )

                        return new_hearts

                    # Tidak ada hati yang bisa diregenerasi
                    return int(stored_hearts)
                else:
                    print(
                        "Warning: Invalid hearts value found, initializing with default"
                    )
            else:
                print("Info: No hearts data found, initializing with default")

            # Jika data hati tidak valid atau tidak ada, inisialisasi dengan default
            store.put("hearts", value=DEFAULT_HEARTS, last_regen=time.time())
            return DEFAULT_HEARTS

        except Exception as e:
            print(f"Error reading hearts data: {str(e)}, using default value")
            return DEFAULT_HEARTS

    @staticmethod
    def save_remaining_hearts(hearts):
        try:
            DEFAULT_HEARTS = 5
            # Validate hearts value before saving
            if hearts is None or not isinstance(hearts, (int, float)):
                print("Warning: Invalid hearts value, not saving")
                return False

            hearts = int(hearts)  # Convert to integer
            if hearts < 0:
                hearts = 0
            elif hearts > DEFAULT_HEARTS:
                hearts = DEFAULT_HEARTS

            store = JsonStore("user_progress.json")
            store.put("hearts", value=hearts)
            return True

        except Exception as e:
            print(f"Error saving hearts data: {str(e)}")
            return False

    @staticmethod
    def get_last_heart_regen_time():
        store = JsonStore("user_progress.json")
        if store.exists("last_heart_regen"):
            return store.get("last_heart_regen")["timestamp"]
        else:
            current_time = time.time()
            store.put("last_heart_regen", timestamp=current_time)
            return current_time

    @staticmethod
    def save_last_heart_regen_time(timestamp):
        store = JsonStore("user_progress.json")
        store.put("last_heart_regen", timestamp=timestamp)

    @staticmethod
    def load_user_progress():
        store = JsonStore("user_progress.json")
        if store.exists("user_progress"):
            return store.get("user_progress")
        return {}

    @staticmethod
    def check_zone_completion(progress, zone, difficulty):
        zone_scores = progress.get(f"{zone}_{difficulty}_level_scores", {})
        if not zone_scores:
            return False
        total_levels = 9
        completed_levels = 0

        for level in range(1, total_levels + 1):
            level_key = f"{zone}_{difficulty}_{level}"
            if level_key in zone_scores:
                level_data = zone_scores[level_key]
                if level_data.get("score", 0) > 0:
                    completed_levels += 1
        return completed_levels == total_levels

    @staticmethod
    def check_unlocked_avatars():
        progress = UserDataUtils.load_user_progress()

        unlocked_avatars = list(AVATAR_OPTIONS.items())
        unlocked_avatarrs = dict(DEFAULT_AVATAR_OPTIONS)

        for avatar_data in LOCKED_AVATARS[:]:
            static_path, name, hover_path, gif_path = avatar_data
            avatar_key = name.lower()
            should_unlock = False
            if avatar_key == "bee":
                should_unlock = UserDataUtils.check_zone_completion(
                    progress, "kelas_1", "mudah"
                )

            elif avatar_key == "knight":
                should_unlock = UserDataUtils.check_zone_completion(
                    progress, "kelas_2", "mudah"
                )

            elif avatar_key == "rogue":
                should_unlock = UserDataUtils.check_zone_completion(
                    progress, "kelas_3", "mudah"
                )

            elif avatar_key == "punk":
                should_unlock = UserDataUtils.check_zone_completion(
                    progress, "kelas_2", "sedang"
                )

            elif avatar_key == "roger":
                should_unlock = UserDataUtils.check_zone_completion(
                    progress, "kelas_3", "sedang"
                )

            elif avatar_key == "wizard":
                should_unlock = True
                # Check all zones and difficulties
                for zone in ["kelas_1", "kelas_2", "kelas_3"]:
                    for difficulty in ["mudah", "sedang", "sulit"]:
                        if not UserDataUtils.check_zone_completion(
                            progress, zone, difficulty
                        ):
                            should_unlock = False
                            break
                    if not should_unlock:
                        break

            if should_unlock:
                # Convert locked avatar to unlocked format
                new_avatar = (static_path.replace("/lock/", "/"), name), gif_path
                unlocked_path = static_path.replace("/lock/", "/")
                new_avatar_key = (unlocked_path, name)
                unlocked_avatarrs[new_avatar_key] = gif_path

                if new_avatar not in unlocked_avatars:
                    unlocked_avatars.append(new_avatar)
                    LOCKED_AVATARS.remove(avatar_data)

        AVATAR_OPTIONS.clear()
        AVATAR_OPTIONS.update(dict(unlocked_avatars))

    @staticmethod
    def check_newly_unlocked_avatar(progress, zone, level):
        UserDataUtils.initialize_unlocked_avatars_tracking()
        current_class = int(zone.split("_")[1]) if "_" in zone else None
        newly_unlocked = None
        for (
            avatar_name,
            requirements,
        ) in UserDataUtils.AVATAR_UNLOCK_REQUIREMENTS.items():
            if UserDataUtils.is_avatar_already_unlocked(avatar_name):
                continue
            if requirements["class"] == "all" and zone == "kelas_3":
                all_completed = True
                for z in ["kelas_1", "kelas_2", "kelas_3"]:
                    for d in ["mudah", "sedang", "sulit"]:
                        if not UserDataUtils.check_zone_completion(progress, z, d):
                            all_completed = False
                            break
                if all_completed:
                    newly_unlocked = avatar_name

            elif requirements["class"] == current_class:
                if requirements["difficulty"] == "mudah":
                    if UserDataUtils.check_zone_completion(progress, zone, "mudah"):
                        newly_unlocked = avatar_name
                elif requirements["difficulty"] == "sedang":
                    if UserDataUtils.check_zone_completion(progress, zone, "sedang"):
                        newly_unlocked = avatar_name
        if newly_unlocked:
            UserDataUtils.mark_avatar_as_unlocked(newly_unlocked)
        return newly_unlocked

    @staticmethod
    def initialize_unlocked_avatars_tracking():
        store = JsonStore("user_progress.json")
        if not store.exists("unlocked_avatars"):
            store.put(
                "unlocked_avatars",
                avatars=["ninja", "male", "female"],
            )

    @staticmethod
    def is_avatar_already_unlocked(avatar_name):
        """Check if an avatar has been previously unlocked"""
        store = JsonStore("user_progress.json")
        if not store.exists("unlocked_avatars"):
            UserDataUtils.initialize_unlocked_avatars_tracking()
        unlocked_avatars = store.get("unlocked_avatars")["avatars"]
        return avatar_name.lower() in [a.lower() for a in unlocked_avatars]

    @staticmethod
    def mark_avatar_as_unlocked(avatar_name):
        """Mark an avatar as unlocked in persistent storage"""
        if not avatar_name:
            return

        store = JsonStore("user_progress.json")
        if not store.exists("unlocked_avatars"):
            UserDataUtils.initialize_unlocked_avatars_tracking()

        current_unlocked = store.get("unlocked_avatars")["avatars"]
        avatar_name = avatar_name.lower()

        if avatar_name not in [a.lower() for a in current_unlocked]:
            current_unlocked.append(avatar_name)
            store.put("unlocked_avatars", avatars=current_unlocked)
