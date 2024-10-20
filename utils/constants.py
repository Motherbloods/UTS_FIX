from kivy.utils import get_color_from_hex

# Colors
CUSTOM_COLOR = get_color_from_hex("#050a30")

# Paths
BACKGROUND_PATH = "./assets/bg.png"
BACK_BUTTON_PATH = "./assets/backk.png"
FONTS_PATH = "./assets/fonts/Bungee/Bungee-Regular.ttf"

# Storage
PROGRESS_FILE = "user_progress.json"

# Avatar positions
AVATAR_POSITIONS = {
    1: {"center_x": 0.05, "center_y": 0.5},
    2: {"center_x": 0.9, "center_y": 0.5},
    3: {"center_x": 0.05, "center_y": 0.41},
    4: {"center_x": 0.9, "center_y": 0.41},
}

# Time thresholds
QUESTION_TIME_THRESHOLD = 10

# Scores
SCORE_FAST_CORRECT = 500
SCORE_CORRECT = 250
SCORE_INCORRECT = -100
