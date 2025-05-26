# buttons_data.py
from constants import GameConstants as GC
from utils import load_image
from buttons import Button 

def get_game_buttons(game_instance):
    BUTTON_SIZE_MENU = (GC.BUTTON_WIDTH, GC.BUTTON_HEIGHT)
    BUTTON_SIZE_NAV = (200, 60) 
    BUTTON_CONGRATS_WIDTH = 280 
    BUTTON_CONGRATS_SIZE = (BUTTON_CONGRATS_WIDTH, GC.BUTTON_HEIGHT)

    img_play_normal, img_play_hover, img_exit_normal, img_exit_hover = None, None, None, None
    img_next_normal, img_next_hover = None, None
    img_menu_normal, img_menu_hover = None, None # Untuk tombol "Main Menu" di congrats

    try:
        img_play_normal = load_image("data/images/entities/play.png", BUTTON_SIZE_MENU)
        img_play_hover = load_image("data/images/entities/playhov.png", BUTTON_SIZE_MENU)
        img_exit_normal = load_image("data/images/entities/exit.png", BUTTON_SIZE_MENU)
        img_exit_hover = load_image("data/images/entities/exithov.png", BUTTON_SIZE_MENU)
        
        img_next_normal = load_image("data/images/entities/next.png", BUTTON_SIZE_NAV)
        img_next_hover = load_image("data/images/entities/nexthov.png", BUTTON_SIZE_NAV)

        # Ganti 'play.png' dengan gambar tombol "Main Menu" jika Anda punya
        img_menu_normal = load_image("data/images/entities/play.png", BUTTON_CONGRATS_SIZE) 
        img_menu_hover = load_image("data/images/entities/playhov.png", BUTTON_CONGRATS_SIZE) 
    except Exception as e:
        print(f"Error loading button images in buttons_data.py: {e}")
        # Set semua ke None agar Button class bisa buat placeholder jika ada error load
        img_play_normal, img_play_hover, img_exit_normal, img_exit_hover, \
        img_next_normal, img_next_hover, img_menu_normal, img_menu_hover = [None] * 8


    center_x = game_instance.screen_rect.centerx
    center_y = game_instance.screen_rect.centery

    button_menu_x = center_x - (BUTTON_SIZE_MENU[0] // 2)
    play_button_y = center_y - BUTTON_SIZE_MENU[1] - GC.BUTTON_GAP // 2 
    exit_button_y = center_y + GC.BUTTON_GAP // 2      

    next_button_x_right_bottom = GC.SCREEN_WIDTH - BUTTON_SIZE_NAV[0] - GC.BUTTON_MARGIN
    next_button_y_bottom = GC.SCREEN_HEIGHT - BUTTON_SIZE_NAV[1] - GC.BUTTON_MARGIN
    
    next_button_x_center_bottom = center_x - (BUTTON_SIZE_NAV[0] // 2)
    
    congrats_button_y = center_y + 150 
    congrats_button_gap = 40
    total_congrats_buttons_width = BUTTON_CONGRATS_SIZE[0] * 2 + congrats_button_gap
    
    congrats_menu_btn_x = center_x - total_congrats_buttons_width // 2
    congrats_exit_btn_x = congrats_menu_btn_x + BUTTON_CONGRATS_SIZE[0] + congrats_button_gap

    def prolog_next_action():
        print("DEBUG: prolog_next_action CALLED")
        if game_instance.subtitle.is_animating():
            print("DEBUG: Prolog - Fast forwarding subtitle")
            game_instance.subtitle.fast_forward()
        elif game_instance.current_dialog_index < len(game_instance.current_dialog_list) - 1:
            print("DEBUG: Prolog - Showing next dialog")
            game_instance.show_next_dialog() 
        else: 
            if game_instance.subtitle.is_showing() and not game_instance.subtitle.is_finished():
                 game_instance.subtitle.fast_forward()
                 print("DEBUG: Prolog - Fast forward sisa dialog terakhir")
            else:
                print("DEBUG: Prolog - Semua dialog selesai. Transisi ke Pre-Stage 1A.")
                game_instance.subtitle.reset() 
                # PERBAIKAN: Gunakan fade_type="out"
                game_instance.transition.start(GC.STATE_PRE_STAGE_1A, fade_type="out") 

    buttons_config = {
        GC.STATE_MAIN_MENU: [
            Button(
                image_normal=img_play_normal, image_hover=img_play_hover,
                x=button_menu_x, y=play_button_y,
                # PERBAIKAN DI SINI: Ganti fade_in menjadi fade_type
                action=lambda: game_instance.transition.start(GC.STATE_STAGE_PROLOG, fade_type="out")
            ),
            Button(
                image_normal=img_exit_normal, image_hover=img_exit_hover,
                x=button_menu_x, y=exit_button_y,
                action=game_instance.quit_game
            ),
        ],
        GC.STATE_STAGE_PROLOG: [
             Button(
                image_normal=img_next_normal, image_hover=img_next_hover,
                x=next_button_x_right_bottom, y=next_button_y_bottom, 
                action=prolog_next_action # Aksi ini sudah menggunakan fade_type="out"
             )
        ],
        GC.STATE_CONGRATULATIONS: [
            Button(
                image_normal=img_menu_normal, image_hover=img_menu_hover, 
                x=congrats_menu_btn_x, y=congrats_button_y,
                # PERBAIKAN DI SINI: Ganti fade_in menjadi fade_type
                action=lambda: game_instance.transition.start(GC.STATE_MAIN_MENU, fade_type="out")
            ),
            Button(
                image_normal=img_exit_normal, image_hover=img_exit_hover, 
                x=congrats_exit_btn_x, y=congrats_button_y,
                action=game_instance.quit_game
            )
        ],
        GC.STATE_GAME_OVER: [ 
             Button(
                image_normal=img_next_normal, image_hover=img_next_hover,
                x=next_button_x_right_bottom, y=next_button_y_bottom, # Atau tengahkan jika lebih baik
                # PERBAIKAN DI SINI: Ganti fade_in menjadi fade_type
                action=lambda: game_instance.transition.start(GC.STATE_MAIN_MENU, fade_type="out")
             )
        ]
        # Tambahkan konfigurasi tombol untuk state lain jika diperlukan
    }
    return buttons_config