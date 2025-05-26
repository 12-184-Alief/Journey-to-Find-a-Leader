# ending_scene.py
import pygame
import sys
from constants import GameConstants as GC
from utils import load_image

def run_ending_scene(game_instance):
    screen = game_instance.screen
    WIDTH, HEIGHT = screen.get_size()
    FPS = 60 

    char1_config = {
        "name": "Bimas", "image": "data/images/entities/DIALOGBIMAS.png",
        "dim_image": "data/images/entities/Bimas Hover.png", "size": (512, 520), "pos": (190, 460)
    }
    char2_config = {
        "name": "Penyihir", "image": "data/images/entities/PENYIHIR.png",
        "dim_image": "data/images/entities/PENYIHIR-HOVER.png", "size": (462, 470), "pos": (1200, 470)
    }
    chat_box_config = {
        "image": "data/images/entities/Dialog-Box.png", "size": (1600, 210), "pos": (160, 820)
    }

    background = load_image("data/images/entities/awan.png", (WIDTH, HEIGHT))

    def load_character_assets(config):
        char = load_image(config["image"])
        char_dim = load_image(config["dim_image"])
        if char and config.get("size"): char = pygame.transform.scale(char, config["size"])
        if char_dim and config.get("size"): char_dim = pygame.transform.scale(char_dim, config["size"])
        return char, char_dim

    character1, character1_dim = load_character_assets(char1_config)
    character2, character2_dim = load_character_assets(char2_config)
    chat_frame = load_image(chat_box_config["image"], chat_box_config["size"])

    font = pygame.font.Font("data/fonts/dogicapixelbold.otf", 24)

    dialogues = [
        ("Bimas", "Akhirnya kau muncul juga..."),
        ("Penyihir", "*tertawa* Heh... lama sekali kau sampai ke sini, ksatria."),
        ("Bimas", "Apa maksudmu membuat kekacauan di dua desa itu?!"),
        ("Penyihir", "Maksudku? Hah! Kau pikir aku akan membocorkan rencanaku padamu?"),
        ("Bimas", "Kau menyebabkan penderitaan! Banyak yang kehilangan rumah, bahkan nyawa!"),
        ("Penyihir", "Lemah. Mereka pantas mendapatkannya. Dunia ini butuh sedikit guncangan."),
        ("Bimas", "Kau pengecut, menyerang yang tak bersalah. Kau tak lebih dari monster!"),
        ("Penyihir", "Hati-hati dengan kata-katamu, ksatria. Aku belum serius barusan."),
        ("Penyihir", "Anggap saja ini... pemanasan."),
        ("Bimas", "Kalau begitu selesaikan di sini dan sekarang!"),
        ("Penyihir", "Oh tidak, belum saatnya. Tapi..."),
        ("Penyihir", "*tersenyum sinis* Aku akan kembali... dan saat itu, kau tak akan mampu menghentikanku."),
        ("Penyihir", "*tertawa keras* Hahahahaha!"),
        ("Bimas", "Tunggu! Jangan lari, dasar pengecut!"),
        ("Narasi", "Penyihir itu menghilang ke dalam bayangan... meninggalkan aroma sihir gelap di udara."),
        ("Narasi", "Bimas menggenggam erat pedangnya. Pertarungan mereka... baru saja dimulai."),
    ]

    dialog_index = 0
    dialog_delay = 300  # ms
    last_click_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(FPS)
        screen.blit(background, (0, 0))

        speaker, text = None, ""
        if dialog_index < len(dialogues):
            speaker, text = dialogues[dialog_index]
        
        # Draw characters
        if character1 and character1_dim and character2 and character2_dim: # Check if images loaded
            if speaker == char1_config["name"]:
                screen.blit(character1, char1_config["pos"])
                screen.blit(character2_dim, char2_config["pos"])
            elif speaker == char2_config["name"]:
                screen.blit(character1_dim, char1_config["pos"])
                screen.blit(character2, char2_config["pos"])
            else: 
                screen.blit(character1_dim, char1_config["pos"])
                screen.blit(character2_dim, char2_config["pos"])
        
        if chat_frame: screen.blit(chat_frame, chat_box_config["pos"])

        if dialog_index < len(dialogues):
            text_surf = font.render(text, True, (0, 0, 0))
            text_pos_x = chat_box_config["pos"][0] + 40
            text_pos_y = chat_box_config["pos"][1] + 60 # Adjusted for typical dialog box padding
            screen.blit(text_surf, (text_pos_x, text_pos_y))
        else:
            end_surf = font.render("Tekan SPACE untuk melanjutkan...", True, (0,0,0)) # Changed message
            screen.blit(end_surf, (chat_box_config["pos"][0] + 40, chat_box_config["pos"][1] + 80))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_instance.quit_game() # Proper exit
                return 
            elif event.type == pygame.KEYDOWN:
                now = pygame.time.get_ticks()
                if event.key == pygame.K_ESCAPE:
                    running = False
                    game_instance.transition.start(GC.STATE_MAIN_MENU) 
                    return
                elif event.key == pygame.K_SPACE and now - last_click_time > dialog_delay:
                    if dialog_index < len(dialogues):
                        dialog_index += 1
                        last_click_time = now
                    else: 
                        running = False
                        # Transition to Game Over (which can then show a "You Win" message)
                        game_instance.game_over_message = "Selamat! Kau telah menyelesaikan petualangan!"
                        game_instance.transition.start(GC.STATE_MAIN_MENU)
                        return
        pygame.display.flip()