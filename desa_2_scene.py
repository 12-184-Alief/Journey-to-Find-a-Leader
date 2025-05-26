# desa_2_scene.py
import pygame
import sys 
from constants import GameConstants as GC
from utils import load_image 

def run_desa_2_scene(game_instance):
    print("DEBUG: run_desa_2_scene - CALLED")
    screen = game_instance.screen
    clock = game_instance.clock
    WIDTH, HEIGHT = GC.SCREEN_WIDTH, GC.SCREEN_HEIGHT
    FPS = GC.FPS

    # --- Font ---
    try:
        font_ui = pygame.font.Font("data/fonts/dogicapixelbold.otf", GC.FONT_SIZE_SMALL)
        font_dialog = pygame.font.Font("data/fonts/dogicapixelbold.otf", 21) 
    except pygame.error:
        print("Warning: Font kustom tidak ditemukan di desa_2_scene, menggunakan default.")
        font_ui = pygame.font.Font(None, GC.FONT_SIZE_SMALL + 4)
        font_dialog = pygame.font.Font(None, 24)

    # --- Aset Gambar ---
    background_image = load_image("data/images/entities/spotdifference_vilage.png") 
    if background_image:
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    else: 
        background_image = pygame.Surface((WIDTH, HEIGHT))
        background_image.fill((110,160,110))

    dialog_box_img = game_instance.dialog_box_img 
    DIALOG_BOX_WIDTH = dialog_box_img.get_width() if dialog_box_img else 1500
    DIALOG_BOX_HEIGHT = dialog_box_img.get_height() if dialog_box_img else 150
    
    player_right_sprites = game_instance.player_right_anim_scaled
    player_left_sprites = game_instance.player_left_anim_scaled

    npc_image = load_image("data/images/entities/npc2.png") 
    if npc_image:
        npc_image = pygame.transform.scale(npc_image, (60,90)) 
    else: 
        npc_image = pygame.Surface((60,90), pygame.SRCALPHA); npc_image.fill((200,0,0))

    # --- Inisialisasi Pemain ---
    PLAYER_WIDTH = player_right_sprites[0].get_width() if player_right_sprites else 50
    PLAYER_HEIGHT = player_right_sprites[0].get_height() if player_right_sprites else 80
    
    jalan_atas_y = 400 
    jalan_bawah_y = HEIGHT - 150 

    player_start_x = 100 
    player_start_y = 400 
    player_rect = pygame.Rect(player_start_x, player_start_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    PLAYER_SPEED = 5
    facing_right = True
    frame_index = 0
    animation_timer_ms = 0
    PLAYER_ANIMATION_INTERVAL_MS = 120

    # --- Dinding ---
    walls = [
        pygame.Rect(0, 0, 1920, 350), 
        pygame.Rect(0, 500, 1920, HEIGHT - jalan_bawah_y),
        pygame.Rect(1550, 350, 500, 500), 
    ]

    # --- Dialog ---
    dialog_active = False
    current_dialog_index = 0
    dialog_list = game_instance.dialogues.get(GC.STATE_DESA_2, [
        "Penduduk: Ksatria, terima kasih telah menyelamatkan desa kami!",
        "Ksatria: Sudah tugasku. Di mana penyihir itu sekarang?",
        "Penduduk: Dia melarikan diri ke kastilnya di pegunungan gelap!",
        "Ksatria: Aku akan mengejarnya!"
    ])
    dialog_completed = False

    # --- NPC dan Trigger Interaksi ---
    npc_width = npc_image.get_width() if npc_image else 60
    npc_height = npc_image.get_height() if npc_image else 90
    npc_pos_x = 1300 
    npc_pos_y = 400
    npc_rect = pygame.Rect(npc_pos_x, npc_pos_y, npc_width, npc_height)
    trigger_zone_interaction = npc_rect.inflate(80, 80) 

    running = True
    transition_initiated_by_this_scene = False # Flag
    print("DEBUG: Desa 2 Scene - Loop utama dimulai")
    while running:
        delta_time_ms = clock.tick(FPS)

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_instance.quit_game()
                return
            
            if not transition_initiated_by_this_scene:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        player_collides_with_npc_trigger = player_rect.colliderect(trigger_zone_interaction)
                        if dialog_active:
                            current_dialog_index += 1
                            if current_dialog_index >= len(dialog_list):
                                dialog_active = False
                                dialog_completed = True
                                # Setelah dialog selesai, langsung transisi
                                if not game_instance.transition.is_active():
                                    print("Desa 2: Dialog selesai. Memulai transisi ke Final Stage!")
                                    # PERBAIKAN DI SINI:
                                    game_instance.transition.start(GC.STATE_FINAL, fade_type="out")
                                    transition_initiated_by_this_scene = True
                        elif player_collides_with_npc_trigger and not dialog_completed:
                            dialog_active = True
                            current_dialog_index = 0
                        # Tidak perlu kondisi elif untuk (trigger and completed) karena transisi langsung setelah dialog.
        
        # --- Logika Update Scene (Hanya jika transisi belum dimulai OLEH SCENE INI) ---
        if not transition_initiated_by_this_scene:
            keys = pygame.key.get_pressed()
            is_moving = False

            if not dialog_active:
                old_player_rect_topleft = player_rect.topleft 

                if keys[pygame.K_LEFT]:
                    player_rect.x -= PLAYER_SPEED; facing_right = False; is_moving = True
                if keys[pygame.K_RIGHT]:
                    player_rect.x += PLAYER_SPEED; facing_right = True; is_moving = True
                
                if keys[pygame.K_UP]:
                    if player_rect.top - PLAYER_SPEED >= jalan_atas_y:
                        player_rect.y -= PLAYER_SPEED; is_moving = True
                    elif player_rect.top > jalan_atas_y: player_rect.top = jalan_atas_y
                if keys[pygame.K_DOWN]:
                    if player_rect.bottom + PLAYER_SPEED <= jalan_bawah_y:
                        player_rect.y += PLAYER_SPEED; is_moving = True
                    elif player_rect.bottom < jalan_bawah_y: player_rect.bottom = jalan_bawah_y
            
                player_rect.clamp_ip(screen.get_rect()) 
                for wall_rect in walls:
                    if player_rect.colliderect(wall_rect):
                        player_rect.topleft = old_player_rect_topleft 
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
        if background_image: screen.blit(background_image, (0, 0))
        else: screen.fill((120,170,120))
        
        if npc_image:
            screen.blit(npc_image, npc_rect.topleft)

        if player_right_sprites and player_left_sprites: 
            current_player_sprite = player_right_sprites[frame_index] if facing_right else player_left_sprites[frame_index]
            if current_player_sprite: 
                 screen.blit(current_player_sprite, player_rect.topleft)

        if not transition_initiated_by_this_scene:
            if player_rect.colliderect(trigger_zone_interaction) and not dialog_active and not dialog_completed:
                prompt_surface = font_ui.render("Tekan ENTER untuk bicara", True, (255, 255, 255))
                prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT - 60))
                bg_prompt_rect = prompt_rect.inflate(20,10)
                pygame.draw.rect(screen, (0,0,0,180), bg_prompt_rect)
                screen.blit(prompt_surface, prompt_rect)
        
        if dialog_active and current_dialog_index < len(dialog_list):
            if dialog_box_img:
                dialog_box_draw_x = (WIDTH - DIALOG_BOX_WIDTH) // 2
                dialog_box_draw_y = HEIGHT - DIALOG_BOX_HEIGHT - 20
                screen.blit(dialog_box_img, (dialog_box_draw_x, dialog_box_draw_y))
                
                max_text_width = DIALOG_BOX_WIDTH - 100 
                words = dialog_list[current_dialog_index].split(' ')
                lines_to_render = []
                current_line_render = ""
                for word in words:
                    test_line_render = current_line_render + word + " "
                    if font_dialog.size(test_line_render)[0] <= max_text_width:
                        current_line_render = test_line_render
                    else:
                        lines_to_render.append(current_line_render.strip())
                        current_line_render = word + " "
                lines_to_render.append(current_line_render.strip())

                text_y_offset = dialog_box_draw_y + 35 
                line_spacing = 5 
                for line_str_render in lines_to_render:
                    dialog_text_surface = font_dialog.render(line_str_render, True, (30, 30, 30)) 
                    screen.blit(dialog_text_surface, (dialog_box_draw_x + 60, text_y_offset)) 
                    text_y_offset += font_dialog.get_height() + line_spacing

        game_instance.transition.draw(screen) 
        pygame.display.flip() 

        # --- Logika Penghentian Loop ---
        if transition_initiated_by_this_scene:
            print(f"DEBUG: Desa 2 Scene - Transisi ke {game_instance.transition.next_state} telah dimulai. Menghentikan loop.")
            running = False

    print(f"DEBUG: Desa 2 Scene - Loop berakhir. Kembali ke game.py.")
    return