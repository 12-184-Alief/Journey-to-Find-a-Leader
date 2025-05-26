# buttons.py
import pygame

class Button:
    def __init__(self, image_normal, image_hover, x, y, action=None, sound_hover=None, sound_click=None):
        # Pastikan gambar tidak None sebelum memanggil get_rect
        if image_normal is None:
            # Buat placeholder jika gambar normal tidak ada
            print(f"Warning: image_normal is None for a button at ({x},{y}). Creating placeholder.")
            self.image_normal = pygame.Surface((100, 50)) # Ukuran placeholder
            self.image_normal.fill((128, 128, 128)) # Warna abu-abu
        else:
            self.image_normal = image_normal
        
        self.image_hover = image_hover if image_hover is not None else self.image_normal
        self.action = action

        self.rect = self.image_normal.get_rect()
        self.rect.topleft = (x, y)

        self.is_hovered = False
        self.sound_hover = sound_hover
        self.sound_click = sound_click
        self.hover_sound_played = False


    def draw(self, surface):
        current_image = self.image_hover if self.is_hovered else self.image_normal
        surface.blit(current_image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self.is_hovered
            self.is_hovered = self.rect.collidepoint(event.pos)
            if self.is_hovered and not was_hovered and self.sound_hover:
                try:
                    self.sound_hover.play()
                except AttributeError: # Jika sound_hover bukan objek sound Pygame
                    print("Warning: sound_hover is not a valid Pygame sound object.")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered: # Klik kiri
                if self.sound_click:
                    try:
                        self.sound_click.play()
                    except AttributeError:
                        print("Warning: sound_click is not a valid Pygame sound object.")
                if self.action:
                    self.action()
                    return True # Menandakan aksi tombol telah dipicu
        return False