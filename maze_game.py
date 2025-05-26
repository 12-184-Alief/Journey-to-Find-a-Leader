# maze_game.py
import pygame
import sys
import random

from constants import GameConstants as GC
from utils import load_image

# --- Konfigurasi ---
FPS = 60
TILE_SIZE = 40 

# Layout maze
maze_definition = [ # Ganti nama variabel agar tidak bentrok dengan modul 'maze' jika ada
    "################################################", 
    "################################################", 
    "####                #                #       ###", 
    "####                #                #       ###", 
    "####         ####   #  ###########   #   #   ###", 
    "###########  #         #                 #   ###", 
    "####      #  #         #                 #   ###", 
    "####      #  #   ####  #                 #   ###", 
    "####      #  #   #  #  #  ###########    #   ###", 
    "####  #   #  #   #  #  #  ##  #              ###", 
    "## P  #   #  #   #     #  ##  #              ###", 
    "####  #   #  #   #     #  ##  #              ###", 
    "####  #   #  #   #  ####    #         ####   ###", 
    "####  #      #   #  #  #                 #   ###", 
    "####  #      #   #  #  #                 #   ###", 
    "####  #      #   #  #  #                 #   ###", 
    "####  ########      #  #####   ######    #######", 
    "####  #             #                       ####", 
    "####  #             #                       ####", 
    "####  #             #                       ####", 
    "####  #   ###########    ######   ########  ####", 
    "####                       #             #  ####", 
    "####                       #             #  ####", 
    "####                       #             #  ####", 
    "################################################", 
    "################################################", 
    "################################################"  
]
# Simpan maze asli untuk reset jika diperlukan
original_maze_layout_for_maze_game = [row[:] for row in maze_definition] 

class Enemy:
    def __init__(self, x, y, image_path, tile_size, maze_layout_ref):
        self.pos = [x, y]
        loaded_img = load_image(image_path)
        if loaded_img:
            self.image = pygame.transform.scale(loaded_img, (tile_size, tile_size))
        else:
            self.image = pygame.Surface((tile_size, tile_size))
            self.image.fill((255,0,0)) 
            print(f"Warning: Gagal memuat gambar musuh di path: {image_path} untuk Enemy di ({x},{y})")
        self.move_timer = 0
        self.move_delay = 450 
        self.maze_ref = maze_layout_ref

    def draw(self, screen, tile_size):
        screen.blit(self.image, (self.pos[0] * tile_size, self.pos[1] * tile_size))

    def update(self, current_time, player_pos):
        if current_time - self.move_timer > self.move_delay:
            if self.is_player_near(player_pos):
                self.chase_player(player_pos)
            else:
                self.move_random()
            self.move_timer = current_time

    def is_player_near(self, player_pos, sight_range=8):
        distance_x = abs(self.pos[0] - player_pos[0])
        distance_y = abs(self.pos[1] - player_pos[1])
        return distance_x <= sight_range and distance_y <= sight_range

    def chase_player(self, player_pos):
        dx_total = player_pos[0] - self.pos[0]
        dy_total = player_pos[1] - self.pos[1]
        possible_moves = []
        if abs(dx_total) > abs(dy_total):
            if dx_total != 0: possible_moves.append((1 if dx_total > 0 else -1, 0))
            if dy_total != 0: possible_moves.append((0, 1 if dy_total > 0 else -1))
        else:
            if dy_total != 0: possible_moves.append((0, 1 if dy_total > 0 else -1))
            if dx_total != 0: possible_moves.append((1 if dx_total > 0 else -1, 0))
        
        random_moves = [(1,0), (-1,0), (0,1), (0,-1)]
        random.shuffle(random_moves)
        for move in random_moves:
            if move not in possible_moves:
                possible_moves.append(move)

        for dx, dy in possible_moves:
            new_x = self.pos[0] + dx
            new_y = self.pos[1] + dy
            if self.can_move_to(new_x, new_y):
                self.pos = [new_x, new_y]
                return

    def move_random(self):
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = self.pos[0] + dx
            new_y = self.pos[1] + dy
            if self.can_move_to(new_x, new_y):
                self.pos = [new_x, new_y]
                break

    def can_move_to(self, x, y):
        return (0 <= y < len(self.maze_ref) and
                0 <= x < len(self.maze_ref[0]) and
                self.maze_ref[y][x] != '#')

