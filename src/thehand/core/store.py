import pygame as pg

from .configs import DEFAULT_WINDOW_SIZE
from .utils import asset_path

# ===============================================
# Standard 8-Bit RGB Color Definitions (0-255)
# ===============================================

# Primary Colors (Additive)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

# Secondary Colors (Mixing Primaries)
COLOR_YELLOW = (255, 255, 0)  # Red + Green
COLOR_CYAN = (0, 255, 255)  # Green + Blue (also called Aqua)
COLOR_MAGENTA = (255, 0, 255)  # Red + Blue (also called Fuchsia)

# Achromatic Colors (Gray Scale)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_DARK_GRAY = (64, 64, 64)
COLOR_LIGHT_GRAY = (192, 192, 192)

# Dark/Half-Intensity Colors (128 component values)
COLOR_MAROON = (128, 0, 0)  # Dark Red
COLOR_OLIVE = (128, 128, 0)  # Dark Yellow/Khaki
COLOR_NAVY = (0, 0, 128)  # Dark Blue
COLOR_TEAL = (0, 128, 128)  # Dark Cyan
COLOR_PURPLE = (128, 0, 128)  # Dark Magenta
COLOR_LIME = (0, 128, 0)  # Dark Green (sometimes called Lime)

# Tertiary/Other Common Colors
COLOR_ORANGE = (255, 165, 0)
COLOR_BROWN = (165, 42, 42)
COLOR_PINK = (255, 192, 203)
COLOR_GOLD = (255, 215, 0)
COLOR_SILVER = (192, 192, 192)

# ===============================================
# Catppuccin Mocha Flavor Palette (Dark Theme)
# Based on 8-Bit RGB Color Definitions (0-255)
# ===============================================

# Accent Colors (Vivid Pastels)
# These are the primary, most colorful shades.
COLOR_MOCHA_ROSEWATER = (245, 224, 220)  # Rosewater / #f5e0dc
COLOR_MOCHA_FLAMINGO = (242, 205, 205)  # Flamingo / #f2cdcd
COLOR_MOCHA_PINK = (245, 194, 231)  # Pink / #f5c2e7
COLOR_MOCHA_MAUVE = (203, 166, 247)  # Mauve / #cba6f7
COLOR_MOCHA_RED = (243, 139, 168)  # Red / #f38ba8
COLOR_MOCHA_MAROON = (235, 160, 172)  # Maroon / #eba0ac
COLOR_MOCHA_PEACH = (250, 179, 135)  # Peach / #fab387
COLOR_MOCHA_YELLOW = (249, 226, 175)  # Yellow / #f9e2af
COLOR_MOCHA_GREEN = (166, 227, 161)  # Green / #a6e3a1
COLOR_MOCHA_TEAL = (148, 226, 213)  # Teal / #94e2d5
COLOR_MOCHA_SKY = (137, 220, 235)  # Sky / #89dceb
COLOR_MOCHA_SAPPHIRE = (116, 199, 236)  # Sapphire / #74c7ec
COLOR_MOCHA_BLUE = (137, 180, 250)  # Blue / #89b4fa
COLOR_MOCHA_LAVENDER = (180, 190, 254)  # Lavender / #b4befe

# Monochromatic Colors (Text and Background)
# These define the main surfaces, foreground, and subtext.
COLOR_MOCHA_TEXT = (205, 214, 244)  # Text / #cdd6f4
COLOR_MOCHA_SUBTEXT1 = (186, 194, 222)  # Subtext 1 / #bac2de
COLOR_MOCHA_SUBTEXT0 = (166, 173, 200)  # Subtext 0 / #a6adc8
COLOR_MOCHA_OVERLAY2 = (147, 153, 178)  # Overlay 2 / #9399b2
COLOR_MOCHA_OVERLAY1 = (127, 132, 156)  # Overlay 1 / #7f849c
COLOR_MOCHA_OVERLAY0 = (108, 112, 134)  # Overlay 0 / #6c7086
COLOR_MOCHA_SURFACE2 = (88, 91, 112)  # Surface 2 / #585b70
COLOR_MOCHA_SURFACE1 = (69, 71, 90)  # Surface 1 / #45475a
COLOR_MOCHA_SURFACE0 = (49, 50, 68)  # Surface 0 / #313244
COLOR_MOCHA_BASE = (30, 30, 46)  # Base (Main Background) / #1e1e2e
COLOR_MOCHA_MANTLE = (24, 24, 37)  # Mantle (Darker Background) / #181825
COLOR_MOCHA_CRUST = (17, 17, 27)  # Crust (Deepest Background) / #11111b


