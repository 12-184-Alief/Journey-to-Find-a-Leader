import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Blocking with Background")

# Memuat font khusus untuk menampilkan teks di layar
font = pygame.font.Font("data/fonts/dogicapixelbold.otf", 21)

# Load gambar dialog box (tanpa potret)
DIALOG_WIDTH = 1500  # misalnya selebar 1400px
DIALOG_HEIGHT = 150  # misalnya setinggi 200px
dialog_box_img = pygame.image.load("data/images/entities/Dialog-Box.png").convert_alpha()
dialog_box_img = pygame.transform.scale(dialog_box_img, (DIALOG_WIDTH, DIALOG_HEIGHT))
# Warna
# WHITE = (255, 255, 255)
# BLUE = (0, 0, 255)
# DARK_GRAY = (50, 50, 50)

# Load gambar background
background_image = pygame.image.load("data/images/entities/pacman_vilage.png").convert()

# Load sprite animasi ke dalam list
player_right = [
    pygame.image.load("data/images/entities/Bimas Kanan/1.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kanan/2.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kanan/3.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kanan/4.png").convert_alpha()
]
player_left = [
    pygame.image.load("data/images/entities/Bimas Kiri/1.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kiri/2.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kiri/3.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kiri/4.png").convert_alpha()
]

# Load gambar NPC
npc1_image = pygame.image.load("data/images/entities/npc1.png").convert_alpha()

# FPS
clock = pygame.time.Clock()
FPS = 60

# Objek player
player_w = 50
player_h = 80
player = pygame.Rect(0, 495, player_w, player_h)

# Kecepatan pemain
player_speed = 5

facing_right = True  # Arah gerak saat ini
frame_index = 0      # Index frame animasi
frame_timer = 0      # Pengatur kecepatan animasi

# Objek dinding
wall1 = pygame.Rect(0, 0, 1022, 456)
wall2 = pygame.Rect(1267, 0, 653, 413)
wall3 = pygame.Rect(1022, 0, 245, 380)
wall4 = pygame.Rect(0, 661, 1002, 423)
wall5 = pygame.Rect(1256, 661, 664, 419)
wall6 = pygame.Rect(1000, 1080, 250, 100)
wall7 = pygame.Rect(1920, 430, 100, 230)

# Status penyelesaian trigger zone
zone1_done = False
zone2_done = False
zone3_done = False

# Sistem dialog zona 1
dialog_active = False
dialog_index = 0

# Format dialog: "Speaker: Kalimat"
dialog_list = [
    "Kepala Desa: Kamu kesatria utusan raja, ya?",
    "Kesatria: Benar. Ada apa dengan desa ini?",
    "Kepala Desa: Kami dilanda wabah, banyak warga sakit.",
    "Kesatria: Apa penyebabnya?",
    "Kepala Desa: Diduga ulah penyihir jahat.",
    "Kesatria: Apa yang bisa kubantu?",
    "Kepala Desa: Ada ramuan penyembuh, tapi bahan utamanya ada di hutan.",
    "Kepala Desa: Jalannya berbahaya, banyak makhluk buas dan bawahan penyihir.",
    "Kesatria: Aku akan mencarinya. Arahkan aku ke sana.",
    "Kepala Desa: Dari rumah saya, lurus ke arah hutan.",
    "Kepala Desa: Hati-hati. Banyak nyawa bergantung padamu."
]

# Membuat area trigger untuk transisi map, posisi dan ukuran ditentukan
trigger_zone1 = pygame.Rect(1065, 296, 150, 100)
# Membuat area trigger untuk transisi map, posisi dan ukuran ditentukan
trigger_zone2 = pygame.Rect(1000, 1000, 250, 100)
# Membuat area trigger untuk transisi map, posisi dan ukuran ditentukan
trigger_zone3 = pygame.Rect(1810, 430, 100, 230)

# Posisi tetap NPC di dekat masing-masing trigger zone
npc1_pos = (trigger_zone1.x + 60, trigger_zone1.y)  # dekat trigger_zone1

