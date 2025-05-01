# Impor library yang dibutuhkan
import pygame  # Library utama untuk membuat game
import sys     # Library untuk berinteraksi dengan sistem (misalnya, keluar dari program)

# --- Kelas untuk Membuat Tombol Interaktif ---
class Button:
    # Konstanta warna teks untuk tombol (putih)
    TEXT_COLOR = (255, 255, 255)

    # Fungsi yang dijalankan saat objek Button dibuat (konstruktor)
    def __init__(self, text, x, y, width, height, color, hover_color, font, action=None):
        """
        Inisialisasi tombol.

        Args:
            text (str): Teks yang ditampilkan di tombol.
            x (int): Posisi horizontal (koordinat x) pojok kiri atas tombol.
            y (int): Posisi vertikal (koordinat y) pojok kiri atas tombol.
            width (int): Lebar tombol.
            height (int): Tinggi tombol.
            color (tuple): Warna tombol dalam keadaan normal (R, G, B).
            hover_color (tuple): Warna tombol saat kursor mouse di atasnya (R, G, B).
            font (pygame.font.Font): Objek font untuk teks tombol.
            action (function, optional): Fungsi yang akan dipanggil saat tombol diklik. Defaults to None.
        """
        # Membuat area persegi untuk mendeteksi klik dan menggambar tombol
        self.rect = pygame.Rect(x, y, width, height)
        # Menyimpan warna-warna tombol
        self.color = color
        self.hover_color = hover_color
        # Menyimpan teks dan font
        self.text = text
        self.font = font
        # Menyimpan fungsi yang akan dijalankan saat diklik
        self.action = action
        # Status apakah mouse sedang berada di atas tombol
        self.is_hovered = False
        # Membuat permukaan (surface) untuk teks tombol
        self.text_surf = self.font.render(self.text, True, self.TEXT_COLOR)
        # Mendapatkan area persegi untuk teks dan menempatkannya di tengah tombol
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    # Fungsi untuk menggambar tombol ke layar
    def draw(self, surface):
        """
        Menggambar tombol ke permukaan (layar) yang diberikan.

        Args:
            surface (pygame.Surface): Permukaan tempat tombol akan digambar.
        """
        # Pilih warna berdasarkan status hover
        current_color = self.hover_color if self.is_hovered else self.color
        # Gambar persegi panjang tombol dengan sudut membulat
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        # Gambar teks di atas tombol
        surface.blit(self.text_surf, self.text_rect)

    # Fungsi untuk menangani event (interaksi pengguna)
    def handle_event(self, event):
        """
        Memproses event yang terkait dengan tombol (gerakan mouse, klik).

        Args:
            event (pygame.event.Event): Event yang sedang diproses.

        Returns:
            bool: True jika tombol diklik dan memiliki action, False jika tidak.
        """
        # Jika event adalah gerakan mouse
        if event.type == pygame.MOUSEMOTION:
            # Cek apakah posisi mouse berada di dalam area tombol
            self.is_hovered = self.rect.collidepoint(event.pos)
        # Jika event adalah klik tombol mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Cek apakah mouse sedang di atas tombol dan tombol kiri (1) yang diklik
            if self.is_hovered and event.button == 1:
                # Jika tombol ini punya fungsi action
                if self.action:
                    # Jalankan fungsi action
                    self.action()
                    # Kembalikan True untuk menandakan tombol diklik
                    return True
        # Kembalikan False jika tombol tidak diklik atau tidak ada action
        return False

