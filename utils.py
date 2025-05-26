# utils.py
import pygame

def load_image(path, size=None):
    try:
        # Coba muat dengan convert_alpha() untuk transparansi yang benar
        img = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image '{path}' (trying without alpha): {e}")
        try:
            # Jika convert_alpha gagal (misalnya format JPG), coba tanpa itu
            img = pygame.image.load(path).convert()
        except pygame.error as e2:
            print(f"Fatal error loading image '{path}': {e2}")
            # Kembalikan Surface placeholder jika gagal total
            placeholder = pygame.Surface(size if size else (50,50))
            placeholder.fill((255,0,255)) # Warna magenta untuk menandakan error
            return placeholder
            
    if size:
        try:
            img = pygame.transform.scale(img, size)
        except Exception as e_scale: # Menangkap exception yang lebih umum saat scaling
            print(f"Error scaling image '{path}' to {size}: {e_scale}")
            # Jika scaling gagal, kembalikan gambar asli jika ada, atau placeholder
            if img: return img
            placeholder = pygame.Surface(size if size else (50,50))
            placeholder.fill((255,0,255)) 
            return placeholder
    return img