class Store:
    def __init__(self) -> None:
        self.screen: pg.Surface = pg.Surface(DEFAULT_WINDOW_SIZE)

        self.font_sys = pg.font.SysFont("Comic Sans MS", 24)

        self.font_display_64 = pg.font.Font(asset_path("fonts", "MajorMonoDisplay.ttf"), 64)
        self.font_display_48 = pg.font.Font(asset_path("fonts", "MajorMonoDisplay.ttf"), 48)
        self.font_display_32 = pg.font.Font(asset_path("fonts", "MajorMonoDisplay.ttf"), 32)

        self.font_text_32 = pg.font.Font(asset_path("fonts", "SpaceMono.ttf"), 32)
        self.font_text_24 = pg.font.Font(asset_path("fonts", "SpaceMono.ttf"), 24)
        self.font_text_18 = pg.font.Font(asset_path("fonts", "SpaceMono.ttf"), 18)

        self.font_pixel_36 = pg.font.Font(asset_path("fonts", "PixeloidSansBold.ttf"), 36)
        self.font_pixel_24 = pg.font.Font(asset_path("fonts", "PixeloidSansBold.ttf"), 24)
        self.font_pixel_18 = pg.font.Font(asset_path("fonts", "PixeloidSansBold.ttf"), 18)

        self.imgs: dict[str, pg.Surface] = {
            "flying_comets": pg.image.load(asset_path("imgs", "flying_comets.jpg")),
            "mlrs_00": pg.image.load(asset_path("imgs", "mlrs_00.jpg")),
            "mlrs_01": pg.image.load(asset_path("imgs", "mlrs_01.jpg")),
            "pacman_bg_gray": pg.image.load(asset_path("imgs", "pacman_bg_gray.jpg")),
            "pacman_bg": pg.image.load(asset_path("imgs", "pacman_bg.jpg")),
            "tutorial_00_00": pg.image.load(asset_path("imgs", "tutorial_00_00.jpg")),
            "tutorial_00_01": pg.image.load(asset_path("imgs", "tutorial_00_01.jpg")),
            "tutorial_00_02": pg.image.load(asset_path("imgs", "tutorial_00_02.jpg")),
            "tutorial_01_00": pg.image.load(asset_path("imgs", "tutorial_01_00.jpg")),
            "tutorial_01_01": pg.image.load(asset_path("imgs", "tutorial_01_01.jpg")),
            "tutorial_01_02": pg.image.load(asset_path("imgs", "tutorial_01_02.jpg")),
            "tutorial_01_03": pg.image.load(asset_path("imgs", "tutorial_01_03.jpg")),
            "tutorial_02_00": pg.image.load(asset_path("imgs", "tutorial_02_00.jpg")),
            "tutorial_02_01": pg.image.load(asset_path("imgs", "tutorial_02_01.jpg")),
            "tutorial_02_02": pg.image.load(asset_path("imgs", "tutorial_02_02.jpg")),
            "apple": pg.image.load(asset_path("imgs", "apple.png")),
            "ghost_blinky": pg.image.load(asset_path("imgs", "ghost_blinky.png")),
            "ghost_blue": pg.image.load(asset_path("imgs", "ghost_blue.png")),
            "ghost_clyde": pg.image.load(asset_path("imgs", "ghost_clyde.png")),
            "ghost_inky": pg.image.load(asset_path("imgs", "ghost_inky.png")),
            "ghost_pinky": pg.image.load(asset_path("imgs", "ghost_pinky.png")),
            "pacman_close_down": pg.image.load(asset_path("imgs", "pacman_close_down.png")),
            "pacman_close_left": pg.image.load(asset_path("imgs", "pacman_close_left.png")),
            "pacman_close_right": pg.image.load(asset_path("imgs", "pacman_close_right.png")),
            "pacman_close_up": pg.image.load(asset_path("imgs", "pacman_close_up.png")),
            "pacman_down": pg.image.load(asset_path("imgs", "pacman_down.png")),
            "pacman_left": pg.image.load(asset_path("imgs", "pacman_left.png")),
            "pacman_right": pg.image.load(asset_path("imgs", "pacman_right.png")),
            "pacman_up": pg.image.load(asset_path("imgs", "pacman_up.png")),
            "strawberry": pg.image.load(asset_path("imgs", "strawberry.png")),
            "thehand_icon": pg.image.load(asset_path("imgs", "thehand_icon.png")),
            "thehand": pg.image.load(asset_path("imgs", "thehand.png")),
        }

        self.sounds: dict[str, pg.mixer.Sound] = {
            "ambient_rain": pg.mixer.Sound(asset_path("audio", "ambient_rain.mp3")),
            "auughhh": pg.mixer.Sound(asset_path("audio", "auughhh.mp3")),
            "button_launch": pg.mixer.Sound(asset_path("audio", "button_launch.mp3")),
            "danger_alarm": pg.mixer.Sound(asset_path("audio", "danger_alarm.mp3")),
            "error": pg.mixer.Sound(asset_path("audio", "error.mp3")),
            "fbi_open_up": pg.mixer.Sound(asset_path("audio", "fbi_open_up.mp3")),
            "fire_in_the_hole": pg.mixer.Sound(asset_path("audio", "fire_in_the_hole.mp3")),
            "green_screen": pg.mixer.Sound(asset_path("audio", "green_screen.mp3")),
            "gta_v_death": pg.mixer.Sound(asset_path("audio", "gta_v_death.mp3")),
            "gun": pg.mixer.Sound(asset_path("audio", "gun.mp3")),
            "heavy_eating": pg.mixer.Sound(asset_path("audio", "heavy_eating.mp3")),
            "mlrs_00_welcome": pg.mixer.Sound(asset_path("audio", "mlrs_00_welcome.mp3")),
            "mlrs_01_defeated": pg.mixer.Sound(asset_path("audio", "mlrs_01_defeated.mp3")),
            "mlrs_02_rocket": pg.mixer.Sound(asset_path("audio", "mlrs_02_rocket.mp3")),
            "mlrs_03_fire": pg.mixer.Sound(asset_path("audio", "mlrs_03_fire.mp3")),
            "mlrs_04_easy": pg.mixer.Sound(asset_path("audio", "mlrs_04_easy.mp3")),
            "mlrs_05_launch": pg.mixer.Sound(asset_path("audio", "mlrs_05_launch.mp3")),
            "mlrs_06_weldone": pg.mixer.Sound(asset_path("audio", "mlrs_06_weldone.mp3")),
            "munch": pg.mixer.Sound(asset_path("audio", "munch.mp3")),
            "pacman_start": pg.mixer.Sound(asset_path("audio", "pacman_start.mp3")),
            "pacman_theme": pg.mixer.Sound(asset_path("audio", "pacman_theme.mp3")),
            "pacman_victory": pg.mixer.Sound(asset_path("audio", "pacman_victory.mp3")),
            "punch_gaming": pg.mixer.Sound(asset_path("audio", "punch_gaming.mp3")),
            "shocked": pg.mixer.Sound(asset_path("audio", "shocked.mp3")),
            "spiderman": pg.mixer.Sound(asset_path("audio", "spiderman_meme_song.mp3")),
            "tf_nemesis": pg.mixer.Sound(asset_path("audio", "tf_nemesis.mp3")),
            "vine_boom": pg.mixer.Sound(asset_path("audio", "vine_boom.mp3")),
            "windows_xp_startup": pg.mixer.Sound(asset_path("audio", "windows_xp_startup.mp3")),
        }
