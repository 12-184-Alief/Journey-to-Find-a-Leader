# --- START OF FILE game.py ---

import pygame
import sys

# from buttons import Button 
from subtitle import Subtitle 
from transition import Transition 

from constants import GameConstants as GC
from utils import load_image 
from dialogues import GAME_DIALOGUES 
from buttons_data import get_game_buttons 

from game_states import (
    setup_main_menu,
    setup_prologue,
    setup_pre_stage_1a,
    setup_pre_stage_1b,
    setup_stage_1_pacman,
    setup_aft_stage_1b,
    setup_state_awan,
    setup_stage_2,
    setup_desa_2,
    setup_final_stage,
)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((GC.SCREEN_WIDTH, GC.SCREEN_HEIGHT))
        pygame.display.set_caption('Journey to Find a Leader')
        self.screen_rect = self.screen.get_rect()

        self.clock = pygame.time.Clock()

        self.state = GC.STATE_MAIN_MENU
        self.transition = Transition(1000) 
        self.subtitle = Subtitle(self.screen) # Pastikan screen dilewatkan

        try:
            self.font = pygame.font.Font("data/fonts/dogicapixelbold.otf", GC.FONT_SIZE_MEDIUM)
        except pygame.error as e:
            print(f"Warning: Font file not found or could not be loaded: {e}")
            self.font = pygame.font.Font(None, GC.FONT_SIZE_MEDIUM) 

        self.menu_bg = load_image("data/images/entities/menu.png", (GC.SCREEN_WIDTH, GC.SCREEN_HEIGHT))
        self.prolog_bg = load_image("data/images/entities/prolog_bg.png", (GC.SCREEN_WIDTH, GC.SCREEN_HEIGHT))
        self.pre_stage_1a_bg = load_image("data/images/entities/stage_1_bg.png", (GC.SCREEN_WIDTH, GC.SCREEN_HEIGHT))
        self.pre_stage_1b_bg = load_image("data/images/entities/stage_1_2_bg.png", (GC.SCREEN_WIDTH, GC.SCREEN_HEIGHT)) 
        self.pacman_bg = load_image("data/images/entities/labirin.jpg", (GC.SCREEN_WIDTH, GC.SCREEN_HEIGHT))

        self.dialog_box_img = load_image("data/images/entities/Dialog-Box.png", (int(GC.SCREEN_WIDTH * 0.9), 175))
        
        char_bimas_img = load_image("data/images/entities/DIALOGBIMAS.png")
        char_king_img = load_image("data/images/entities/DIALOGKING.png")
        scale_factor = 0.9
        self.bimas_scaled_img = None
        self.king_scaled_img = None
        if char_bimas_img: 
            char_bimas_size = (int(char_bimas_img.get_width() * scale_factor), int(char_bimas_img.get_height() * scale_factor))
            self.bimas_scaled_img = pygame.transform.scale(char_bimas_img, char_bimas_size)
        if char_king_img:
            char_king_size = (int(char_king_img.get_width() * scale_factor), int(char_king_img.get_height() * scale_factor))
            self.king_scaled_img = pygame.transform.scale(char_king_img, char_king_size)

        self.player_right_anim_scaled = []
        self.player_left_anim_scaled = []
        self.npc1_img_scaled = None
        try:
            self.player_right_anim_scaled = [pygame.transform.scale(load_image(f"data/images/entities/Bimas Kanan/{i}.png"),(50,80)) for i in range(1,5)]
            self.player_left_anim_scaled = [pygame.transform.scale(load_image(f"data/images/entities/Bimas Kiri/{i}.png"),(50,80)) for i in range(1,5)]
            self.npc1_img_scaled = pygame.transform.scale(load_image("data/images/entities/npc1.png"), (60,90))
        except Exception as e_asset:
            print(f"Error loading common player/npc assets in Game.__init__: {e_asset}")

        self.current_left_char_img = None
        self.current_right_char_img = None
        self.dialogues = GAME_DIALOGUES
        self.current_dialog_list = []
        self.current_dialog_index = -1

        self.buttons = get_game_buttons(self) 

        try:
            self.background_music_path = "data/audio/bg_sound.mp3"
            pygame.mixer.music.load(self.background_music_path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)
        except pygame.error as e:
            print(f"Tidak bisa memuat atau memainkan musik latar: {e}")

    def quit_game(self):
        print("Quitting game...")
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            delta_time = self.clock.tick(GC.FPS)
            self.handle_events() 
            self.update_main_logic(delta_time)
            
            # Draw hanya jika state dikelola Game class utama ATAU jika transisi sedang aktif
            # (agar transisi bisa fade out dari scene yang dikelola Game class)
            if self.state not in [GC.STATE_PRE_STAGE_1A, GC.STATE_PRE_STAGE_1B, GC.STATE_STAGE_1, 
                                  GC.STATE_AFT_STAGE_1B, GC.STATE_AWAN, GC.STATE_STAGE_2, 
                                  GC.STATE_DESA_2, GC.STATE_FINAL] or self.transition.is_active():
                self.draw() 
                pygame.display.flip()
            # Jika state memiliki loop sendiri, run_..._scene() akan menangani flip().

    def setup_main_menu(self): setup_main_menu(self)
    def setup_prologue(self): setup_prologue(self)
    def setup_pre_stage_1a(self): setup_pre_stage_1a(self)
    def setup_pre_stage_1b(self): setup_pre_stage_1b(self)
    def setup_stage_1_pacman(self): setup_stage_1_pacman(self)
    def setup_aft_stage_1b(self): setup_aft_stage_1b(self)
    def setup_state_awan(self): setup_state_awan(self)
    def setup_stage_2(self): setup_stage_2(self)
    def setup_desa_2(self): setup_desa_2(self)
    def setup_final_stage(self): setup_final_stage(self)
    
    def get_current_dialogues(self, state_key=None):
        if state_key is None: state_key = self.state
        return self.dialogues.get(state_key, [])

    def show_next_dialog(self):
        dialog_list = self.current_dialog_list
        if not dialog_list:
            self.subtitle.reset() 
            return False # Tidak ada dialog

        if self.current_dialog_index < len(dialog_list) - 1:
            self.current_dialog_index += 1
            dialog_text = dialog_list[self.current_dialog_index]
            self.subtitle.show(dialog_text)
            print(f"DEBUG: Menampilkan dialog {self.current_dialog_index + 1}/{len(dialog_list)}: {dialog_text[:30]}...")
            return True # Dialog baru ditampilkan
        else:
            print(f"DEBUG: Sudah di akhir dialog list untuk state {self.state}.")
            return False 

    def handle_events(self):
    
        if self.state not in [GC.STATE_PRE_STAGE_1A, GC.STATE_PRE_STAGE_1B, GC.STATE_STAGE_1, 
                              GC.STATE_AFT_STAGE_1B, GC.STATE_AWAN, GC.STATE_STAGE_2, 
                              GC.STATE_DESA_2, GC.STATE_FINAL]:
            # Untuk state yang dikelola loop utama Game (Main Menu, Prolog, Game Over)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.quit_game()
                    return 

                active_buttons = self.buttons.get(self.state, [])
                # PENTING: Tombol diproses dulu, karena aksi tombol mungkin mengubah state atau dialog
                for btn in active_buttons:
                    if btn.handle_event(event): # Jika tombol memicu aksi, kita anggap event sudah ditangani
                        return # Keluar dari handle_events agar tidak ada pemrosesan ganda

                # Jika tidak ada tombol yang di-handle dan state adalah Game Over (contoh untuk dialog tanpa tombol Next khusus)
                if self.state == GC.STATE_GAME_OVER:
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                            if self.subtitle.is_animating():
                                self.subtitle.fast_forward()
                            elif not self.subtitle.is_finished(): # Jika ada dialog lagi di list
                                self.show_next_dialog()
                            # else: # Dialog Game Over selesai, transisi biasanya dari tombol


    def update_main_logic(self, delta_time):
        next_state_from_transition = self.transition.update(delta_time) 
        
        if next_state_from_transition and next_state_from_transition != self.state:
            print(f"Transisi SELESAI. Mengubah state dari {self.state} ke {next_state_from_transition}")
            self.state = next_state_from_transition 
            
            if self.state == GC.STATE_MAIN_MENU: self.setup_main_menu()
            elif self.state == GC.STATE_STAGE_PROLOG: self.setup_prologue()
            elif self.state == GC.STATE_PRE_STAGE_1A: self.setup_pre_stage_1a()
            elif self.state == GC.STATE_PRE_STAGE_1B: self.setup_pre_stage_1b()
            elif self.state == GC.STATE_STAGE_1: self.setup_stage_1_pacman()
            elif self.state == GC.STATE_AFT_STAGE_1B: self.setup_aft_stage_1b()
            elif self.state == GC.STATE_AWAN: self.setup_state_awan()
            elif self.state == GC.STATE_STAGE_2: self.setup_stage_2()
            elif self.state == GC.STATE_DESA_2: self.setup_desa_2()
            elif self.state == GC.STATE_FINAL: self.setup_final_stage()
            # elif self.state == GC.STATE_GAME_OVER: self.setup_game_over() 
            
            print(f"DEBUG Game Update: Selesai memanggil setup untuk state {self.state}")
            return 

        if not self.transition.is_active() and self.state in [GC.STATE_MAIN_MENU, GC.STATE_STAGE_PROLOG, GC.STATE_GAME_OVER]:
             self.subtitle.update()


    def draw(self):
        if self.state not in [GC.STATE_PRE_STAGE_1A, GC.STATE_PRE_STAGE_1B, GC.STATE_STAGE_1, 
                              GC.STATE_AFT_STAGE_1B, GC.STATE_AWAN, GC.STATE_STAGE_2, 
                              GC.STATE_DESA_2, GC.STATE_FINAL] or self.transition.is_active():
            
            self.screen.fill((0, 0, 0)) 
            if self.state == GC.STATE_MAIN_MENU:
                if self.menu_bg: self.screen.blit(self.menu_bg, (0, 0))
            elif self.state == GC.STATE_STAGE_PROLOG:
                if self.prolog_bg: self.screen.blit(self.prolog_bg, (0, 0))
            elif self.state == GC.STATE_GAME_OVER: # Contoh
                 if hasattr(self, 'game_over_bg') and self.game_over_bg:
                     self.screen.blit(self.game_over_bg, (0,0))
                 else: self.screen.fill((30,0,0)) # Latar merah tua jika tidak ada bg khusus
            
            if self.state in [GC.STATE_STAGE_PROLOG, GC.STATE_GAME_OVER]: 
                self._draw_dialogue_ui()

            if self.state in [GC.STATE_MAIN_MENU, GC.STATE_STAGE_PROLOG, GC.STATE_GAME_OVER]: 
                active_buttons = self.buttons.get(self.state, [])
                for btn in active_buttons:
                     btn.draw(self.screen)

                if self.subtitle.is_showing():
                    self.subtitle.draw()

        if self.transition.is_active():
            self.transition.draw(self.screen)


    def _draw_dialogue_ui(self):
        if not self.dialog_box_img: return 

        dialog_rect = self.dialog_box_img.get_rect(midbottom=(GC.SCREEN_WIDTH // 2, GC.SCREEN_HEIGHT - 30)) 
        char_horizontal_inset = 80 
        char_bottom_offset = -45 

        if self.current_left_char_img:
            char_left_rect = self.current_left_char_img.get_rect(bottomleft=(dialog_rect.left + char_horizontal_inset, dialog_rect.bottom + char_bottom_offset))
            self.screen.blit(self.current_left_char_img, char_left_rect)
        
        if self.current_right_char_img:
            char_right_rect = self.current_right_char_img.get_rect(bottomright=(dialog_rect.right - char_horizontal_inset, dialog_rect.bottom + char_bottom_offset))
            self.screen.blit(self.current_right_char_img, char_right_rect)
        
        self.screen.blit(self.dialog_box_img, dialog_rect)

