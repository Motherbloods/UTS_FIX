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

AVATAR_OPTIONS = {
    (
        "./assets/avatar/png/male.png",
        "Veldora",
    ): "./assets/avatar/gif/male/male-",
    (
        "./assets/avatar/png/female.png",
        "Asismant",
    ): "./assets/avatar/gif/female/female-",
    (
        "./assets/avatar/png/ninja.png",
        "Tuple",
    ): "./assets/avatar/gif/ninja/ninja-",
}

LOCKED_AVATARS = [
    (
        "./assets/avatar/png/lock/bee.png",
        "Bee",
        "./assets/avatar/png/hover/bee.png",
        "./assets/avatar/gif/bee/bee-",
    ),
    (
        "./assets/avatar/png/lock/knight.png",
        "Knight",
        "./assets/avatar/png/hover/knight.png",
        "./assets/avatar/gif/knight/knight-",
    ),
    (
        "./assets/avatar/png/lock/rogue.png",
        "Rogue",
        "./assets/avatar/png/hover/rogue.png",
        "./assets/avatar/gif/rogue/rogue-",
    ),
    (
        "./assets/avatar/png/lock/punk.png",
        "Punk",
        "./assets/avatar/png/hover/punk.png",
        "./assets/avatar/gif/punk/punk-",
    ),
    (
        "./assets/avatar/png/lock/roger.png",
        "Roger",
        "./assets/avatar/png/hover/roger.png",
        "./assets/avatar/gif/roger/roger-",
    ),
    (
        "./assets/avatar/png/lock/wizard.png",
        "Wizard",
        "./assets/avatar/png/hover/wizard.png",
        "./assets/avatar/gif/wizard/wizard-",
    ),
]

LOCKED_AVATARSsss = [
    (
        "./assets/avatar/png/lock/bee.png",
        "Bee",
        "./assets/avatar/png/hover/bee.png",
        "./assets/avatar/gif/bee/bee-",
        "Kamu Harus Menyelesaikan Zone Kelas 1 Mode Mudah",
    ),
    (
        "./assets/avatar/png/lock/knight.png",
        "Knight",
        "./assets/avatar/png/hover/knight.png",
        "./assets/avatar/gif/knight/knight-",
        "Kamu Harus Menyelesaikan Zone Kelas 2 Mode Mudah untuk membuka avatar Knight",
    ),
    (
        "./assets/avatar/png/lock/rogue.png",
        "Rogue",
        "./assets/avatar/png/hover/rogue.png",
        "./assets/avatar/gif/rogue/rogue-",
        "Kamu Harus Menyelesaikan Zone Kelas 1 Mode Mudah untuk membuka avatar Rogue",
    ),
    (
        "./assets/avatar/png/lock/punk.png",
        "Punk",
        "./assets/avatar/png/hover/punk.png",
        "./assets/avatar/gif/punk/punk-",
        "Kamu Harus Menyelesaikan Zone Kelas 2 Mode Sedang untuk membuka avatar Punk",
    ),
    (
        "./assets/avatar/png/lock/roger.png",
        "Roger",
        "./assets/avatar/png/hover/roger.png",
        "./assets/avatar/gif/roger/roger-",
        "Kamu Harus Menyelesaikan Zone Kelas 3 Mode Sedang untuk membuka avatar Roger",
    ),
    (
        "./assets/avatar/png/lock/wizard.png",
        "Wizard",
        "./assets/avatar/png/hover/wizard.png",
        "./assets/avatar/gif/wizard/wizard-",
        "Kamu harus menyelesaikan semua Zone dan Mode untuk membuka avatar Wizzard",
    ),
]

AVATAR_UNLOCK_REQUIREMENTS = {
    "bee": {"difficulty": "mudah", "class": 1, "all_levels": True},
    "knight": {"difficulty": "mudah", "class": 2, "all_levels": True},
    "rogue": {"difficulty": "mudah", "class": 3, "all_levels": True},
    "punk": {"difficulty": "sedang", "class": 2, "all_levels": True},
    "roger": {"difficulty": "sedang", "class": 3, "all_levels": True},
    "wizard": {"difficulty": "all", "class": "all", "all_levels": True},
}
LOCKED_AVATARSsss = [
    (
        "./assets/avatar/png/lock/bee.png",
        "Bee",
        "./assets/avatar/png/hover/bee.png",
        "./assets/avatar/gif/bee/bee-",
        "Kamu Harus Menyelesaikan Zone Kelas 1 Mode Mudah",
    ),
    (
        "./assets/avatar/png/lock/knight.png",
        "Knight",
        "./assets/avatar/png/hover/knight.png",
        "./assets/avatar/gif/knight/knight-",
        "Kamu Harus Menyelesaikan Zone Kelas 2 Mode Mudah untuk membuka avatar Knight",
    ),
    (
        "./assets/avatar/png/lock/rogue.png",
        "Rogue",
        "./assets/avatar/png/hover/rogue.png",
        "./assets/avatar/gif/rogue/rogue-",
        "Kamu Harus Menyelesaikan Zone Kelas 1 Mode Mudah untuk membuka avatar Rogue",
    ),
    (
        "./assets/avatar/png/lock/punk.png",
        "Punk",
        "./assets/avatar/png/hover/punk.png",
        "./assets/avatar/gif/punk/punk-",
        "Kamu Harus Menyelesaikan Zone Kelas 2 Mode Sedang untuk membuka avatar Punk",
    ),
    (
        "./assets/avatar/png/lock/roger.png",
        "Roger",
        "./assets/avatar/png/hover/roger.png",
        "./assets/avatar/gif/roger/roger-",
        "Kamu Harus Menyelesaikan Zone Kelas 3 Mode Sedang untuk membuka avatar Roger",
    ),
    (
        "./assets/avatar/png/lock/wizard.png",
        "Wizard",
        "./assets/avatar/png/hover/wizard.png",
        "./assets/avatar/gif/wizard/wizard-",
        "Kamu harus menyelesaikan semua Zone dan Mode untuk membuka avatar Wizzard",
    ),
]

DEFAULT_AVATAR_OPTIONS = {
    (
        "./assets/avatar/png/male.png",
        "Veldora",
    ): "./assets/avatar/gif/male/male-",
    (
        "./assets/avatar/png/female.png",
        "Asismant",
    ): "./assets/avatar/gif/female/female-",
    (
        "./assets/avatar/png/ninja.png",
        "Tuple",
    ): "./assets/avatar/gif/ninja/ninja-",
}
