import pygame
import sys

from buttons import Button
from assets import load_image
from transition import Transition
from entities import Player
from subtitle import Subtitle


class Game:
    BG_COLOR = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    BUTTON_COLOR = (50, 50, 50)
    BUTTON_HOVER_COLOR = (70, 70, 70)
    TITLE_COLOR = (10, 10, 50)

    FONT_SIZE_LARGE = 60
    FONT_SIZE_MEDIUM = 30
    FONT_SIZE_SMALL = 20

    STATE_MAIN_MENU = "main_menu"
    STATE_PLAYING = "playing"

    PLAYER_SPEED = 5

    def __init__(self):
        pygame.init()

        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Journey to Find a Leader')
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()

        self.state = "main_menu"
        self.transition = Transition(1000)
        self.subtitle = Subtitle(self.screen)

        self.font = pygame.font.Font("data/fonts/dogicapixelbold.otf", 30)

        self.menu_bg = load_image("data/images/entities/HomePage.png", self.screen.get_size())
        self.playing_bg = load_image("data/images/entities/Prolog-Background-Dialog.png", self.screen.get_size())
        self.player = Player(load_image("data/images/entities/DIALOGBIMAS.png"), self.screen_rect.center)
        self.dialog = load_image("data/images/entities/Dialog-Box.png", self.screen.get_size())

        self.prologue_dialogues = [
            "Aku bukan raja... hanya kesatria...",
            "Aku hanya seorang kesatria yang mencari apa arti kepemimpinan sejati.",
            "Tiga desa sedang dilanda bencana…",
            "Dan hanya dengan memahami mereka, aku bisa menyelamatkan negeri ini",
            "dan diriku sendiri.",
            "Angin hangat membawa kabar buruk ke istana... dari tiga penjuru negeri,",
            "desa-desa mengirim pesan yang sama: bencana telah datang.",
            "Raja Habbi,pemimpin kerajaan,memanggil kesatria kepercayaannya ke ruang singgasana.",
            "Di hadapan bentangan karpet merah yang panjang",
            "dan ruangan yang didominasi warna merah dan emas",
            "perintah agung pun disampaikan."
        ]
        self.current_dialog_index = -1

        self.king = load_image("data/images/entities/DIALOGKING.png", self.screen.get_size())
        char_left = "data/images/entities/DIALOGBIMAS.png"
        char_right = "data/images/entities/DIALOGKING.png"
        self.character_left_img = load_image(char_left)
        self.character_right_img = load_image(char_right)

        scale_factor = 0.9
        char_left_size = (int(self.character_left_img.get_width() * scale_factor), int(self.character_left_img.get_height() * scale_factor))
        char_right_size = (int(self.character_right_img.get_width() * scale_factor), int(self.character_right_img.get_height() * scale_factor))
        self.character_left_img = pygame.transform.scale(self.character_left_img, char_left_size)
        self.character_right_img = pygame.transform.scale(self.character_right_img, char_right_size)

        BUTTON_WIDTH = 300
        BUTTON_HEIGHT = 60
        BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)
        BUTTON_SIZE_NEXT = (200, 60)
        BUTTON_GAP = 30

        button_img_play = load_image("data/images/entities/play.png")
        button_img_exit = load_image("data/images/entities/exit.png")
        button_img_next = load_image("data/images/entities/next.png")
        btn_img_playHov = load_image("data/images/entities/playhov.png")
        btn_img_exitHov = load_image("data/images/entities/exithov.png")
        btn_img_nextHov = load_image("data/images/entities/nexthov.png")

        IMG_PLAY_NORMAL = pygame.transform.scale(button_img_play, BUTTON_SIZE)
        IMG_EXIT_NORMAL = pygame.transform.scale(button_img_exit, BUTTON_SIZE)
        IMG_NEXT_NORMAL = pygame.transform.scale(button_img_next, BUTTON_SIZE_NEXT)
        IMG_PLAY_HOVER = pygame.transform.scale(btn_img_playHov, BUTTON_SIZE)
        IMG_EXIT_HOVER = pygame.transform.scale(btn_img_exitHov, BUTTON_SIZE)
        IMG_NEXT_HOVER = pygame.transform.scale(btn_img_nextHov, BUTTON_SIZE_NEXT)

        center_x = self.screen_rect.centerx
        center_y = self.screen_rect.centery

        button_x_topleft = center_x - (BUTTON_WIDTH // 2)

        total_button_block_height = (BUTTON_HEIGHT * 2) + BUTTON_GAP

        base_play_y = center_y - (total_button_block_height // 2)

        vertical_offset = 125

        play_y = base_play_y + vertical_offset

        exit_y = play_y + BUTTON_HEIGHT + BUTTON_GAP

        margin = 20
        next_y = margin
        next_x_topleft = self.screen_width - margin - BUTTON_SIZE_NEXT[0]

        self.buttons = {
            "main_menu": [
                Button(
                    image_normal=IMG_PLAY_NORMAL, image_hover=IMG_PLAY_HOVER,
                    x=button_x_topleft, y=play_y,
                    action=self.start_transition
                ),
                Button(
                    image_normal=IMG_EXIT_NORMAL, image_hover=IMG_EXIT_HOVER,
                    x=button_x_topleft, y=exit_y,
                    action=self.quit_game
                ),
            ],
            "stage_prolog": [
                Button(
                    image_normal=IMG_NEXT_NORMAL, image_hover=IMG_NEXT_HOVER,
                    x=next_x_topleft, y=next_y,
                    action=self.start_transition
                )
            ],
            "stage_1.1": [
                Button(
                    image_normal=IMG_NEXT_NORMAL, image_hover=IMG_NEXT_HOVER,
                    x=next_x_topleft, y=next_y,
                    action=self.start_transition
                )
            ]
        }
        
        self.background_music_path = "data/audio/bg_sound.mp3"
        pygame.mixer.music.load(self.background_music_path)
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(3.0)
        

    def start_transition(self):
        self.transition.start("stage_prolog")

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            FPS = self.clock.tick(60)
            self.handle_events()
            self.update(FPS)
            self.draw()

    def setup_prologue(self):
        self.subtitle.reset()
        self.current_dialog_index = 0
        if self.prologue_dialogues:
            self.subtitle.show(self.prologue_dialogues[self.current_dialog_index])
        else:
            self.current_dialog_index = -1
            print("Warning: Prologue dialogues are empty.")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if self.state == "main_menu":
                for btn in self.buttons.get(self.state, []):
                    btn.handle_event(event)

            elif self.state == "stage_prolog":
                for btn in self.buttons.get(self.state, []):
                    btn.handle_event(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if 0 <= self.current_dialog_index < len(self.prologue_dialogues) - 1:
                            self.current_dialog_index += 1
                            self.subtitle.show(self.prologue_dialogues[self.current_dialog_index])
                        elif self.current_dialog_index >= len(self.prologue_dialogues) - 1:
                            print("Prolog dialogue finished.")
                            pass

            elif self.state == "stage1.1":
                for btn in self.buttons.get(self.state, []):
                    btn.handle_event(event)
                pass

    def update(self, FPS):
        next_state = self.transition.update(FPS)
        state_changed = False
        if next_state:
            print(f"Status changed from {self.state} to {next_state}")
            self.state = next_state
            state_changed = True

            if self.state == "stage_prolog":
                self.setup_prologue()
            elif self.state == "stage1.1":
                self.subtitle.reset()
                self.subtitle.show("Starting stage 1.1...")


        if self.state == "main_menu":
            pass
        elif self.state == "stage_prolog":
            self.player.update(self.screen.get_size())
            self.subtitle.update()
        elif self.state == "stage1.1":
            self.subtitle.update()


    def draw(self):
        if self.state == "main_menu":
            self.screen.blit(self.menu_bg, (0, 0))
            for btn in self.buttons.get(self.state, []):
                btn.draw(self.screen)

        elif self.state == "stage_prolog":
            self.screen.blit(self.playing_bg, (0, 0))

            dialog_width = self.screen_width * 0.9
            dialog_height = 175
            overlay_resized = pygame.transform.scale(self.dialog, (int(dialog_width), int(dialog_height)))

            dialog_rect = overlay_resized.get_rect(midbottom=(self.screen_width // 2, self.screen_height - 50))

            char_horizontal_inset = 70
            char_bottom_offset = -60

            if self.character_left_img:
                char_left_rect = self.character_left_img.get_rect()
                char_left_rect.left = dialog_rect.left + char_horizontal_inset
                char_left_rect.bottom = dialog_rect.bottom + char_bottom_offset
                self.screen.blit(self.character_left_img, char_left_rect)

            if self.character_right_img:
                char_right_rect = self.character_right_img.get_rect()
                char_right_rect.right = dialog_rect.right - char_horizontal_inset
                char_right_rect.bottom = dialog_rect.bottom + char_bottom_offset
                self.screen.blit(self.character_right_img, char_right_rect)

            self.screen.blit(overlay_resized, dialog_rect)

            for btn in self.buttons.get(self.state, []):
                btn.draw(self.screen)

        if self.subtitle.font:
             self.subtitle.draw()
        self.transition.draw(self.screen)

        pygame.display.flip()