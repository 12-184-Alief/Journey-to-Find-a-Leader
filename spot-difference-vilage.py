# Import modul pygame dan sys untuk membuat game dan mengakses fungsi sistem
import pygame
import sys

# Inisialisasi semua modul pygame yang diperlukan
pygame.init()

# Menentukan ukuran layar permainan
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Membuat jendela permainan
pygame.display.set_caption("Collision Blocking with Background")  # Judul jendela game

# Memuat font khusus untuk menampilkan teks di layar
font = pygame.font.Font("data/fonts/dogicapixelbold.otf", 21)

# Memuat gambar dialog box (tanpa potret karakter)
DIALOG_WIDTH = 1500
DIALOG_HEIGHT = 150
dialog_box_img = pygame.image.load("data/images/entities/Dialog-Box.png").convert_alpha()
dialog_box_img = pygame.transform.scale(dialog_box_img, (DIALOG_WIDTH, DIALOG_HEIGHT))

# Memuat gambar background utama
background_image = pygame.image.load("data/images/entities/spotdifference_vilage.png").convert()

# Memuat animasi gerakan ke kanan pemain
player_right = [
    pygame.image.load("data/images/entities/Bimas Kanan/1.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kanan/2.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kanan/3.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kanan/4.png").convert_alpha()
]

# Memuat animasi gerakan ke kiri pemain
player_left = [
    pygame.image.load("data/images/entities/Bimas Kiri/1.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kiri/2.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kiri/3.png").convert_alpha(),
    pygame.image.load("data/images/entities/Bimas Kiri/4.png").convert_alpha()
]

# Memuat gambar NPC
npc1_image = pygame.image.load("data/images/entities/npc2.png").convert_alpha()

# Pengatur waktu FPS
clock = pygame.time.Clock()
FPS = 60  # Frame per detik

# Membuat objek pemain menggunakan pygame.Rect (x, y, width, height)
player_w = 50
player_h = 80
player = pygame.Rect(0, 375, player_w, player_h)

# Kecepatan gerakan pemain
player_speed = 5

# Variabel status arah gerakan pemain dan animasi
facing_right = True
frame_index = 0
frame_timer = 0

# Membuat dinding-dinding sebagai batas yang tidak bisa dilewati
wall1 = pygame.Rect(0, 0, 1920, 365)
wall2 = pygame.Rect(1514, 365, 406, 724)
wall3 = pygame.Rect(0, 486, 1255, 372)
wall4 = pygame.Rect(0, 858, 1084, 225)
wall5 = pygame.Rect(1424, 930, 100, 300)
wall6 = pygame.Rect(1080, 1080, 400, 100)
wall7 = pygame.Rect(1460, 510, 50, 80)

# Menandai apakah dialog trigger di zona 1 sudah selesai
zone1_done = False

# Status dan kontrol dialog
dialog_active = False
dialog_index = 0

# Daftar dialog, format: "Nama: Kalimat"
dialog_list = [
    "Kepala Desa: Kesatria! Kau berhasil... awan tebal itu telah sirna.",
    "Kesatria: Apa warga sudah bisa keluar desa?",
    "Kepala Desa: Ya. Kami bisa melihat langit lagi. Udara pun terasa segar.",
    "Kesatria: Awan itu... pasti ulah penyihir itu, bukan?",
    "Kepala Desa: Benar. Ia ingin memutus kami dari dunia luar.",
    "Kesatria: Sekarang semua sudah aman.",
    "Kepala Desa: Terima kasih, kau telah menyelamatkan kami.",
    "Kesatria: Senang bisa membantu.",
    "Kepala Desa: Kami akan selalu mengenang jasamu.",
    "Kesatria: Di mana penyihir itu sekarang?"
]

# Membuat area trigger zona 1 (ketika pemain masuk area ini, dialog akan dimulai)
trigger_zone1 = pygame.Rect(1400, 510, 100, 100)

# Menentukan posisi NPC agar terlihat di dekat zona trigger
npc1_pos = (trigger_zone1.x + 60, trigger_zone1.y)

# Mulai game loop
running = True
while running:
    # Menggambar background
    screen.blit(background_image, (0, 0))

    # Menangani event pada game (input dari keyboard atau penutupan jendela)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Keluar dari loop utama saat jendela ditutup
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if dialog_active:
                    dialog_index += 1
                    if dialog_index >= len(dialog_list):  # Selesai semua dialog
                        dialog_active = False
                        zone1_done = True
                elif in_trigger1 and not zone1_done:
                    dialog_active = True
                    dialog_index = 0  # Mulai dialog dari awal

    # Simpan posisi lama sebelum bergerak (untuk rollback jika tabrakan)
    old_position = player.copy()

    # Cek tombol yang ditekan dan gerakkan pemain
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

    # Cek tabrakan dengan dinding, jika tabrakan, kembalikan ke posisi lama
    if player.colliderect(wall1): player = old_position
    elif player.colliderect(wall2): player = old_position
    elif player.colliderect(wall3): player = old_position
    elif player.colliderect(wall4): player = old_position
    elif player.colliderect(wall5): player = old_position
    elif player.colliderect(wall6): player = old_position
    elif player.colliderect(wall7): player = old_position

    # Cek apakah pemain berada di zona trigger
    in_trigger1 = player.colliderect(trigger_zone1)

    # Update animasi jika pemain bergerak
    if moving:
        frame_timer += 1
        if frame_timer >= 10:  # Ganti frame setiap 10 frame
            frame_index = (frame_index + 1) % len(player_right)
            frame_timer = 0
    else:
        frame_index = 0  # Jika diam, gunakan frame pertama

    # Pilih sprite sesuai arah
    sprite = player_right[frame_index] if facing_right else player_left[frame_index]

    # Gambar NPC di layar
    screen.blit(npc1_image, npc1_pos)

    # Gambar pemain di layar
    screen.blit(sprite, player)

    # Tampilkan instruksi jika pemain berada di zona trigger dan belum selesai
    if in_trigger1 and not zone1_done:
        text = font.render("Tekan ENTER untuk dialog", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))

    # Tampilkan notifikasi jika semua trigger telah selesai
    if zone1_done:
        done_text = font.render("Semua trigger selesai!", True, (255, 255, 0))
        screen.blit(done_text, (WIDTH // 2 - done_text.get_width() // 2, 50))

    # Tampilkan kotak dan teks dialog jika dialog aktif
    if dialog_active and dialog_index < len(dialog_list):
        dialog_x = (WIDTH - DIALOG_WIDTH) // 2
        dialog_y = 800
        screen.blit(dialog_box_img, (dialog_x, dialog_y))  # Tampilkan kotak dialog
        dialog_text = font.render(dialog_list[dialog_index], True, (0, 0, 0))
        screen.blit(dialog_text, (dialog_x + 50, dialog_y + 50))  # Tampilkan teks dialog

    # Perbarui layar
    pygame.display.flip()

    # Jaga agar permainan berjalan sesuai kecepatan FPS
    clock.tick(FPS)

# Keluar dari pygame dan program
pygame.quit()
sys.exit()
