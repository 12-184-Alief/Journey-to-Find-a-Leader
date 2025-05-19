import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scene Clue - Spot the Difference")

# Font dan warna
font = pygame.font.Font("data/fonts/dogicapixelbold.otf", 18)
text_color = (255, 255, 255)

# Background
background = pygame.image.load("data/images/entities/awan.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cerita
story_lines = [
    "Di desa selanjutnya terdapat awan gelap tebal",
    "yang menutupi desa tersebut, membuatnya hilang dan tak bisa ditemukan.",
    "Orang-orang desa terkurung di dalamnya tanpa harapan.",
    "",
    "Untuk membuka jalan ke desa itu, sang kesatria harus",
    "menggunakan kekuatan magic dan ketelitiannya.",
    "Awan tebal tersebut dibuat oleh seorang penyihir gelap.",
    "",
    "Tekan [SPASI] untuk melanjutkan..."
]

# Pengaturan posisi teks
start_y = 300         # Posisi Y awal teks (bisa diubah)
line_spacing = 40     # Jarak antar baris
text_align = "center" # Pilihan: "center", "left", atau "right"

def draw_story():
    screen.blit(background, (0, 0))

    y = start_y
    for line in story_lines:
        text_surface = font.render(line, True, text_color)
        text_rect = text_surface.get_rect()

        if text_align == "center":
            text_rect.centerx = SCREEN_WIDTH // 2
        elif text_align == "left":
            text_rect.x = 100  # bisa diganti nilai margin kiri
        elif text_align == "right":
            text_rect.right = SCREEN_WIDTH - 100  # bisa diganti nilai margin kanan

        text_rect.y = y
        screen.blit(text_surface, text_rect)
        y += line_spacing

    pygame.display.flip()

def show_clue_scene():
    running = True
    while running:
        draw_story()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

# Jalankan scene clue
show_clue_scene()

print("Game dimulai... (lanjut ke spot the difference)")
