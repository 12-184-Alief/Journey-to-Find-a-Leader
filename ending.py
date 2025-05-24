import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dialog Scene")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ======== PENGATURAN POSISI DAN UKURAN MANUAL ========
char1_config = {
    "name": "Bimas",
    "image": "data/images/entities/DIALOGBIMAS.png",
    "dim_image": "data/images/entities/Bimas Hover.png",
    "size": (512, 520),
    "pos": (190, 460)
}

char2_config = {
    "name": "Penyihir",
    "image": "data/images/entities/PENYIHIR.png",
    "dim_image": "data/images/entities/PENYIHIR-HOVER.png",
    "size": (462, 470),
    "pos": (1200, 470)
}

chat_box_config = {
    "image": "data/images/entities/Dialog-Box.png",
    "size": (1600, 210),
    "pos": (160, 820)
}

# ======================================================

# Load background
background = pygame.image.load("data/images/entities/awan.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load dan skalakan karakter
def load_character(config):
    char = pygame.image.load(config["image"]).convert_alpha()
    char_dim = pygame.image.load(config["dim_image"]).convert_alpha()
    char = pygame.transform.scale(char, config["size"])
    char_dim = pygame.transform.scale(char_dim, config["size"])
    return char, char_dim

character1, character1_dim = load_character(char1_config)
character2, character2_dim = load_character(char2_config)

# Load dan skalakan chat frame
chat_frame = pygame.image.load(chat_box_config["image"]).convert_alpha()
chat_frame = pygame.transform.scale(chat_frame, chat_box_config["size"])

# Font lebih kecil
font = pygame.font.Font("data/fonts/dogicapixelbold.otf", 24)

# Dialog (masih pakai tuple tapi tanpa ditampilkan nama)
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

# Timer
last_click_time = pygame.time.get_ticks()
clock = pygame.time.Clock()

# Loop utama
running = True
while running:
    dt = clock.tick(60)
    screen.blit(background, (0, 0))

    # Ambil data dialog
    if dialog_index < len(dialogues):
        speaker, text = dialogues[dialog_index]
    else:
        speaker = None
        text = ""

    # Gambar karakter dengan sorotan
    if speaker == char1_config["name"]:
        screen.blit(character1, char1_config["pos"])
        screen.blit(character2_dim, char2_config["pos"])
    elif speaker == char2_config["name"]:
        screen.blit(character1_dim, char1_config["pos"])
        screen.blit(character2, char2_config["pos"])
    else:
        screen.blit(character1_dim, char1_config["pos"])
        screen.blit(character2_dim, char2_config["pos"])

    # Chat frame
    chat_x, chat_y = chat_box_config["pos"]
    screen.blit(chat_frame, (chat_x, chat_y))

    # Tampilkan teks dialog tanpa nama
    if dialog_index < len(dialogues):
        text_surf = font.render(text, True, BLACK)
        screen.blit(text_surf, (chat_x + 40, chat_y + 60))
    else:
        end_surf = font.render("Dialog selesai. Tekan ESC untuk keluar.", True, BLACK)
        screen.blit(end_surf, (chat_x + 40, chat_y + 80))

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            now = pygame.time.get_ticks()
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and now - last_click_time > dialog_delay:
                if dialog_index < len(dialogues):
                    dialog_index += 1
                    last_click_time = now

    pygame.display.flip()

pygame.quit()
sys.exit()