# --- Kelas Utama Permainan ---
class Game:
    # Konstanta Warna (format R, G, B)
    BG_COLOR = (255, 255, 255) # Warna latar belakang (putih)
    BLACK = (0, 0, 0)         # Hitam
    GRAY = (100, 100, 100)      # Abu-abu
    BUTTON_COLOR = (50, 50, 50) # Warna tombol normal
    BUTTON_HOVER_COLOR = (70, 70, 70) # Warna tombol saat hover
    TITLE_COLOR = (10, 10, 50)  # Warna untuk judul game

    # Konstanta Ukuran Font
    FONT_SIZE_LARGE = 60
    FONT_SIZE_MEDIUM = 30
    FONT_SIZE_SMALL = 20

    # Konstanta Status Game
    STATE_MAIN_MENU = "main_menu" # Status saat di menu utama
    STATE_PLAYING = "playing"     # Status saat sedang bermain

    # Konstanta Kecepatan Pemain (pixel per frame)
    PLAYER_SPEED = 5

    # Fungsi yang dijalankan saat objek Game dibuat (konstruktor)
    def __init__(self):
        """
        Inisialisasi permainan, pygame, layar, aset, dan status awal.
        """
        # Inisialisasi semua modul pygame
        pygame.init()

        # Pengaturan ukuran layar
        self.screen_width = 1000
        self.screen_height = 600
        # Membuat jendela permainan
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # Mengatur judul jendela
        pygame.display.set_caption('Journey to Find a Leader')

        # Membuat objek Clock untuk mengatur frame rate
        self.clock = pygame.time.Clock()

        # Memuat font dan gambar
        self._load_fonts()
        self._load_images()

        # Mengatur status awal game ke menu utama
        self.game_state = self.STATE_MAIN_MENU

        # Menyiapkan posisi dan area (Rect) untuk gambar pemain
        # Jika gambar berhasil dimuat
        if self.img:
            img_width = self.img.get_width()
            img_height = self.img.get_height()
            # Hitung posisi awal agar di tengah layar (menggunakan list untuk posisi)
            self.img_pos = [self.screen_width // 2 - img_width // 2,
                            self.screen_height // 2 - img_height // 2]
            # Buat Rect untuk deteksi tabrakan dan penggambaran, berpusat di tengah layar
            self.img_rect = self.img.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        # Jika gambar gagal dimuat, gunakan placeholder
        else:
            # Posisi default untuk placeholder
            self.img_pos = [self.screen_width // 2 - 25, self.screen_height // 2 - 25]
            # Buat Rect default untuk placeholder
            self.img_rect = pygame.Rect(self.img_pos[0], self.img_pos[1], 50, 50)

        # Dictionary untuk melacak tombol gerakan yang sedang ditekan
        self.movement = {'up': False, 'down': False, 'left': False, 'right': False}

        # Membuat tombol-tombol untuk UI
        self._create_buttons()

    # Fungsi internal untuk memuat font
    def _load_fonts(self):
        """Memuat berbagai ukuran font yang akan digunakan."""
        # Menggunakan font default pygame (None) dengan ukuran berbeda
        self.large_font = pygame.font.Font(None, self.FONT_SIZE_LARGE)
        self.medium_font = pygame.font.Font(None, self.FONT_SIZE_MEDIUM)
        self.small_font = pygame.font.Font(None, self.FONT_SIZE_SMALL)
        # Font khusus untuk judul, sedikit lebih besar dari large_font
        self.title_font = pygame.font.Font(None, self.FONT_SIZE_LARGE + 10)

    # Fungsi internal untuk memuat gambar
    def _load_images(self):
        """Memuat gambar pemain dan latar belakang."""
        try:
            # Muat gambar pemain dari file
            image_path = "data/images/entities/bimas.png"
            loaded_image = pygame.image.load(image_path)
            # Konversi format gambar untuk performa lebih baik (dengan transparansi alpha)
            self.img = loaded_image.convert_alpha()
        except pygame.error as e:
            # Tangani jika file gambar pemain tidak ditemukan atau ada error lain
            print(f"Error loading player image: {e}")
            self.img = None # Set img ke None jika gagal dimuat

        try:
            # Muat gambar latar belakang
            bg_image_path = "data/images/entities/maps.png"
            loaded_bg_image = pygame.image.load(bg_image_path).convert() # Convert tanpa alpha untuk bg
            # Ubah ukuran gambar latar belakang agar sesuai dengan ukuran layar
            self.bg_image = pygame.transform.scale(loaded_bg_image, (self.screen_width, self.screen_height))
        except pygame.error as e:
            # Tangani jika file gambar latar belakang tidak ditemukan
            print(f"Error loading background image: {e}")
            self.bg_image = None # Set bg_image ke None jika gagal dimuat

    # Fungsi internal untuk membuat tombol UI
    def _create_buttons(self):
        """Membuat instance tombol untuk menu utama."""
        # Pengaturan dimensi dan jarak tombol
        btn_width = 200
        btn_height = 50
        btn_spacing = 20

        # Hitung posisi y awal agar tombol berada di tengah vertikal layar (sedikit ke bawah)
        total_btn_height = (btn_height * 2) + btn_spacing # Tinggi total 2 tombol + jarak
        start_y = (self.screen_height - total_btn_height) // 2 + 50
        # Hitung posisi x agar tombol berada di tengah horizontal layar
        btn_x = (self.screen_width - btn_width) // 2

        # Membuat tombol "Play Game"
        self.play_button = Button(
            text="Play Game",
            x=btn_x, y=start_y, # Posisi tombol pertama
            width=btn_width, height=btn_height,
            color=self.BUTTON_COLOR, hover_color=self.BUTTON_HOVER_COLOR,
            font=self.medium_font,
            action=self.start_game # Fungsi yang dijalankan saat diklik
        )
        # Membuat tombol "Exit"
        self.exitButton = Button(
            text="Exit",
            x=btn_x, y=start_y + btn_height + btn_spacing, # Posisi tombol kedua (di bawah tombol pertama)
            width=btn_width, height=btn_height,
            color=self.BUTTON_COLOR, hover_color=self.BUTTON_HOVER_COLOR,
            font=self.medium_font,
            action=self.quit_game # Fungsi yang dijalankan saat diklik
        )

        # Menyimpan tombol menu utama dalam list
        self.mainMenu_btn = [self.play_button, self.exitButton]
        # List untuk tombol dalam game (saat ini kosong)
        self.ingame_buttons = []

    # Fungsi untuk memulai permainan (dipanggil oleh tombol Play)
    def start_game(self):
        """Mengubah status game ke 'playing' dan mereset posisi pemain."""
        print("Starting game...")
        self.game_state = self.STATE_PLAYING # Ubah status

        # Reset posisi pemain ke tengah layar saat game dimulai
        if self.img:
             self.img_rect.center = (self.screen_width // 2, self.screen_height // 2)
        else:
             # Reset posisi placeholder jika gambar tidak ada
             self.img_rect.center = (self.screen_width // 2, self.screen_height // 2)

        # Reset status gerakan pemain
        self.movement = {'up': False, 'down': False, 'left': False, 'right': False}

    # Fungsi untuk keluar dari permainan (dipanggil oleh tombol Exit atau menutup jendela)
    def quit_game(self):
        """Menghentikan pygame dan menutup aplikasi."""
        print("Exiting game..")
        pygame.quit() # Hentikan semua modul pygame
        sys.exit()   # Keluar dari program Python

    # Fungsi internal untuk menangani semua input pengguna
    def _handle_events(self):
        """Memproses semua event dari pengguna (keyboard, mouse, dll.)."""
        # Loop melalui semua event yang terjadi sejak pemanggilan terakhir
        for event in pygame.event.get():
            # Jika event adalah menutup jendela (klik tombol X)
            if event.type == pygame.QUIT:
                self.quit_game() # Panggil fungsi keluar

            # Penanganan event berdasarkan status game
            if self.game_state == self.STATE_MAIN_MENU:
                # Jika di menu utama, teruskan event ke setiap tombol menu
                for button in self.mainMenu_btn:
                    button.handle_event(event)
            elif self.game_state == self.STATE_PLAYING:
                # Jika sedang bermain, tangani input keyboard untuk gerakan
                if event.type == pygame.KEYDOWN: # Tombol ditekan
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.movement['up'] = True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.movement['down'] = True
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.movement['left'] = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.movement['right'] = True
                elif event.type == pygame.KEYUP: # Tombol dilepas
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.movement['up'] = False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.movement['down'] = False
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.movement['left'] = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.movement['right'] = False

    # Fungsi internal untuk memperbarui logika game
    def _update(self):
        """Memperbarui status game, seperti posisi pemain."""
        # Hanya update logika pemain jika status game adalah 'playing'
        if self.game_state == self.STATE_PLAYING:
            # Variabel untuk menyimpan perubahan posisi di frame ini
            posisi_x = 0
            posisi_y = 0
            # Hitung perubahan posisi berdasarkan tombol yang ditekan
            if self.movement['up']:
                posisi_y -= self.PLAYER_SPEED
            if self.movement['down']:
                posisi_y += self.PLAYER_SPEED
            if self.movement['left']:
                posisi_x -= self.PLAYER_SPEED
            if self.movement['right']:
                posisi_x += self.PLAYER_SPEED

            # Terapkan perubahan posisi ke Rect pemain
            self.img_rect.x += posisi_x
            self.img_rect.y += posisi_y

            # --- Batasi Gerakan Pemain Agar Tetap di Dalam Layar ---
            # Cek batas kiri
            if self.img_rect.left < 0:
                self.img_rect.left = 0
            # Cek batas kanan
            if self.img_rect.right > self.screen_width:
                self.img_rect.right = self.screen_width
            # Cek batas atas
            if self.img_rect.top < 0:
                self.img_rect.top = 0
            # Cek batas bawah
            if self.img_rect.bottom > self.screen_height:
                self.img_rect.bottom = self.screen_height

    # Fungsi internal untuk menggambar semua elemen ke layar
    def _draw(self):
        """Menggambar semua elemen visual game ke layar."""
        # Gambar latar belakang terlebih dahulu
        if self.bg_image:
            # Jika gambar latar belakang ada, gambar ke layar di posisi (0,0)
            self.screen.blit(self.bg_image, (0, 0))
        else:
            # Jika tidak ada gambar latar belakang, isi layar dengan warna BG_COLOR
            self.screen.fill(self.BG_COLOR)

        # Gambar elemen berdasarkan status game
        if self.game_state == self.STATE_MAIN_MENU:
            # --- Gambar Elemen Menu Utama ---
            # Buat permukaan teks untuk judul
            title_surf = self.title_font.render('Journey to Find a Leader', True, self.TITLE_COLOR)
            # Dapatkan Rect untuk judul dan posisikan di tengah atas layar
            title_rect = title_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
            # Gambar judul ke layar
            self.screen.blit(title_surf, title_rect)

            # Gambar setiap tombol di menu utama
            for button in self.mainMenu_btn:
                button.draw(self.screen)

        elif self.game_state == self.STATE_PLAYING:
            # --- Gambar Elemen Saat Bermain ---
            # Gambar pemain jika gambar ada
            if self.img:
                self.screen.blit(self.img, self.img_rect)
            # Jika gambar pemain tidak ada, gambar placeholder (persegi abu-abu)
            else:
                pygame.draw.rect(self.screen, self.GRAY, self.img_rect)

        # Perbarui seluruh tampilan layar untuk menampilkan apa yang baru digambar
        pygame.display.flip()

    # Fungsi utama untuk menjalankan game loop
    def run(self):
        """Memulai dan menjalankan loop utama permainan."""
        # Loop tak terbatas yang menjaga game tetap berjalan
        while True:
            # 1. Tangani Input Pengguna
            self._handle_events()
            # 2. Perbarui Logika Game
            self._update()
            # 3. Gambar Ulang Tampilan
            self._draw()
            # 4. Atur Frame Rate (misal: 60 FPS)
            self.clock.tick(60)

# --- Titik Masuk Program ---
# Blok ini hanya akan dijalankan jika script ini dijalankan secara langsung
if __name__ == '__main__':
    # Buat objek dari kelas Game
    game = Game()
    # Panggil metode run() untuk memulai game
    game.run()