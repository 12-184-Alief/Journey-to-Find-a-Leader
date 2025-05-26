# spot_difference_game.py
import pygame
import sys

# Impor GameConstants dari struktur game utama
from constants import GameConstants as GC
from utils import load_image # Untuk loading gambar secara konsisten

# --- Konfigurasi (Ambil dari GameConstants jika relevan) ---
FPS = 60

# --- Colors (Tidak Berubah) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (40, 120, 255)
RED = (220, 0, 0)
GREEN = (0, 160, 0)

# --- Fungsi Pembantu ---
def draw_text(screen, font, text, pos, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, pos)

# --- Main game loop untuk Stage 2 (Spot Difference) ---
def run_spot_difference_game(game_instance):
    screen = game_instance.screen
    WIDTH = GC.SCREEN_WIDTH
    HEIGHT = GC.SCREEN_HEIGHT

    # Inisialisasi asset khusus Spot Difference game di sini
    font_path = "data/fonts/dogicapixelbold.otf" # Usahakan gunakan font yang sama
    try:
        font_ui = pygame.font.Font(font_path, 28) # Ukuran font sedikit lebih kecil untuk UI
        font_message = pygame.font.Font(font_path, 40) # Font untuk pesan menang/kalah
    except pygame.error:
        print(f"Warning: Font {font_path} tidak ditemukan, menggunakan font sistem.")
        font_ui = pygame.font.SysFont(None, 32)
        font_message = pygame.font.SysFont(None, 48)


    frame = pygame.transform.scale(load_image('data/images/entities/2frame.jpg'), (WIDTH, HEIGHT))

    left_img = load_image("data/images/entities/Spot_difer.png")
    right_img = load_image("data/images/entities/spot_difer2.png")
    circle_img_orig = load_image("data/images/entities/Red_Circle.png")
    circle_img = pygame.transform.scale(circle_img_orig, (70,70))

    # Posisi gambar
    left_pos = (185, 100)
    right_pos = (1055, 100)

    # Area perbedaan relatif terhadap gambar kiri
    differences_data_initial = [
        pygame.Rect(450, 650, 100,100), #posisi batu di kolam
        pygame.Rect(5, 550, 100,100),  #posisi batu kiri
        pygame.Rect(400, 25, 100,100), #posisi awan
        pygame.Rect(190, 400, 100,100), #posisi pohon
        pygame.Rect(220, 620, 100,100), #posisi ekor rubah
        pygame.Rect(320, 800, 100,100), #posisi bayangan rubah
    ]
    
    # Variabel game state internal
    differences_to_find = [] # Akan diisi ulang saat reset
    found_differences = []
    max_guesses = 3
    max_hints = 3
    guesses_left = max_guesses
    hints_left = max_hints
    show_hint_visual = False
    game_over_state = False # Renamed from game_over to avoid conflict with a potential variable
    ask_retry_state = False # Renamed

    def reset_game_state_internal():
        nonlocal guesses_left, found_differences, game_over_state, ask_retry_state, hints_left, show_hint_visual, differences_to_find
        guesses_left = max_guesses
        hints_left = max_hints
        # Penting: Buat salinan baru dari differences_data_initial setiap kali reset
        differences_to_find = [rect.copy() for rect in differences_data_initial]
        found_differences = []
        game_over_state = False
        ask_retry_state = False
        show_hint_visual = False
        print("Spot the Difference game state reset.")

    reset_game_state_internal() # Panggil reset di awal untuk inisialisasi

    def check_click_action(pos):
        nonlocal guesses_left, found_differences 

        clicked_on_difference = False
        # Iterasi melalui salinan list agar aman jika memodifikasi `found_differences`
        for i, rect_diff in enumerate(differences_to_find):
            # Cek apakah perbedaan ini sudah ditemukan (dengan membandingkan objek Rect, bukan hanya indeks)
            # Ini penting jika urutan differences_to_find berubah atau jika kita menghapus dari list ini
            is_already_found = any(found_rect is rect_diff for found_rect in found_differences)
            if is_already_found:
                continue

            # Cek klik pada gambar kiri atau kanan
            if rect_diff.move(left_pos).collidepoint(pos) or rect_diff.move(right_pos).collidepoint(pos):
                print(f"Benar! Ditemukan perbedaan di: {rect_diff}")
                found_differences.append(rect_diff) # Tambahkan objek Rect yang asli
                clicked_on_difference = True
                # Anda bisa menambahkan suara "benar" di sini
                break # Hanya satu perbedaan per klik

        if not clicked_on_difference:
            print("Salah klik.")
            guesses_left -= 1
            # Anda bisa menambahkan suara "salah" di sini

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(frame, (0, 0)) # Gambar frame background utama

        # --- UI Atas: Ditemukan, Nyawa, Hint ---
        draw_text(screen, font_ui, f"{len(found_differences)}/{len(differences_data_initial)}", (WIDTH * 0.35, 30), GREEN) # Disesuaikan posisinya
        draw_text(screen, font_ui, f"Nyawa: {guesses_left}", (WIDTH * 0.5, 30), RED)
        draw_text(screen, font_ui, f"Hint: {hints_left}", (WIDTH * 0.65, 30), BLUE)


        # --- Gambar Kiri dan Kanan ---
        screen.blit(left_img, left_pos)
        screen.blit(right_img, right_pos)

        # --- Tampilkan perbedaan yang ditemukan ---
        for rect in found_differences:
            # Gambar lingkaran di kedua gambar untuk perbedaan yang ditemukan
            screen.blit(circle_img, (left_pos[0] + rect.x + (rect.width - circle_img.get_width()) // 2, 
                                     left_pos[1] + rect.y + (rect.height - circle_img.get_height()) // 2))
            screen.blit(circle_img, (right_pos[0] + rect.x + (rect.width - circle_img.get_width()) // 2, 
                                     right_pos[1] + rect.y + (rect.height - circle_img.get_height()) // 2))

        # --- Hint visual ---
        if show_hint_visual and hints_left > 0:
            hint_found_for_display = False
            for rect in differences_to_find: # Iterasi dari data asli
                is_already_found = any(found_rect is rect for found_rect in found_differences)
                if not is_already_found:
                    # Gambar kotak hint di sekitar perbedaan yang belum ditemukan pada gambar kanan
                    pygame.draw.rect(screen, RED, rect.move(right_pos), 5) # Ketebalan border 5
                    hint_found_for_display = True
                    break # Tampilkan hanya satu hint per permintaan
            
            if hint_found_for_display:
                hints_left -= 1
            show_hint_visual = False # Reset flag setelah hint ditampilkan atau jika tidak ada hint lagi

        # --- Tombol Hint ---
        hint_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 80, 200, 50) # Posisi tombol di bawah
        pygame.draw.rect(screen, BLUE, hint_button_rect, border_radius=10)
        draw_text(screen, font_ui, "Hint (H)", (hint_button_rect.centerx - font_ui.size("Hint (H)")[0] // 2, hint_button_rect.centery - font_ui.size("Hint (H)")[1] // 2), WHITE)

        # --- Logika Game Over / Menang ---
        # Kondisi Menang
        if len(found_differences) == len(differences_data_initial) and not game_over_state:
            # Menang
            win_text_surface = font_message.render("Selamat, Kamu Menang!", True, GREEN)
            win_text_rect = win_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            screen.blit(win_text_surface, win_text_rect)
            
            lanjut_text_surface = font_ui.render("Tekan ENTER untuk melanjutkan...", True, WHITE)
            lanjut_text_rect = lanjut_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            screen.blit(lanjut_text_surface, lanjut_text_rect)
            
            pygame.display.flip() # Pastikan pesan menang terlihat
            
            # Tunggu ENTER untuk melanjutkan
            waiting_for_continue = True
            while waiting_for_continue:
                for event_win in pygame.event.get():
                    if event_win.type == pygame.QUIT:
                        game_instance.quit_game()
                        return
                    if event_win.type == pygame.KEYDOWN:
                        if event_win.key == pygame.K_RETURN:
                            waiting_for_continue = False
                clock.tick(FPS) # Jaga game tetap responsif

            print("Spot the Difference MENANG! Transisi ke Desa 2.")
            game_instance.transition.start(GC.STATE_DESA_2) # <<< PERBAIKAN UTAMA: Transisi ke Desa 2
            return # Keluar dari loop mini-game

        # Kondisi Kalah
        elif guesses_left <= 0 and not game_over_state: # Jika nyawa habis
            game_over_state = True
            ask_retry_state = True # Langsung tanya retry

        if game_over_state and ask_retry_state:
            # Tampilkan pesan Game Over dan opsi Retry
            go_text_surface = font_message.render("Game Over", True, RED)
            go_text_rect = go_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(go_text_surface, go_text_rect)

            retry_text_surface = font_ui.render("Coba lagi? (Y = Ya / N = Tidak)", True, BLACK)
            retry_text_rect = retry_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
            screen.blit(retry_text_surface, retry_text_rect)


        # --- Event Handling Utama ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_instance.quit_game() # Gunakan fungsi quit global
                return # Keluar dari loop mini-game

            if game_over_state and ask_retry_state: # Hanya proses Y/N jika sedang bertanya retry
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        reset_game_state_internal() # Reset state internal game
                        # Tidak perlu 'continue' karena loop utama akan menggambar ulang
                    elif event.key == pygame.K_n:
                        print("Spot the Difference KALAH dan tidak retry. Transisi ke Main Menu.")
                        game_instance.transition.start(GC.STATE_MAIN_MENU) # <<< PERBAIKAN: Transisi jika kalah & tidak retry
                        return # Keluar dari loop mini-game
            
            elif not game_over_state: # Jika game belum over (masih bermain)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Klik kiri
                        if hint_button_rect.collidepoint(event.pos):
                            if hints_left > 0 and not show_hint_visual: # Hanya aktifkan jika ada hint dan belum aktif
                                show_hint_visual = True
                                print("Tombol Hint ditekan.")
                        else:
                            check_click_action(event.pos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h: # Tombol 'H' untuk hint
                         if hints_left > 0 and not show_hint_visual:
                            show_hint_visual = True
                            print("Tombol 'H' untuk Hint ditekan.")
                    # Tambahkan tombol ESC untuk kembali ke state sebelumnya jika diinginkan (opsional)
                    elif event.key == pygame.K_ESCAPE:
                        print("ESC ditekan di Spot Difference. Kembali ke Awan.")
                        game_instance.transition.start(GC.STATE_AWAN) # Asumsi state sebelum stage 2 adalah awan
                        return


        pygame.display.flip()
        clock.tick(FPS)

    # Jika loop 'running' selesai karena alasan lain (seharusnya tidak terjadi dengan logika di atas)
    # Default kembali ke main menu jika keluar dari loop tanpa transisi eksplisit.
    print("Keluar dari loop utama Spot Difference tanpa transisi yang jelas.")
    game_instance.transition.start(GC.STATE_MAIN_MENU)