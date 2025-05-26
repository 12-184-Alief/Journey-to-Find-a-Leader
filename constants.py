# constants.py
class GameConstants:
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    FPS = 60 

    FONT_SIZE_LARGE = 60
    FONT_SIZE_MEDIUM = 30
    FONT_SIZE_SMALL = 20

    # Definisi State Game
    STATE_MAIN_MENU = "main_menu"
    STATE_STAGE_PROLOG = "stage_prolog"
    STATE_PRE_STAGE_1A = "pre_stage_1a"
    STATE_PRE_STAGE_1B = "pre_stage_1b"     # Desa 1 sebelum Pacman
    STATE_STAGE_1 = "stage_1"               # Pacman (maze_game.py)
    STATE_AFT_STAGE_1B = "aft_stage_1b"     # Desa 1 setelah Pacman
    STATE_AWAN = "state_awan"
    STATE_STAGE_2 = "stage_2"               # Spot Difference
    STATE_DESA_2 = "desa_2"
    STATE_FINAL = "final_stage"             # Ending scene
    STATE_CONGRATULATIONS = "congratulations" # Halaman Selamat
    STATE_GAME_OVER = "game_over"           # State Game Over

    # Konstanta untuk Tombol (jika masih relevan digunakan secara global)
    BUTTON_WIDTH = 300
    BUTTON_HEIGHT = 60
    BUTTON_SIZE_NEXT = (200, 60) # Mungkin lebih baik diatur di buttons_data.py
    BUTTON_GAP = 30
    BUTTON_VERTICAL_OFFSET = 125 # Mungkin lebih baik diatur di buttons_data.py
    BUTTON_MARGIN = 20