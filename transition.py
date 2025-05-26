# transition.py
import pygame

class Transition:
    def __init__(self, duration_ms, color=(0, 0, 0)):
        self.duration = duration_ms
        self.color = color
        self.timer = 0
        self.active = False
        self.alpha = 0
        self.next_state = None # State tujuan
        self.current_fade_type = "out" # Default fade type

    # PERBAIKAN: Tambahkan parameter fade_type
    def start(self, next_state_key, fade_type="out"): # default "out" (dari jelas ke buram)
        self.active = True
        self.timer = 0
        self.next_state = next_state_key
        self.current_fade_type = fade_type

        if self.current_fade_type == "in": # Transisi MASUK ke scene baru (dari buram/hitam menjadi jelas)
            self.alpha = 255 # Mulai dari buram penuh
        else: # Transisi KELUAR dari scene lama (dari jelas menjadi buram/hitam)
            self.alpha = 0   # Mulai dari transparan (akan menjadi buram)
        print(f"Transition started to {next_state_key}, type: {self.current_fade_type}, duration: {self.duration}, initial_alpha: {self.alpha}")

    def reset(self):
        self.active = False
        self.timer = 0
        # self.alpha = 0 # Alpha akan di-set ulang saat start() dipanggil lagi
        self.next_state = None
        print("Transition reset.")

    def update(self, dt_ms):
        if not self.active:
            return None

        self.timer += dt_ms
        progress = min(1.0, self.timer / self.duration)

        if self.current_fade_type == "in": # Dari buram (255) ke jelas (0)
            self.alpha = int(255 * (1.0 - progress))
        else: # "out": Dari jelas (0) ke buram (255)
            self.alpha = int(255 * progress)
        
        self.alpha = max(0, min(255, self.alpha)) # Pastikan alpha dalam rentang 0-255

        if self.timer >= self.duration:
            self.active = False 
            # Saat transisi selesai:
            # Jika itu adalah fade-in, alpha akan menjadi ~0 (jelas).
            # Jika itu adalah fade-out, alpha akan menjadi ~255 (buram).
            print(f"Transition effect finished for {self.next_state}. Final alpha: {self.alpha}")
            # Alpha bisa direset di sini jika mau, tapi biasanya tidak perlu karena start() akan set lagi
            # self.alpha = 0 
            return self.next_state 
        
        return None 

    def draw(self, screen):
        if self.active:
            if self.alpha > 0: # Hanya gambar jika ada sesuatu untuk digambar (alpha > 0)
                fade_surface = pygame.Surface(screen.get_size())
                fade_surface.fill(self.color)
                fade_surface.set_alpha(self.alpha)
                screen.blit(fade_surface, (0, 0))
    
    def is_active(self):
        return self.active