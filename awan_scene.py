# awan_scene.py
import pygame
import sys
from constants import GameConstants as GC # Impor GC untuk konsistensi jika diperlukan
from utils import load_image # Gunakan utilitas load_image jika memungkinkan

# Fungsi ini akan dipanggil dari game_states.py
def run_awan_scene(game_instance):
    screen = game_instance.screen # Gunakan screen dari game_instance
    # Ukuran layar sudah di-set oleh game_instance
    # SCREEN_WIDTH = GC.SCREEN_WIDTH
    # SCREEN_HEIGHT = GC.SCREEN_HEIGHT
    # pygame.display.set_caption("Scene Clue - Awan") # Caption sudah di-set oleh Game

    # Font dan warna
    try:
        font = pygame.font.Font("data/fonts/dogicapixelbold.otf", 24) # Ukuran font bisa disesuaikan
    except pygame.error as e:
        print(f"Gagal memuat font di awan_scene: {e}. Menggunakan font default.")
        font = pygame.font.Font(None, 28) # Fallback font
    text_color = (255, 255, 255)

    # Background
    # Bisa menggunakan background yang sudah dimuat di game_instance jika ada
    # atau muat di sini secara spesifik
    background = load_image("data/images/entities/awan.png", (GC.SCREEN_WIDTH, GC.SCREEN_HEIGHT))
    if background is None: # Fallback jika gambar gagal dimuat
        background = pygame.Surface((GC.SCREEN_WIDTH, GC.SCREEN_HEIGHT))
        background.fill((100, 100, 120)) # Warna abu-abu kebiruan untuk awan

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
    start_y = GC.SCREEN_HEIGHT // 2 - (len(story_lines) * 40) // 2 # Posisi Y awal teks (tengah)
    line_spacing = 45     # Jarak antar baris
    text_align = "center"

    clock = pygame.time.Clock() # Gunakan clock dari game_instance jika perlu, atau clock lokal
    running = True

    while running:
        screen.blit(background, (0, 0))

        y = start_y
        for line in story_lines:
            text_surface = font.render(line, True, text_color)
            text_rect = text_surface.get_rect()

            if text_align == "center":
                text_rect.centerx = GC.SCREEN_WIDTH // 2
            elif text_align == "left":
                text_rect.x = 100
            elif text_align == "right":
                text_rect.right = GC.SCREEN_WIDTH - 100

            text_rect.y = y
            screen.blit(text_surface, text_rect)
            y += line_spacing

        pygame.display.flip() # Penting untuk update tampilan

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_instance.quit_game() # Gunakan metode quit_game dari game_instance
                return # Keluar dari fungsi
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False # Hentikan loop scene awan
                    # Transisi ke state berikutnya (Spot Difference Game)
                    print("Scene Awan selesai, lanjut ke Spot Difference (STATE_STAGE_2)")
                    game_instance.transition.start(GC.STATE_STAGE_2) # Transisi ke state berikutnya
                    return # Keluar dari fungsi setelah memulai transisi

        clock.tick(60) # Batasi FPS