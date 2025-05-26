# pre_stage_1b_scene.py
import pygame
from constants import GameConstants as GC
from utils import load_image

def run_pre_stage_1b_scene(game_instance):
    print("DEBUG: run_pre_stage_1b_scene - CALLED")
    screen = game_instance.screen
    clock = game_instance.clock
    
    player_right_sprites = game_instance.player_right_anim_scaled
    player_left_sprites = game_instance.player_left_anim_scaled
    npc1_sprite = game_instance.npc1_img_scaled

    player_rect = pygame.Rect(50, 495, 50, 80)
    facing_right = True
    frame_index = 0
    animation_timer_ms = 0
    PLAYER_ANIMATION_INTERVAL_MS = 100
    PLAYER_SPEED = 5

    wall1 = pygame.Rect(0, 0, 1022, 456)
    wall2 = pygame.Rect(1267, 0, 653, 413)
    wall3 = pygame.Rect(1022, 0, 245, 380)
    wall4 = pygame.Rect(0, 661, 1002, 423)
    wall5 = pygame.Rect(1256, 661, 664, 419)
    
    npc_pos_tuple = (1065 + 60, 296) 
    trigger_npc_rect = pygame.Rect(npc_pos_tuple[0] - 30, npc_pos_tuple[1] - 30, 
                                   npc1_sprite.get_width() + 60 if npc1_sprite else 120, 
                                   npc1_sprite.get_height() + 60 if npc1_sprite else 150)

    dialog_active = False
    dialog_index = 0
    dialog_with_npc_list = game_instance.dialogues.get("pre_stage_1b_npc_dialog", ["NPC: Siap untuk tantangan di labirin?"]) 
    dialog_completed = False

    WIDTH, HEIGHT = GC.SCREEN_WIDTH, GC.SCREEN_HEIGHT
    background_surface = game_instance.pre_stage_1b_bg
    dialog_box_surface = game_instance.dialog_box_img
    
    try:
        font_prompt = pygame.font.Font("data/fonts/dogicapixelbold.otf", GC.FONT_SIZE_SMALL)
        font_dialog_text = pygame.font.Font("data/fonts/dogicapixelbold.otf", GC.FONT_SIZE_SMALL)
    except pygame.error:
        print("Warning: Font kustom tidak ditemukan di pre_stage_1b_scene, menggunakan default.")
        font_prompt = pygame.font.Font(None, GC.FONT_SIZE_SMALL + 5)
        font_dialog_text = pygame.font.Font(None, GC.FONT_SIZE_SMALL + 5)

    running = True
    transition_initiated_by_this_scene = False # Flag untuk mengontrol logika setelah transisi dimulai
    print("DEBUG: Pre-Stage 1B Scene - Loop utama dimulai")

    while running:
        delta_time_ms = clock.tick(GC.FPS) 

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_instance.quit_game()
                return
            
            if not transition_initiated_by_this_scene: # Hanya proses input jika belum memulai transisi
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        player_collides_with_npc_trigger = player_rect.colliderect(trigger_npc_rect)
                        if dialog_active:
                            dialog_index += 1
                            if dialog_index >= len(dialog_with_npc_list):
                                dialog_active = False
                                dialog_completed = True
                        elif player_collides_with_npc_trigger and not dialog_completed:
                            dialog_active = True
                            dialog_index = 0
                        elif player_collides_with_npc_trigger and dialog_completed:
                            if not game_instance.transition.is_active():
                                print("Pre-Stage 1B: Dialog NPC selesai. Memulai transisi ke Stage 1 (Pacman)!")
                                # PERBAIKAN DI SINI:
                                game_instance.transition.start(GC.STATE_STAGE_1, fade_type="out")
                                transition_initiated_by_this_scene = True
        
        # --- Logika Update Scene (Hanya jika transisi belum dimulai OLEH SCENE INI) ---
        if not transition_initiated_by_this_scene:
            keys = pygame.key.get_pressed()
            is_moving = False

            if not dialog_active: 
                if keys[pygame.K_LEFT]:
                    player_rect.x -= PLAYER_SPEED; facing_right = False; is_moving = True
                if keys[pygame.K_RIGHT]:
                    player_rect.x += PLAYER_SPEED; facing_right = True; is_moving = True
                if keys[pygame.K_UP]:
                    player_rect.y -= PLAYER_SPEED; is_moving = True 
                if keys[pygame.K_DOWN]:
                    player_rect.y += PLAYER_SPEED; is_moving = True 
            
            old_player_pos_tuple = player_rect.topleft 
            player_rect.clamp_ip(screen.get_rect()) 
            for wall in [wall1, wall2, wall3, wall4, wall5]: 
                if player_rect.colliderect(wall):
                    player_rect.topleft = old_player_pos_tuple 
                    is_moving = False 
                    break 

            if is_moving:
                animation_timer_ms += delta_time_ms
                if animation_timer_ms >= PLAYER_ANIMATION_INTERVAL_MS:
                    frame_index = (frame_index + 1) % len(player_right_sprites) 
                    animation_timer_ms = 0
            else:
                frame_index = 0
                animation_timer_ms = 0
        
        # --- Penggambaran Scene ---
        if background_surface: screen.blit(background_surface, (0, 0))
        else: screen.fill((60,60,70)) 
        
        current_player_sprite = player_right_sprites[frame_index] if facing_right else player_left_sprites[frame_index]
        
        if npc1_sprite: screen.blit(npc1_sprite, npc_pos_tuple)
        screen.blit(current_player_sprite, player_rect.topleft)

        prompt_message = ""
        prompt_color = (255,255,255)
        if player_rect.colliderect(trigger_npc_rect):
            if not dialog_active and not dialog_completed:
                prompt_message = "Tekan ENTER untuk bicara"
            elif dialog_completed and not transition_initiated_by_this_scene:
                prompt_message = "Tekan ENTER untuk masuk ke tantangan"
                prompt_color = (255,255,0)
        
        if prompt_message:
            text_surf = font_prompt.render(prompt_message, True, prompt_color)
            text_r_prompt = text_surf.get_rect(center=(WIDTH // 2, HEIGHT - 60))
            bg_r_prompt = text_r_prompt.inflate(20,10)
            prompt_bg_surf = pygame.Surface(bg_r_prompt.size, pygame.SRCALPHA)
            prompt_bg_surf.fill((0,0,0,180))
            screen.blit(prompt_bg_surf, bg_r_prompt.topleft)
            screen.blit(text_surf, text_r_prompt)

        if dialog_active and dialog_index < len(dialog_with_npc_list):
            if dialog_box_surface:
                dialog_box_x = (WIDTH - dialog_box_surface.get_width()) // 2
                dialog_box_y = HEIGHT - dialog_box_surface.get_height() - 30
                screen.blit(dialog_box_surface, (dialog_box_x, dialog_box_y))
                dialog_text_surf = font_dialog_text.render(dialog_with_npc_list[dialog_index], True, (20, 20, 20))
                screen.blit(dialog_text_surf, (dialog_box_x + 50, dialog_box_y + 40))
        
        game_instance.transition.draw(screen) 
        pygame.display.flip() 

        # --- Logika Penghentian Loop ---
        if transition_initiated_by_this_scene:
            print(f"DEBUG: Pre-Stage 1B Scene - Transisi ke {game_instance.transition.next_state} telah dimulai. Menghentikan loop.")
            running = False

    print(f"DEBUG: Pre-Stage 1B Scene - Loop berakhir. Kembali ke game.py.")
    return