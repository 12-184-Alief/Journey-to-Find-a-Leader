# Impor modul
import pygame
import sys

# Impor modul kustom (tombol, aset, transisi, player, subtitle)
from buttons import Button
from assets import load_image
from transition import Transition
from entities import Player
from subtitle import Subtitle

# Kelas utama Game
class Game:
    # Konstruktor: Inisialisasi game
    def __init__(self):
        # Inisialisasi Pygame
        pygame.init()

        # --- Pengaturan Layar ---
        # Dimensi layar
        self.screen_width = 1920
        self.screen_height = 1080
        # Buat layar/jendela
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # Judul jendela
        pygame.display.set_caption('Journey to Find a Leader')
        # Rect layar (untuk posisi)
        self.screen_rect = self.screen.get_rect()
        # Kontrol frame rate (Clock)
        self.clock = pygame.time.Clock()

        # --- Status Game & Sistem ---
        # Status game awal ('main_menu')
        self.state = "main_menu"
        # Efek transisi layar
        self.transition = Transition(1000) # Durasi ms
        # Sistem subtitle
        self.subtitle = Subtitle(self.screen)
        # Margin bawah kotak dialog
        # self.dialog_bottom_margin = 60

        # --- Pemuatan Aset ---
        # Muat font
        self.font = pygame.font.Font("data/fonts/dogicapixelbold.otf", 30)
        # Muat gambar background
        self.menu_bg = load_image("data/images/entities/HomePage.png", self.screen.get_size())
        self.playing_bg = load_image("data/images/entities/Prolog-Background-Dialog.png", self.screen.get_size())
        # Inisialisasi pemain
        self.player = Player(load_image("data/images/entities/DIALOGBIMAS.png"), self.screen_rect.center)
        # Muat gambar kotak dialog
        self.dialog = load_image("data/images/entities/Dialog-Box.png", self.screen.get_size())

        # --- Data Dialog Prolog ---
        # Daftar dialog prolog
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
        # Indeks dialog saat ini (-1 agar mulai dari 0 saat ditekan)
        self.current_dialog_index = -1

        # --- Gambar Karakter Dialog ---
        # Muat gambar raja (opsional)
        self.king = load_image("data/images/entities/DIALOGKING.png", self.screen.get_size())
        # Path gambar karakter dialog
        char_left = "data/images/entities/DIALOGBIMAS.png"
        char_right = "data/images/entities/DIALOGKING.png"
        # Muat gambar karakter
        self.character_left_img = load_image(char_left)
        self.character_right_img = load_image(char_right)

        # --- Penskalaan Gambar Karakter ---
        # Faktor skala karakter
        scale_factor = 0.9
        # Hitung ukuran baru
        char_left_size = (int(self.character_left_img.get_width() * scale_factor), int(self.character_left_img.get_height() * scale_factor))
        char_right_size = (int(self.character_right_img.get_width() * scale_factor), int(self.character_right_img.get_height() * scale_factor))
        # Skalakan gambar karakter
        self.character_left_img = pygame.transform.scale(self.character_left_img, char_left_size)
        self.character_right_img = pygame.transform.scale(self.character_right_img, char_right_size)

        # --- Pengaturan Tombol ---
        # Ukuran & jarak tombol
        BUTTON_WIDTH = 300
        BUTTON_HEIGHT = 60
        BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)
        BUTTON_SIZE_NEXT = (200, 60) # Ukuran tombol 'Next'
        BUTTON_GAP = 30 # Jarak vertikal

        # Muat gambar tombol (normal/hover)
        button_img_play = load_image("data/images/entities/play.png")
        button_img_exit = load_image("data/images/entities/back.png")
        button_img_next = load_image("data/images/entities/next.png")
        btn_img_playHov = load_image("data/images/entities/playhov.png")
        btn_img_exitHov = load_image("data/images/entities/exithov.png")
        btn_img_nextHov = load_image("data/images/entities/nexthov.png")

        # Skalakan gambar tombol
        IMG_PLAY_NORMAL = pygame.transform.scale(button_img_play, BUTTON_SIZE)
        IMG_EXIT_NORMAL = pygame.transform.scale(button_img_exit, BUTTON_SIZE)
        IMG_NEXT_NORMAL = pygame.transform.scale(button_img_next, BUTTON_SIZE_NEXT)
        IMG_PLAY_HOVER = pygame.transform.scale(btn_img_playHov, BUTTON_SIZE)
        IMG_EXIT_HOVER = pygame.transform.scale(btn_img_exitHov, BUTTON_SIZE)
        IMG_NEXT_HOVER = pygame.transform.scale(btn_img_nextHov, BUTTON_SIZE_NEXT)

        # --- Perhitungan Posisi Tombol ---
        # Pusat layar (x, y)
        center_x = self.screen_rect.centerx
        center_y = self.screen_rect.centery

        # Posisi X tombol menu (tengah horizontal)
        button_x_topleft = center_x - (BUTTON_WIDTH // 2)

        # Tinggi total blok tombol menu
        total_button_block_height = (BUTTON_HEIGHT * 2) + BUTTON_GAP

        # Posisi Y dasar tombol menu (tengah vertikal)
        base_play_y = center_y - (total_button_block_height // 2)

        # --- Offset Vertikal Tombol Menu ---
        # Jumlah offset ke bawah
        vertical_offset = 125 # Piksel

        # Terapkan offset ke Y 'Play'
        play_y = base_play_y + vertical_offset

        # Hitung Y 'Exit' berdasarkan 'Play' + jarak
        exit_y = play_y + BUTTON_HEIGHT + BUTTON_GAP

        # --- Posisi Tombol 'Next' (Prolog, dll) ---
        # Margin tepi layar
        margin = 20
        # Atur posisi Y 'Next' (dekat atas)
        next_y = margin
        # Atur posisi X 'Next' (dekat kanan)
        next_x_topleft = self.screen_width - margin - BUTTON_SIZE_NEXT[0] # Gunakan lebar 'Next'

        # --- Kamus Tombol per Status ---
        # Simpan objek Button, dikelompokkan berdasarkan status game
        self.buttons = {
            "main_menu": [
                # Tombol Play -> mulai transisi
                Button(
                    image_normal=IMG_PLAY_NORMAL, image_hover=IMG_PLAY_HOVER,
                    x=button_x_topleft, y=play_y,
                    action=self.start_transition # Fungsi saat diklik
                ),
                # Tombol Exit -> keluar game
                Button(
                    image_normal=IMG_EXIT_NORMAL, image_hover=IMG_EXIT_HOVER,
                    x=button_x_topleft, y=exit_y,
                    action=self.quit_game # Fungsi saat diklik
                ),
            ],
            "stage_prolog": [
                # Tombol Next (prolog)
                Button(
                    image_normal=IMG_NEXT_NORMAL, image_hover=IMG_NEXT_HOVER,
                    x=next_x_topleft, y=next_y,
                    action=self.start_transition # TODO: Ganti aksi jika perlu
                )
            ],
            "stage_1.1": [
                # Tombol Next (stage 1.1)
                Button(
                    image_normal=IMG_NEXT_NORMAL, image_hover=IMG_NEXT_HOVER,
                    x=next_x_topleft, y=next_y,
                    action=self.start_transition # TODO: Ganti aksi jika perlu
                )
            ]
            # Tambahkan status & tombol lain di sini
        }

    # Mulai transisi layar ke status tertentu
    def start_transition(self):
        # Mulai fade out ke status 'stage_prolog'
        self.transition.start("stage_prolog")

    # Keluar dari game
    def quit_game(self):
        # Tutup Pygame
        pygame.quit()
        # Hentikan skrip
        sys.exit()

    # Loop game utama
    def run(self):
        while True:
            # Delta time (FPS), batasi FPS
            FPS = self.clock.tick(60)
            # Tangani event (input)
            self.handle_events()
            # Perbarui logika game
            self.update(FPS)
            # Gambar ke layar
            self.draw()

    # Setup saat masuk status prolog
    def setup_prologue(self):
        """(Dipanggil sekali saat ganti status ke prolog)"""
        # Reset subtitle
        self.subtitle.reset()
        # Reset indeks dialog ke awal
        self.current_dialog_index = 0
        # Jika ada dialog prolog
        if self.prologue_dialogues:
            # Tampilkan dialog pertama
            self.subtitle.show(self.prologue_dialogues[self.current_dialog_index])
        else:
            # Jika tidak ada dialog
            self.current_dialog_index = -1 # Hindari error
            print("Peringatan: Dialog prolog kosong.")
            # Pertimbangkan transisi otomatis jika perlu

    # Tangani input & event
    def handle_events(self):
        # Loop semua event
        for event in pygame.event.get():
            # Cek event QUIT (klik tombol close)
            if event.type == pygame.QUIT:
                self.quit_game()

            # --- Penanganan Event per Status ---
            # Beda penanganan per status game
            if self.state == "main_menu":
                # Kirim event ke tombol status ini ('main_menu')
                for btn in self.buttons.get(self.state, []):
                    btn.handle_event(event)

            elif self.state == "stage_prolog":
                # Kirim event ke tombol status ini ('stage_prolog')
                for btn in self.buttons.get(self.state, []):
                     btn.handle_event(event)

                # --- Progresi Dialog (Prolog) ---
                # Jika tombol ditekan
                if event.type == pygame.KEYDOWN:
                    # Jika Spasi/Enter
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        # Jika masih ada dialog berikutnya
                        if 0 <= self.current_dialog_index < len(self.prologue_dialogues) - 1:
                            # Maju ke dialog berikutnya
                            self.current_dialog_index += 1
                            # Tampilkan dialog berikutnya
                            self.subtitle.show(self.prologue_dialogues[self.current_dialog_index])
                        # Jika dialog terakhir sudah tampil
                        elif self.current_dialog_index >= len(self.prologue_dialogues) - 1:
                            # Dialog selesai
                            print("Dialog prolog selesai.")
                            # (Tunggu aksi lain, atau otomatis lanjut)
                            pass

            elif self.state == "stage1.1":
                # Event stage 1.1
                # Kirim event ke tombol stage 1.1
                 for btn in self.buttons.get(self.state, []):
                     btn.handle_event(event)
            pass # Tambahkan logika event stage 1.1

            # Tambahkan penanganan status lain (elif self.state == ...)

    # Perbarui logika game (per frame)
    def update(self, FPS):
        # --- Penanganan Transisi ---
        # Update transisi, cek apakah ada status baru
        next_state = self.transition.update(FPS)
        # Tandai jika status berubah frame ini
        state_changed = False
        # Jika ada status baru dari transisi
        if next_state:
            print(f"Status berubah dari {self.state} menjadi {next_state}") # Debug
            # Ganti status game
            self.state = next_state
            # Tandai status sudah berubah
            state_changed = True

            # --- Setup SEKALI Saat Ganti Status ---
            # (Hanya dijalankan 1x saat status baru aktif)
            if self.state == "stage_prolog":
                # Panggil setup prolog
                self.setup_prologue()
            elif self.state == "stage1.1":
                # Reset subtitle stage 1.1
                self.subtitle.reset()
                # Contoh teks awal stage 1.1
                self.subtitle.show("Memulai stage 1.1...") # Ganti teks
                # Tambah setup stage 1.1
            # Tambah setup status lain (elif self.state == ...)

        # --- Pembaruan Berkelanjutan per Status ---
        # (Dijalankan setiap frame)
        if self.state == "main_menu":
            # Update elemen menu (jika ada animasi dll)
            pass
        elif self.state == "stage_prolog":
            # Update pemain (jika bergerak saat dialog)
            self.player.update(self.screen.get_size())
            # Update subtitle (animasi teks, timing, dll)
            self.subtitle.update()
        elif self.state == "stage1.1":
            # Update elemen stage 1.1
            # Update subtitle (jika ada teks)
            self.subtitle.update()
            # Update pemain/entitas lain
            # self.player.update(...)

    # Gambar semua elemen ke layar
    def draw(self):
        # --- Penggambaran per Status ---
        # Gambar elemen sesuai status game
        if self.state == "main_menu":
            # Gambar background menu
            self.screen.blit(self.menu_bg, (0, 0))
            # Gambar tombol menu
            for btn in self.buttons.get(self.state, []):
                btn.draw(self.screen)

        elif self.state == "stage_prolog":
            # Gambar background prolog
            self.screen.blit(self.playing_bg, (0, 0))

            # --- Render Kotak Dialog ---
            # Ukuran kotak dialog (lebar 90% layar, tinggi tetap)
            dialog_width = self.screen_width * 0.9
            dialog_height = 175
            # Skalakan gambar dialog
            overlay_resized = pygame.transform.scale(self.dialog, (int(dialog_width), int(dialog_height)))

            # Dapatkan rect & atur posisi dialog
            dialog_rect = overlay_resized.get_rect(midbottom=(self.screen_width // 2, self.screen_height - 50)) # Sedikit naik dari bawah

            # --- Posisi Sprite Karakter ---
            # Jarak karakter dari tepi horizontal dialog
            char_horizontal_inset = 70
            # Tumpang tindih vertikal karakter & dialog (negatif = ke atas)
            char_bottom_offset = -60

            # 1. Gambar Karakter Kiri (jika ada)
            if self.character_left_img:
                # Rect karakter kiri
                char_left_rect = self.character_left_img.get_rect()
                # Atur X karakter kiri (kiri dialog + inset)
                char_left_rect.left = dialog_rect.left + char_horizontal_inset
                # Atur Y karakter kiri (bawah dialog + offset)
                char_left_rect.bottom = dialog_rect.bottom + char_bottom_offset
                # Gambar karakter kiri
                self.screen.blit(self.character_left_img, char_left_rect)

            # 2. Gambar Karakter Kanan (jika ada)
            if self.character_right_img:
                # Rect karakter kanan
                char_right_rect = self.character_right_img.get_rect()
                # Atur X karakter kanan (kanan dialog - inset)
                char_right_rect.right = dialog_rect.right - char_horizontal_inset
                # Atur Y karakter kanan (sama dg kiri)
                char_right_rect.bottom = dialog_rect.bottom + char_bottom_offset
                # Gambar karakter kanan
                self.screen.blit(self.character_right_img, char_right_rect)

            # 3. Gambar Kotak Dialog (di atas karakter)
            self.screen.blit(overlay_resized, dialog_rect)

            # 4. Gambar Tombol Prolog (misal 'Next')
            for btn in self.buttons.get(self.state, []):
                btn.draw(self.screen)

        # --- Elemen Gambar Umum ---
        # Gambar subtitle (jika ada teks aktif)
        self.subtitle.draw()
        # Gambar efek transisi (jika aktif)
        self.transition.draw(self.screen)

        # Tampilkan frame baru ke layar
        pygame.display.flip()

# --- Awal mulai program ---
# (Hanya jika skrip dijalankan langsung)
if __name__ == "__main__":
    # Buat objek Game
    game = Game()
    # Jalankan game (mulai loop utama)
    game.run()