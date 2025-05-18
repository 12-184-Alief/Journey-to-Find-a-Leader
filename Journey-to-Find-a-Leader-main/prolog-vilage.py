# Mengimpor modul pygame dan sys untuk membuat game dan keluar dari program
import pygame
import sys

# Inisialisasi semua modul di Pygame sebelum digunakan
pygame.init()

# Memuat font khusus untuk menampilkan teks di layar
font = pygame.font.Font("data/fonts/dogicapixelbold.otf", 21)

# Mendefinisikan ukuran layar game
WIDTH, HEIGHT = 1920, 1080
# Membuat jendela tampilan game dengan ukuran yang telah ditentukan
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Memberi judul pada jendela game
pygame.display.set_caption("Collision Blocking with Background")

# Memuat gambar background (latar belakang)
background_image = pygame.image.load("data/images/entities/overworld_tileset.png").convert()

# Memuat list gambar animasi player saat bergerak ke kanan
player_right = [
    pygame.image.load("data/images/entities/Bimas Kanan/1.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kanan/2.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kanan/3.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kanan/4.png").convert_alpha()
]

# Memuat list gambar animasi player saat bergerak ke kiri
player_left = [
    pygame.image.load("data/images/entities/Bimas Kiri/1.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kiri/2.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kiri/3.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kiri/4.png").convert_alpha()
]

# Mengatur kecepatan frame per detik (FPS)
clock = pygame.time.Clock()
FPS = 60

# Membuat objek Rect untuk player, menentukan posisi dan ukuran
player_w = 50
player_h = 80
player = pygame.Rect(0, 420, player_w, player_h)

# Kecepatan gerak player dalam piksel
player_speed = 5

# Menyimpan arah gerakan terakhir (untuk menentukan arah animasi)
facing_right = True
# Menyimpan indeks frame animasi yang sedang ditampilkan
frame_index = 0
# Timer untuk mengatur kecepatan animasi
frame_timer = 0

# Membuat batas atas menggunakan Rect (sebagai dinding)
wall1 = pygame.Rect(0, 0, 1920, 380)
# Membuat batas bawah menggunakan Rect (sebagai dinding)
wall2 = pygame.Rect(0, 520, 1920, 560)

# Membuat area trigger untuk transisi map, posisi dan ukuran ditentukan
trigger_zone = pygame.Rect(1800, 420, 100, 100)

# Memulai game loop utama
running = True
while running:
    # Menampilkan background di layar di posisi (0, 0)
    screen.blit(background_image, (0, 0))

    # Mengecek semua event yang terjadi (seperti menekan tombol, keluar game)
    for event in pygame.event.get():
        # Jika user menutup jendela, hentikan loop
        if event.type == pygame.QUIT:
            running = False
        # Jika user menekan tombol
        elif event.type == pygame.KEYDOWN:
            # Jika menekan ENTER dan sedang berada di area trigger
            if event.key == pygame.K_RETURN and in_trigger:
                print("Transisi ke map berikutnya!")  # Ganti sesuai transisi

    # Menyimpan posisi player sebelum digerakkan (untuk rollback jika nabrak)
    old_position = player.copy()

    # Mengecek tombol-tombol yang ditekan
    keys = pygame.key.get_pressed()
    moving = False  # Untuk mendeteksi apakah player sedang bergerak

    # Pergerakan ke kiri
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
        facing_right = False
        moving = True
    # Pergerakan ke kanan
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
        facing_right = True
        moving = True
    # Pergerakan ke atas
    if keys[pygame.K_UP]:
        player.y -= player_speed
        moving = True
    # Pergerakan ke bawah
    if keys[pygame.K_DOWN]:
        player.y += player_speed
        moving = True

    # Mengecek apakah player menabrak dinding atas, jika iya kembalikan posisi sebelumnya
    if player.colliderect(wall1):
        player = old_position
    # Mengecek apakah player menabrak dinding bawah
    elif player.colliderect(wall2):
        player = old_position

    # Mengecek apakah player berada di dalam area trigger
    in_trigger = player.colliderect(trigger_zone)

    # Update frame animasi jika player bergerak
    if moving:
        frame_timer += 1
        # Ganti frame setiap 10 tick
        if frame_timer >= 10:
            frame_index = (frame_index + 1) % len(player_right)
            frame_timer = 0
    else:
        # Jika diam, gunakan frame pertama
        frame_index = 0

    # Pilih sprite berdasarkan arah gerakan terakhir
    if facing_right:
        sprite = player_right[frame_index]
    else:
        sprite = player_left[frame_index]

    # Gambar sprite player di layar
    screen.blit(sprite, player)

    # Jika berada di area trigger, tampilkan perintah ENTER
    if in_trigger:
        text = font.render("Tekan ENTER untuk masuk", True, (255, 255, 255))
        # Letakkan teks di bagian bawah layar, tengah secara horizontal
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))

    # Memperbarui tampilan layar
    pygame.display.flip()
    # Menunda loop untuk menjaga FPS stabil
    clock.tick(FPS)

# Keluar dari Pygame dan program
pygame.quit()
sys.exit()
