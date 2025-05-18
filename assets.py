import pygame

def load_image(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except pygame.error as e:
        print(f"Error loading image '{path}': {e}")
        return None
