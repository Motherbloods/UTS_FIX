import time
from kivy.storage.jsonstore import JsonStore
from utils.constants import *
from utils.time_utils import *


class HeartsUtils:
    @staticmethod
    def get_remaining_hearts():
        store = JsonStore("user_progress.json")
        DEFAULT_HEARTS = 5
        HEART_REGEN_INTERVAL = 30
        MAX_HEARTS = DEFAULT_HEARTS

        try:
            # Mendapatkan data dari store
            if store.exists("hearts"):
                hearts_data = store.get("hearts")
                stored_hearts = hearts_data.get("value", DEFAULT_HEARTS)
                last_regen_time_str = hearts_data.get(
                    "last_regen", TimeUtils.timestamp_to_time_string(time.time())
                )

                # Convert stored time string to timestamp for calculations
                last_regen_timestamp = TimeUtils.time_string_to_timestamp(
                    last_regen_time_str
                )

                if last_regen_timestamp is None:
                    current_time = TimeUtils.timestamp_to_time_string(time.time())
                    store.put("hearts", value=stored_hearts, last_regen=current_time)
                    return stored_hearts

                # Validasi nilai hati yang tersimpan
                if stored_hearts is not None and isinstance(
                    stored_hearts, (int, float)
                ):
                    if stored_hearts < 0:
                        current_time = TimeUtils.timestamp_to_time_string(time.time())
                        store.put("hearts", value=0, last_regen=current_time)
                        return 0
                    elif stored_hearts > MAX_HEARTS:
                        current_time = TimeUtils.timestamp_to_time_string(time.time())
                        store.put("hearts", value=MAX_HEARTS, last_regen=current_time)
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
                            new_last_regen_timestamp = last_regen_timestamp + (
                                regen_amount * HEART_REGEN_INTERVAL
                            )
                            new_last_regen_time = TimeUtils.timestamp_to_time_string(
                                new_last_regen_timestamp
                            )
                            store.put(
                                "hearts",
                                value=new_hearts,
                                last_regen=new_last_regen_time,
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

            current_time = TimeUtils.timestamp_to_time_string(time.time())
            store.put("hearts", value=DEFAULT_HEARTS, last_regen=current_time)
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
        """Get heart regeneration time as timestamp"""
        store = JsonStore("user_progress.json")
        if store.exists("last_heart_regen"):
            time_string = store.get("last_heart_regen")["timestamp"]
            return TimeUtils.time_string_to_timestamp(time_string)
        else:
            current_time = TimeUtils.timestamp_to_time_string(time.time())
            store.put("last_heart_regen", timestamp=current_time)
            return time.time()

    @staticmethod
    def save_last_heart_regen_time(timestamp):
        """Save heart regeneration time in HH:MM:SS format"""
        store = JsonStore("user_progress.json")
        time_string = TimeUtils.timestamp_to_time_string(timestamp)
        store.put("last_heart_regen", timestamp=time_string)
