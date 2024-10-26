import time
from kivy.storage.jsonstore import JsonStore
from utils.constants import *
from utils.time_utils import *


class HeartsUtils:
    @staticmethod
    def get_remaining_hearts():
        store = JsonStore("user_progress.json")
        DEFAULT_HEARTS = 5
        HEART_REGEN_INTERVAL = 30  # dalam detik
        MAX_HEARTS = DEFAULT_HEARTS

        try:
            if store.exists("hearts"):
                hearts_data = store.get("hearts")
                stored_hearts = hearts_data.get("value", DEFAULT_HEARTS)
                last_regen_time_str = hearts_data.get(
                    "last_regen", TimeUtils.timestamp_to_time_string(time.time())
                )

                # Convert stored time string to timestamp
                last_regen_timestamp = TimeUtils.time_string_to_timestamp(
                    last_regen_time_str
                )

                if last_regen_timestamp is None:
                    current_time = TimeUtils.timestamp_to_time_string(time.time())
                    store.put("hearts", value=DEFAULT_HEARTS, last_regen=current_time)
                    return DEFAULT_HEARTS

                # Validasi nilai hearts
                if not isinstance(stored_hearts, (int, float)) or stored_hearts < 0:
                    current_time = TimeUtils.timestamp_to_time_string(time.time())
                    store.put("hearts", value=0, last_regen=current_time)
                    return 0

                if stored_hearts > MAX_HEARTS:
                    current_time = TimeUtils.timestamp_to_time_string(time.time())
                    store.put("hearts", value=MAX_HEARTS, last_regen=current_time)
                    return MAX_HEARTS

                # Hitung regenerasi hearts selama aplikasi tertutup
                current_time = time.time()
                elapsed_time = current_time - last_regen_timestamp

                # Hanya regenerasi jika hearts tidak penuh
                if stored_hearts < MAX_HEARTS:
                    regen_amount = int(elapsed_time // HEART_REGEN_INTERVAL)

                    if regen_amount > 0:
                        new_hearts = min(stored_hearts + regen_amount, MAX_HEARTS)

                        # Update timestamp regenerasi terakhir
                        if new_hearts == MAX_HEARTS:
                            # Jika hearts penuh, timestamp = waktu sekarang
                            new_last_regen = TimeUtils.timestamp_to_time_string(
                                current_time
                            )
                        else:
                            # Jika belum penuh, timestamp = waktu regenerasi terakhir yang tepat
                            new_last_regen_timestamp = last_regen_timestamp + (
                                regen_amount * HEART_REGEN_INTERVAL
                            )
                            new_last_regen = TimeUtils.timestamp_to_time_string(
                                new_last_regen_timestamp
                            )

                        # Simpan hearts baru dan waktu regenerasi
                        store.put("hearts", value=new_hearts, last_regen=new_last_regen)
                        return new_hearts

                return int(stored_hearts)

            # Jika tidak ada data hearts, inisialisasi dengan default
            current_time = TimeUtils.timestamp_to_time_string(time.time())
            store.put("hearts", value=DEFAULT_HEARTS, last_regen=current_time)
            return DEFAULT_HEARTS

        except Exception as e:
            print(f"Error reading hearts data: {str(e)}, using default value")
            return DEFAULT_HEARTS

    @staticmethod
    def save_remaining_hearts(hearts):
        try:
            store = JsonStore("user_progress.json")
            DEFAULT_HEARTS = 5

            # Validasi nilai hearts
            if hearts is None or not isinstance(hearts, (int, float)):
                print("Warning: Invalid hearts value, not saving")
                return False

            hearts = int(hearts)
            if hearts < 0:
                hearts = 0
            elif hearts > DEFAULT_HEARTS:
                hearts = DEFAULT_HEARTS

            # Simpan nilai hearts dan waktu terakhir
            current_time = TimeUtils.timestamp_to_time_string(time.time())

            # Jika hearts data sudah ada, pertahankan last_regen yang lama
            if store.exists("hearts"):
                existing_data = store.get("hearts")
                last_regen = existing_data.get("last_regen", current_time)
            else:
                last_regen = current_time

            store.put("hearts", value=hearts, last_regen=last_regen)
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
