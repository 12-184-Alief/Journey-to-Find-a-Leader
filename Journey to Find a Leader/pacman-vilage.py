# Import modul pygame untuk membuat game dan sys untuk keluar dari program
import pygame
import sys

# Inisialisasi semua modul pygame
pygame.init()

# Menentukan ukuran layar game
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Membuat jendela tampilan
pygame.display.set_caption("Collision Blocking with Background")  # Judul jendela

# Memuat font dari file eksternal untuk menampilkan teks
font = pygame.font.Font("data/fonts/dogicapixelbold.otf", 21)

# Load dan skala gambar kotak dialog
DIALOG_WIDTH = 1500
DIALOG_HEIGHT = 150
dialog_box_img = pygame.image.load("data/images/entities/Dialog-Box.png").convert_alpha()
dialog_box_img = pygame.transform.scale(dialog_box_img, (DIALOG_WIDTH, DIALOG_HEIGHT))

# Load gambar background dari file
background_image = pygame.image.load("data/images/entities/pacman_vilage.png").convert()

# Load animasi gerakan ke kanan dan kiri dalam bentuk list gambar (frame animasi)
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

# Load sprite NPC
npc1_image = pygame.image.load("data/images/entities/npc1.png").convert_alpha()

# Membuat objek clock untuk mengatur FPS
clock = pygame.time.Clock()
FPS = 60  # Frame per second

# Membuat objek pemain dalam bentuk Rect (x, y, lebar, tinggi)
player_w = 50
player_h = 80
player = pygame.Rect(0, 495, player_w, player_h)

# Kecepatan gerak pemain
player_speed = 5

# Variabel arah dan animasi
facing_right = True  # Mengatur arah default menghadap kanan
frame_index = 0      # Index frame animasi yang sedang digunakan
frame_timer = 0      # Timer untuk mengatur kecepatan pergantian frame

# Membuat beberapa dinding sebagai area yang tidak bisa dilewati
wall1 = pygame.Rect(0, 0, 1022, 456)
wall2 = pygame.Rect(1267, 0, 653, 413)
wall3 = pygame.Rect(1022, 0, 245, 380)
wall4 = pygame.Rect(0, 661, 1002, 423)
wall5 = pygame.Rect(1256, 661, 664, 419)
wall6 = pygame.Rect(1000, 1080, 250, 100)
wall7 = pygame.Rect(1920, 430, 100, 230)

# Menyimpan status penyelesaian dari setiap zona/trigger
zone1_done = False
zone2_done = False
zone3_done = False

# Variabel kontrol dialog zona 1
dialog_active = False  # Apakah dialog sedang aktif
dialog_index = 0       # Indeks baris dialog yang sedang ditampilkan

# Daftar dialog sebagai list string
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

# Membuat area trigger (zona interaktif)
trigger_zone1 = pygame.Rect(1065, 296, 150, 100)
trigger_zone2 = pygame.Rect(1000, 1000, 250, 100)
trigger_zone3 = pygame.Rect(1810, 430, 100, 230)

# Posisi NPC1 ditentukan berdasarkan trigger zone
npc1_pos = (trigger_zone1.x + 60, trigger_zone1.y)

# Game loop utama
running = True
while running:
    # Gambar background ke layar
    screen.blit(background_image, (0, 0))

    # Event handler (menangani input dan keluar program)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Keluar game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Menekan enter saat dialog aktif
                if dialog_active:
                    dialog_index += 1
                    # Jika sudah melewati semua dialog, nonaktifkan dialog
                    if dialog_index >= len(dialog_list):
                        dialog_active = False
                        zone1_done = True
                # Aktifkan dialog jika dalam trigger 1 dan belum selesai
                elif in_trigger1 and not zone1_done:
                    dialog_active = True
                    dialog_index = 0
                # Proses trigger kedua
                elif in_trigger2 and zone1_done and not zone2_done:
                    print("Trigger Zone 2 selesai: Masuk labirin")
                    zone2_done = True
                # Proses trigger ketiga
                elif in_trigger3 and zone2_done and not zone3_done:
                    print("Trigger Zone 3 selesai: Next map")
                    zone3_done = True

    # Simpan posisi lama untuk rollback jika tabrakan
    old_position = player.copy()

    # Kontrol pergerakan jika tidak sedang dialog
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

    # Cek tabrakan dengan semua dinding
    if player.colliderect(wall1) or player.colliderect(wall2) or player.colliderect(wall3) or \
       player.colliderect(wall4) or player.colliderect(wall5) or player.colliderect(wall6) or \
       player.colliderect(wall7):
        player = old_position  # Kembalikan ke posisi semula

    # Cek apakah pemain menyentuh trigger zone
    in_trigger1 = player.colliderect(trigger_zone1)
    in_trigger2 = player.colliderect(trigger_zone2)
    in_trigger3 = player.colliderect(trigger_zone3)

    # Update frame animasi jika bergerak
    if moving:
        frame_timer += 1
        if frame_timer >= 10:
            frame_index = (frame_index + 1) % len(player_right)
            frame_timer = 0
    else:
        frame_index = 0  # Diam, tampilkan frame pertama

    # Pilih sprite berdasarkan arah hadap
    sprite = player_right[frame_index] if facing_right else player_left[frame_index]

    # Gambar NPC
    screen.blit(npc1_image, npc1_pos)
    # Gambar pemain
    screen.blit(sprite, player)

    # Tampilkan teks aksi jika menyentuh trigger dan sesuai urutan zona
    if in_trigger1 and not zone1_done:
        text = font.render("Tekan ENTER untuk dialog", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))
    elif in_trigger2 and zone1_done and not zone2_done:
        text = font.render("Tekan ENTER untuk masuk labirin", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))
    elif in_trigger3 and zone2_done and not zone3_done:
        text = font.render("Tekan ENTER untuk next map", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))

    # Jika semua zona telah selesai
    if zone1_done and zone2_done and zone3_done:
        done_text = font.render("Semua trigger selesai!", True, (255, 255, 0))
        screen.blit(done_text, (WIDTH // 2 - done_text.get_width() // 2, 50))

    # Tampilkan dialog jika aktif
    if dialog_active and dialog_index < len(dialog_list):
        dialog_x = (WIDTH - DIALOG_WIDTH) // 2
        dialog_y = 800
        # Gambar kotak dialog
        screen.blit(dialog_box_img, (dialog_x, dialog_y))
        # Gambar teks dialog saat ini
        dialog_text = font.render(dialog_list[dialog_index], True, (0, 0, 0))
        screen.blit(dialog_text, (dialog_x + 50, dialog_y + 50))

    # Perbarui layar
    pygame.display.flip()
    clock.tick(FPS)

# Keluar dari game setelah loop selesai
pygame.quit()
sys.exit()