# --- KELAS TURUNAN ---
class Skeleton(Enemy):
    def __init__(self, x, y, tile_size, maze_layout_ref): # Hanya 4 argumen + self
        super().__init__(x, y, "data/images/entities/skeleton.png", tile_size, maze_layout_ref)
        
class Serigala(Enemy):
    def __init__(self, x, y, tile_size, maze_layout_ref): # Hanya 4 argumen + self
        super().__init__(x, y, "data/images/entities/serigala.png", tile_size, maze_layout_ref)

# --- Fungsi Helper untuk Maze Game ---
def find_char_in_maze(char_to_find, maze_layout_to_search):
    for r_idx, row_str in enumerate(maze_layout_to_search):
        for c_idx, tile_symbol in enumerate(row_str):
            if tile_symbol == char_to_find:
                return [c_idx, r_idx]
    return None

def draw_player(screen, player_pos_coords, current_player_sprite_surface, tile_size_pixels):
    offset_x = (tile_size_pixels - current_player_sprite_surface.get_width()) // 2
    offset_y = (tile_size_pixels - current_player_sprite_surface.get_height()) // 2
    screen.blit(current_player_sprite_surface, 
                (player_pos_coords[0] * tile_size_pixels + offset_x, 
                 player_pos_coords[1] * tile_size_pixels + offset_y))

def move_player(player_pos_coords, dx_move, dy_move, current_maze_layout):
    new_x_coord = player_pos_coords[0] + dx_move
    new_y_coord = player_pos_coords[1] + dy_move
    if 0 <= new_y_coord < len(current_maze_layout) and \
       0 <= new_x_coord < len(current_maze_layout[0]) and \
       current_maze_layout[new_y_coord][new_x_coord] != '#':
        player_pos_coords[0] = new_x_coord
        player_pos_coords[1] = new_y_coord
        return True
    return False

def check_collision_with_enemies(player_pos_coords, enemies_list_data, lives_list_ref, 
                                 last_hit_time_list_ref, player_start_pos_coords, 
                                 hit_cooldown_val_ms, loss_callback_func, current_game_time_ms):
    for enemy_unit in enemies_list_data:
        if player_pos_coords == enemy_unit.pos:
            if current_game_time_ms - last_hit_time_list_ref[0] >= hit_cooldown_val_ms:
                lives_list_ref[0] -= 1
                print(f"Player terkena musuh! Sisa nyawa: {lives_list_ref[0]}")
                last_hit_time_list_ref[0] = current_game_time_ms
                player_pos_coords[0] = player_start_pos_coords[0]
                player_pos_coords[1] = player_start_pos_coords[1]
                
                if lives_list_ref[0] <= 0:
                    print("Nyawa habis!")
                    loss_callback_func() # Panggil fungsi yang akan set running = False dan mulai transisi
                    return True # Kolisi fatal terjadi
            return False # Terkena tapi cooldown
    return False 

def draw_items(screen_surface, items_pos_list, item_img_surf, tile_size_px):
    for item_xy in items_pos_list:
        screen_surface.blit(item_img_surf, (item_xy[0] * tile_size_px, item_xy[1] * tile_size_px))

def check_item_collection_action(player_xy_list, current_items_pos_list_ref, score_val_list_ref):
    for item_xy in current_items_pos_list_ref[:]:
        if player_xy_list[0] == item_xy[0] and player_xy_list[1] == item_xy[1]:
            current_items_pos_list_ref.remove(item_xy)
            score_val_list_ref[0] += 10
            print(f"Tanaman diambil! Skor: {score_val_list_ref[0]}")

