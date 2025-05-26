# --- START OF FILE game_states.py ---

import pygame # Diperlukan jika ada operasi pygame minor di sini, tapi umumnya tidak
from constants import GameConstants as GC
# from utils import load_image # Tidak lagi diperlukan di sini jika aset dikelola game_instance atau scene
# from dialogues import GAME_DIALOGUES # Tidak lagi diperlukan di sini

# Impor fungsi run dari file scene/mini-game masing-masing
from maze_game import run_maze_game
from awan_scene import run_awan_scene
from desa_2_scene import run_desa_2_scene
from spot_difference_game import run_spot_difference_game
from ending_game import run_ending_scene

# Impor fungsi run dari scene yang baru dibuat
from pre_stage_1a_scene import run_pre_stage_1a_scene
from pre_stage_1b_scene import run_pre_stage_1b_scene
from aft_stage_1b_scene import run_aft_stage_1b_scene


# --- Fungsi Setup State (Delegator) ---

def setup_main_menu(game_instance):
    print("Setup: Main Menu")
    game_instance.subtitle.reset()
    game_instance.current_dialog_index = -1
    game_instance.current_dialog_list = [] # Kosongkan dialog, karena menu mungkin tidak punya
    game_instance.current_left_char_img = None
    game_instance.current_right_char_img = None
    # Main Menu dikelola langsung oleh loop Game class

def setup_prologue(game_instance):
    print("Setup: Prologue")
    game_instance.subtitle.reset()
    game_instance.current_dialog_index = -1 # Mulai dialog dari awal
    game_instance.current_dialog_list = game_instance.get_current_dialogues(GC.STATE_STAGE_PROLOG)
    game_instance.show_next_dialog() # Tampilkan dialog pertama
    game_instance.current_left_char_img = game_instance.bimas_scaled_img
    game_instance.current_right_char_img = game_instance.king_scaled_img
    # Prolog dikelola langsung oleh loop Game class

def setup_pre_stage_1a(game_instance):
    print("Setup: Pre-Stage 1A -> Delegating to run_pre_stage_1a_scene")
    run_pre_stage_1a_scene(game_instance)

def setup_pre_stage_1b(game_instance):
    print("Setup: Pre-Stage 1B -> Delegating to run_pre_stage_1b_scene")
    run_pre_stage_1b_scene(game_instance)

def setup_stage_1_pacman(game_instance):
    print("Setup: Stage 1 (Pacman) -> Delegating to run_maze_game")
    run_maze_game(game_instance)

def setup_aft_stage_1b(game_instance):
    print("Setup: AFT-Stage 1B -> Delegating to run_aft_stage_1b_scene")
    run_aft_stage_1b_scene(game_instance)

def setup_state_awan(game_instance):
    print("Setup: Awan Scene -> Delegating to run_awan_scene")
    game_instance.subtitle.reset() 
    run_awan_scene(game_instance)

def setup_stage_2(game_instance):
    print("Setup: Stage 2 (Spot Difference) -> Delegating to run_spot_difference_game")
    run_spot_difference_game(game_instance)
    
def setup_desa_2(game_instance): 
    print("Setup: Desa 2 Scene -> Delegating to run_desa_2_scene")
    game_instance.subtitle.reset()
    run_desa_2_scene(game_instance)

def setup_final_stage(game_instance):
    print("Setup: Final Stage -> Delegating to run_ending_scene")
    game_instance.subtitle.reset()
    run_ending_scene(game_instance)

# def setup_game_over(game_instance): # Contoh jika ada state Game Over
#     print("Setup: Game Over")
#     game_instance.subtitle.reset()
#     # Mungkin ada dialog game over
#     # game_instance.current_dialog_list = game_instance.get_current_dialogues(GC.STATE_GAME_OVER)
#     # game_instance.show_next_dialog()
#     # Game Over dikelola langsung oleh loop Game class

# --- END OF FILE game_states.py ---