# Game loop
running = True
while running:
    # Gambar background ke layar
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Jika user menekan tombol
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if dialog_active:
                    dialog_index += 1
                    if dialog_index >= len(dialog_list):
                        dialog_active = False
                        zone1_done = True  # Dialog selesai, aktifkan zona berikutnya
                elif in_trigger1 and not zone1_done:
                    dialog_active = True
                    dialog_index = 0
                elif in_trigger2 and zone1_done and not zone2_done:
                    print("Trigger Zone 2 selesai: Masuk labirin")
                    zone2_done = True
                elif in_trigger3 and zone2_done and not zone3_done:
                    print("Trigger Zone 3 selesai: Next map")
                    zone3_done = True

    # Simpan posisi lama
    old_position = player.copy()

    # Kontrol pemain hanya jika dialog tidak aktif
    keys = pygame.key.get_pressed()
    moving = False
    if not dialog_active:
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
            facing_right = False
            moving = True
        if keys[pygame.K_RIGHT]:
            player.x += player_speed
            facing_right = True
            moving = True
        if keys[pygame.K_UP]:
            player.y -= player_speed
            moving = True
        if keys[pygame.K_DOWN]:
            player.y += player_speed
            moving = True


    # Cek tabrakan
    if player.colliderect(wall1):
        player = old_position
    elif player.colliderect(wall2):
        player = old_position
    elif player.colliderect(wall3):
        player = old_position
    elif player.colliderect(wall4):
        player = old_position
    elif player.colliderect(wall5):
        player = old_position
    elif player.colliderect(wall6):
        player = old_position
    elif player.colliderect(wall7):
        player = old_position

    # Mengecek apakah player berada di dalam area trigger
    in_trigger1 = player.colliderect(trigger_zone1)
    # Mengecek apakah player berada di dalam area trigger
    in_trigger2 = player.colliderect(trigger_zone2)
    # Mengecek apakah player berada di dalam area trigger
    in_trigger3 = player.colliderect(trigger_zone3)

    # Update animasi hanya jika bergerak
    if moving:
        frame_timer += 1
        if frame_timer >= 10:  # Setiap 10 frame
            frame_index = (frame_index + 1) % len(player_right)
            frame_timer = 0
    else:
        frame_index = 0  # Diam, gunakan frame pertama

    # Pilih sprite berdasarkan arah
    if facing_right:
        sprite = player_right[frame_index]
    else:
        sprite = player_left[frame_index]

    # Gambar NPC ke layar
    screen.blit(npc1_image, npc1_pos)
    # Gambar pemain ke layar
    screen.blit(sprite, player)

    

    # Gambar objek
    # pygame.draw.rect(screen, BLUE, player)
    # pygame.draw.rect(screen, DARK_GRAY, wall1)
    # pygame.draw.rect(screen, DARK_GRAY, wall2)
    # pygame.draw.rect(screen, DARK_GRAY, wall3)
    # pygame.draw.rect(screen, DARK_GRAY, wall4)
    # pygame.draw.rect(screen, DARK_GRAY, wall5)

    # Jika berada di area trigger DAN zona tersebut boleh diakses
    if in_trigger1 and not zone1_done:
        text = font.render("Tekan ENTER untuk dialog", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))
    elif in_trigger2 and zone1_done and not zone2_done:
        text = font.render("Tekan ENTER untuk masuk labirin", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))
    elif in_trigger3 and zone2_done and not zone3_done:
        text = font.render("Tekan ENTER untuk next map", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))

    if zone1_done and zone2_done and zone3_done:
        done_text = font.render("Semua trigger selesai!", True, (255, 255, 0))
        screen.blit(done_text, (WIDTH // 2 - done_text.get_width() // 2, 50))

    # Tampilkan dialog jika aktif
    if dialog_active and dialog_index < len(dialog_list):
        # Hitung posisi supaya dialog box berada di tengah horizontal dan di bawah layar
        dialog_x = (WIDTH - DIALOG_WIDTH) // 2
        dialog_y = 800
        # Gambar kotak dialog
        screen.blit(dialog_box_img, (dialog_x, dialog_y))  # Sesuaikan posisi jika perlu
        # Gambar teks dialog
        dialog_text = font.render(dialog_list[dialog_index], True, (0, 0, 0))
        screen.blit(dialog_text, (dialog_x + 50, dialog_y + 50))  # sesuaikan padding jika perlu


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