# --- Fungsi Utama Maze Game ---
def run_maze_game(game_instance):
    print("DEBUG: run_maze_game - CALLED")
    screen = game_instance.screen
    WIDTH = GC.SCREEN_WIDTH
    HEIGHT = GC.SCREEN_HEIGHT
    clock = game_instance.clock

    # --- Font ---
    # (Kode inisialisasi font seperti pada versi sebelumnya yang sudah baik)
    game_font_large = None
    game_font_small = None
    font_default_path = "data/fonts/dogicapixelbold.otf" 
    try:
        if hasattr(game_instance, 'font') and game_instance.font:
            loaded_font_path = font_default_path 
        else: 
            loaded_font_path = font_default_path
        game_font_large = pygame.font.Font(loaded_font_path, 36)
        game_font_small = pygame.font.Font(loaded_font_path, 28)
    except Exception: # Lebih umum untuk menangkap semua potensi error font
        print(f"Warning: Gagal memuat font utama atau default di maze_game, menggunakan font sistem.")
    if game_font_large is None: game_font_large = pygame.font.SysFont(None, 48)
    if game_font_small is None: game_font_small = pygame.font.SysFont(None, 36)


    # --- Aset Gambar ---
    labirin_bg_surface = game_instance.pacman_bg 
    item_img_surface = pygame.transform.scale(load_image("data/images/entities/Tanaman.png"), (TILE_SIZE, TILE_SIZE))
    
    # --- Inisialisasi Maze dan Pemain ---
    current_maze_layout = [row[:] for row in original_maze_layout_for_maze_game] 
    player_start_pos_val = find_char_in_maze('P', current_maze_layout)
    if player_start_pos_val is None:
        player_start_pos_val = [2,10] 
    
    temp_maze_list_of_lists = [list(row_str) for row_str in current_maze_layout]
    if 0 <= player_start_pos_val[1] < len(temp_maze_list_of_lists) and \
       0 <= player_start_pos_val[0] < len(temp_maze_list_of_lists[0]) and \
       temp_maze_list_of_lists[player_start_pos_val[1]][player_start_pos_val[0]] == 'P':
        temp_maze_list_of_lists[player_start_pos_val[1]][player_start_pos_val[0]] = ' '
    current_maze_layout = ["".join(row_list) for row_list in temp_maze_list_of_lists]

    player_current_pos_list = player_start_pos_val[:]
    lives_val = [3]
    score_val = [0]

    hit_cooldown_duration_ms = 2000
    last_hit_timestamp_ms = [pygame.time.get_ticks() - hit_cooldown_duration_ms]

    player_sprite_size = (TILE_SIZE, int(TILE_SIZE * 1.5)) 
    player_right_anim_list = [pygame.transform.scale(load_image(f"data/images/entities/Bimas Kanan/{i}.png"), player_sprite_size) for i in range(1, 5)]
    player_left_anim_list = [pygame.transform.scale(load_image(f"data/images/entities/Bimas Kiri/{i}.png"), player_sprite_size) for i in range(1, 5)]
    
    player_facing_right_bool = True
    player_anim_frame_idx = 0
    player_anim_frame_timer_ms = 0
    player_animation_speed_ms = 120

    player_move_timer_ms = 0
    player_move_delay_ms = 150

    enemy1_start_pos = find_char_in_maze('1', current_maze_layout) if find_char_in_maze('1', current_maze_layout) else [10, 5]
    enemy2_start_pos = find_char_in_maze('2', current_maze_layout) if find_char_in_maze('2', current_maze_layout) else [30, 15]
    
    enemy1 = Skeleton(enemy1_start_pos[0], enemy1_start_pos[1], TILE_SIZE, current_maze_layout)
    enemy2 = Serigala(enemy2_start_pos[0], enemy2_start_pos[1], TILE_SIZE, current_maze_layout)
    enemies_list = [enemy1, enemy2]

    initial_items_pos_list = [
        [5, 3], [7, 3], [9, 3], [11, 3], [13, 3], [15, 3], [17, 3], [19, 3],[21, 3], [23, 3], 
        [25, 3], [27, 3], [29, 3], [31, 3], [33, 3], [35, 3], [38, 3], [40, 3], [42, 3], [18, 4], 
        [22, 4], [35, 4], [39, 4], [43, 4], [15,5], [15, 7], [8, 18], [8, 20] ,[15, 6] ,[15, 7] ,
        [15, 9], [15, 11], [15, 13], [15, 15], [15, 17], [15, 18], [11, 18], [13, 18], [17, 18] ,
        [18, 5], [20, 5], [22, 5], [11, 4], [11, 6], [11, 8], [11, 10], [11, 12], [11, 14], [8,14], 
        [8, 12], [8, 10], [8, 8], [8, 6], [8, 22], [10, 22], [12, 22], [14, 22], [16, 22] , [18, 22], 
        [20, 22], [22, 22], [22, 20], [22, 18], [24, 18], [26, 18], [28, 18], [30, 18], [32, 18], 
        [34, 18], [36, 18], [38, 18], [40, 18], [42, 18], [29, 16], [29, 14], [31, 14], [33, 14], 
        [35, 14], [37, 14], [27, 14], [25, 14], [25, 12], [25, 10], [25, 8], [25, 6], [27, 6], 
        [29, 6], [31, 6], [33, 6], [35, 6], [37, 6], [39, 6], [43, 6], [39, 8], [39, 10], [37, 10], [36, 12]
    ]
    current_items_list = [pos for pos in initial_items_pos_list 
                          if 0 <= pos[1] < len(current_maze_layout) and \
                             0 <= pos[0] < len(current_maze_layout[0]) and \
                             current_maze_layout[pos[1]][pos[0]] != '#']
    all_items_collected_flag = False

    # --- Kontrol Loop dan Transisi ---
    running = True 
    # transition_initiated_by_maze = False # Tidak lagi memerlukan flag ini dengan pendekatan baru

    def trigger_loss_condition_in_maze(): 
        nonlocal running
        print("Nyawa habis di Maze Game! Memulai transisi ke Desa Awal (Pre-Stage 1B).")
        game_instance.transition.start(GC.STATE_PRE_STAGE_1B, fade_type="out") 
        running = False
    
    print("DEBUG: Maze Game - Loop utama dimulai")
    while running:
        current_time_ms = pygame.time.get_ticks()
        delta_time_ms = clock.tick(FPS)

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_instance.quit_game()
                return 
            
            if all_items_collected_flag and player_current_pos_list == player_start_pos_val:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if not game_instance.transition.is_active(): # Hanya jika belum ada transisi lain
                        print("Maze Game: Menang! Memulai transisi ke AFT_STAGE_1B.")
                        game_instance.transition.start(GC.STATE_AFT_STAGE_1B, fade_type="out")
                        running = False # PERBAIKAN: Langsung set running False di sini
                        # Ini akan menyebabkan loop berhenti setelah frame ini selesai diproses & digambar.
                        # `return` tidak diperlukan di sini karena `running = False` akan menghentikan loop.
                    # else:
                        # print("DEBUG: Maze Game - ENTER menang, TAPI transisi global sudah aktif.")

        # Jika running menjadi False (karena menang atau kalah), kita skip sisa logika update
        # tapi kita tetap ingin menggambar frame terakhirnya dengan efek transisi awal.
        if not running:
            # Gambar frame terakhir sebelum keluar
            if labirin_bg_surface: screen.blit(labirin_bg_surface, (0, 0))
            else: screen.fill((20,20,20))
            draw_items(screen, current_items_list, item_img_surface, TILE_SIZE)
            # ... (gambar pemain, musuh, UI lainnya jika diperlukan untuk frame terakhir) ...
            game_instance.transition.draw(screen) 
            pygame.display.flip()
            break # Keluar dari while loop secara eksplisit

        # --- Logika Update (Hanya jika game masih berjalan) ---
        keys_pressed = pygame.key.get_pressed()
        player_moved_this_frame = False
        
        if current_time_ms - player_move_timer_ms >= player_move_delay_ms:
            dx, dy = 0, 0
            if keys_pressed[pygame.K_LEFT]:
                dx = -1; player_facing_right_bool = False
            elif keys_pressed[pygame.K_RIGHT]:
                dx = 1; player_facing_right_bool = True
            elif keys_pressed[pygame.K_UP]:
                dy = -1
            elif keys_pressed[pygame.K_DOWN]:
                dy = 1
            
            if dx != 0 or dy != 0:
                if move_player(player_current_pos_list, dx, dy, current_maze_layout): 
                    player_moved_this_frame = True
                    player_move_timer_ms = current_time_ms
                    check_item_collection_action(player_current_pos_list, current_items_list, score_val)
                    
                    if not current_items_list and not all_items_collected_flag:
                        all_items_collected_flag = True
                        print("Semua tanaman telah terkumpul! Kembali ke titik awal dan tekan ENTER.")

        if player_moved_this_frame:
            player_anim_frame_timer_ms += delta_time_ms
            if player_anim_frame_timer_ms >= player_animation_speed_ms:
                player_anim_frame_idx = (player_anim_frame_idx + 1) % len(player_right_anim_list)
                player_anim_frame_timer_ms = 0
        else:
            player_anim_frame_idx = 0
            player_anim_frame_timer_ms = 0
        
        for enemy_obj in enemies_list:
            enemy_obj.update(current_time_ms, player_current_pos_list)

        if check_collision_with_enemies(player_current_pos_list, enemies_list, lives_val, 
                                     last_hit_timestamp_ms, player_start_pos_val, 
                                     hit_cooldown_duration_ms, trigger_loss_condition_in_maze, 
                                     current_time_ms):
            if not running: # Jika callback collision membuat running jadi False
                # Gambar frame terakhir sebelum benar-benar keluar dari loop di iterasi berikutnya
                if labirin_bg_surface: screen.blit(labirin_bg_surface, (0, 0))
                else: screen.fill((20,20,20))
                # ... (gambar elemen lain jika perlu untuk frame terakhir saat kalah) ...
                game_instance.transition.draw(screen)
                pygame.display.flip()
                break # Keluar dari loop while


        # --- Penggambaran ---
        if labirin_bg_surface: screen.blit(labirin_bg_surface, (0, 0))
        else: screen.fill((20,20,20)) 
        
        draw_items(screen, current_items_list, item_img_surface, TILE_SIZE)
        
        current_player_sprite_surface = player_right_anim_list[player_anim_frame_idx] if player_facing_right_bool else player_left_anim_list[player_anim_frame_idx]
        if current_player_sprite_surface:
            if current_time_ms - last_hit_timestamp_ms[0] < hit_cooldown_duration_ms:
                if (current_time_ms // 150) % 2 == 0: 
                    draw_player(screen, player_current_pos_list, current_player_sprite_surface, TILE_SIZE)
            else:
                draw_player(screen, player_current_pos_list, current_player_sprite_surface, TILE_SIZE)

        for enemy_obj in enemies_list:
            enemy_obj.draw(screen, TILE_SIZE)

        info_panel_height = 60
        info_panel_rect = pygame.Rect(0, 0, WIDTH, info_panel_height)
        pygame.draw.rect(screen, (30, 30, 30, 200), info_panel_rect)

        score_text = game_font_large.render(f"Skor: {score_val[0]}", True, (255, 215, 0)) 
        screen.blit(score_text, (20, info_panel_height // 2 - score_text.get_height() // 2))

        lives_text_str = f"Nyawa: {lives_val[0]}"
        lives_color = (255, 60, 60) if lives_val[0] > 1 else ((255, 160, 0) if lives_val[0] == 1 else (100,100,100))
        lives_text = game_font_large.render(lives_text_str, True, lives_color)
        screen.blit(lives_text, (WIDTH - lives_text.get_width() - 20, info_panel_height // 2 - lives_text.get_height() // 2))
        
        if all_items_collected_flag: # Prompt selalu ditampilkan jika semua item terkumpul
            prompt_text_str = "Tekan ENTER untuk keluar labirin!" if player_current_pos_list == player_start_pos_val else "Semua tanaman terkumpul! Kembali ke titik awal."
            prompt_color = (173, 255, 47) if player_current_pos_list == player_start_pos_val else (255, 255, 100)
            prompt_text = game_font_small.render(prompt_text_str, True, prompt_color)
            prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
            bg_prompt_rect = prompt_rect.inflate(20,10)
            pygame.draw.rect(screen, (0,0,0,180), bg_prompt_rect) 
            screen.blit(prompt_text, prompt_rect)
        
        game_instance.transition.draw(screen) 
        pygame.display.flip() 

    # Setelah loop `while running` selesai (karena running = False)
    print(f"DEBUG: Maze Game - Loop berakhir. Kembali ke game.py. Transisi menuju: {game_instance.transition.next_state if game_instance.transition.next_state else 'Tidak ada (atau sudah selesai)'}")
    return