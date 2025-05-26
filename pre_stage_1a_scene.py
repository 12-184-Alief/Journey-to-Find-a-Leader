# pre_stage_1a_scene.py
import pygame
from constants import GameConstants as GC
from utils import load_image 

def run_pre_stage_1a_scene(game_instance):
    print("DEBUG: run_pre_stage_1a_scene - CALLED")
    screen = game_instance.screen
    clock = game_instance.clock 

    try:
        player_right_sprites = [pygame.image.load(f"data/images/entities/Bimas Kanan/{i}.png").convert_alpha() for i in range(1, 5)]
        player_left_sprites = [pygame.image.load(f"data/images/entities/Bimas Kiri/{i}.png").convert_alpha() for i in range(1, 5)]
    except pygame.error as e:
        print(f"Error loading player sprites for Pre-Stage 1A: {e}")
        player_right_sprites = [pygame.Surface((50,80), pygame.SRCALPHA)] * 4
        player_left_sprites = [pygame.Surface((50,80), pygame.SRCALPHA)] * 4
        for surf in player_right_sprites: surf.fill((0,255,0))
        for surf in player_left_sprites: surf.fill((0,200,0))

    PLAYER_WIDTH = 50
    PLAYER_HEIGHT = 80
    PLAYER_SPEED = 5
    PLAYER_ANIMATION_INTERVAL_MS = 120 

    jalan_top_y = 400      
    jalan_bottom_y = 580   
                           
    start_player_x = 50
    start_player_y = jalan_top_y + (jalan_bottom_y - jalan_top_y - PLAYER_HEIGHT) // 2 
    player_rect = pygame.Rect(start_player_x, start_player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    facing_right = True
    frame_index = 0
    animation_timer_ms = 0

    trigger_zone_width = 100
    trigger_zone_height = jalan_bottom_y - jalan_top_y 
    trigger_zone_x = GC.SCREEN_WIDTH - trigger_zone_width - 30 
    trigger_zone_y = jalan_top_y
    trigger_zone = pygame.Rect(trigger_zone_x, trigger_zone_y, trigger_zone_width, trigger_zone_height)

    try:
        font_prompt = pygame.font.Font("data/fonts/dogicapixelbold.otf", GC.FONT_SIZE_SMALL)
    except pygame.error:
        font_prompt = pygame.font.Font(None, GC.FONT_SIZE_SMALL + 10)

    running = True
    transition_initiated_by_this_scene = False # Untuk mengontrol logika setelah transisi dimulai
    print("DEBUG: Pre-Stage 1A Scene - Loop utama dimulai")

    while running:
        delta_time_ms = clock.tick(GC.FPS) 
        
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_instance.quit_game()
                return 
            
            if not transition_initiated_by_this_scene: # Hanya proses input jika belum memulai transisi
                if event.type == pygame.KEYDOWN:
                    colliding_with_trigger = player_rect.colliderect(trigger_zone)
                    if event.key == pygame.K_RETURN and colliding_with_trigger:
                        if not game_instance.transition.is_active(): 
                            print("DEBUG: Pre-Stage 1A - ENTER di trigger! Memulai transisi ke Pre-Stage 1B.")
                            # PERBAIKAN DI SINI:
                            game_instance.transition.start(GC.STATE_PRE_STAGE_1B, fade_type="out") 
                            transition_initiated_by_this_scene = True 
                    # elif event.key == pygame.K_p: 
                    #     print(f"Player: {player_rect}, Trigger: {trigger_zone}, Colliding: {player_rect.colliderect(trigger_zone)}")

        # --- Logika Update Scene (Hanya jika transisi belum dimulai OLEH SCENE INI) ---
        if not transition_initiated_by_this_scene:
            keys = pygame.key.get_pressed()
            is_moving = False

            if keys[pygame.K_LEFT]:
                player_rect.x -= PLAYER_SPEED; facing_right = False; is_moving = True
            if keys[pygame.K_RIGHT]:
                player_rect.x += PLAYER_SPEED; facing_right = True; is_moving = True
            
            if keys[pygame.K_UP]:
                if player_rect.top - PLAYER_SPEED >= jalan_top_y:
                    player_rect.y -= PLAYER_SPEED; is_moving = True
                elif player_rect.top > jalan_top_y : 
                    player_rect.top = jalan_top_y
            if keys[pygame.K_DOWN]:
                if player_rect.bottom + PLAYER_SPEED <= jalan_bottom_y:
                    player_rect.y += PLAYER_SPEED; is_moving = True
                elif player_rect.bottom < jalan_bottom_y: 
                    player_rect.bottom = jalan_bottom_y
            
            if player_rect.left < 0: player_rect.left = 0
            if player_rect.right > GC.SCREEN_WIDTH: player_rect.right = GC.SCREEN_WIDTH
            if player_rect.top < jalan_top_y: player_rect.top = jalan_top_y
            if player_rect.bottom > jalan_bottom_y: player_rect.bottom = jalan_bottom_y

            if is_moving:
                animation_timer_ms += delta_time_ms
                if animation_timer_ms >= PLAYER_ANIMATION_INTERVAL_MS:
                    frame_index = (frame_index + 1) % len(player_right_sprites)
                    animation_timer_ms = 0
            else:
                frame_index = 0 
                animation_timer_ms = 0
        
        # --- Penggambaran Scene ---
        if game_instance.pre_stage_1a_bg:
            screen.blit(game_instance.pre_stage_1a_bg, (0, 0))
        else:
            screen.fill((50,50,50)) 

        current_sprite = player_right_sprites[frame_index] if facing_right else player_left_sprites[frame_index]
        screen.blit(current_sprite, player_rect.topleft)

        pygame.draw.rect(screen, (255,0,0), trigger_zone, 2) 

        if player_rect.colliderect(trigger_zone) and not transition_initiated_by_this_scene: 
            text_surf = font_prompt.render("Tekan ENTER untuk masuk desa", True, (255, 255, 255))
            text_r = text_surf.get_rect(center=(GC.SCREEN_WIDTH // 2, GC.SCREEN_HEIGHT - 60))
            bg_r = text_r.inflate(20,10)
            prompt_bg_surface = pygame.Surface(bg_r.size, pygame.SRCALPHA)
            prompt_bg_surface.fill((0,0,0,150))
            screen.blit(prompt_bg_surface, bg_r.topleft)
            screen.blit(text_surf, text_r)

        game_instance.transition.draw(screen) 
        pygame.display.flip() 

        # --- Logika Penghentian Loop ---
        if transition_initiated_by_this_scene:
            # Jika scene ini yang memulai transisi, kita biarkan frame ini tergambar
            # lalu di iterasi berikutnya, running akan false dan fungsi akan return.
            # game.py akan menangani sisa durasi transisi.
            print(f"DEBUG: Pre-Stage 1A Scene - Transisi ke {game_instance.transition.next_state} telah dimulai oleh scene ini. Menghentikan loop.")
            running = False

    print(f"DEBUG: Pre-Stage 1A Scene - Loop berakhir. Kembali ke game.py.")
    return