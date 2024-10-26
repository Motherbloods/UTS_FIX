from datetime import datetime
import time


class TimeUtils:
    @staticmethod
    def timestamp_to_time_string(timestamp):
        """Convert timestamp to HH:MM:SS format"""
        return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")

    @staticmethod
    def time_string_to_timestamp(time_string):
        """Convert HH:MM:SS format to timestamp"""
        try:
            current_date = datetime.now().date()
            full_datetime = datetime.strptime(
                f"{current_date} {time_string}", "%Y-%m-%d %H:%M:%S"
            )
            return full_datetime.timestamp()
        except ValueError:
            return time.time()  # Return current timestamp if conversion fails
