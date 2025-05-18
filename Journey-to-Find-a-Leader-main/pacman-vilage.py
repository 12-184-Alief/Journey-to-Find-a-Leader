import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Blocking with Background")

# Warna
# WHITE = (255, 255, 255)
# BLUE = (0, 0, 255)
DARK_GRAY = (50, 50, 50)

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
wall3 = pygame.Rect(1022, 0, 245, 247)
wall4 = pygame.Rect(0, 661, 1002, 423)
wall5 = pygame.Rect(1256, 661, 664, 419)

# Game loop
running = True
while running:
    # Gambar background ke layar
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Simpan posisi lama
    old_position = player.copy()

    # Kontrol pemain
    keys = pygame.key.get_pressed()
    moving = False
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

    # Gambar pemain ke layar
    screen.blit(sprite, player)

    # Gambar objek
    # pygame.draw.rect(screen, BLUE, player)
    # pygame.draw.rect(screen, DARK_GRAY, wall1)
    # pygame.draw.rect(screen, DARK_GRAY, wall2)
    # pygame.draw.rect(screen, DARK_GRAY, wall3)
    # pygame.draw.rect(screen, DARK_GRAY, wall4)
    # pygame.draw.rect(screen, DARK_GRAY, wall5)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
