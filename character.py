# character.py
import pygame

class Player:
    def __init__(self, image, start_pos, speed=5):
        self.image = image
        self.rect = image.get_rect(center=start_pos)
        self.speed = speed
        self.movement = {'up': False, 'down': False, 'left': False, 'right': False}

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP): self.movement['up'] = True
            if event.key in (pygame.K_s, pygame.K_DOWN): self.movement['down'] = True
            if event.key in (pygame.K_a, pygame.K_LEFT): self.movement['left'] = True
            if event.key in (pygame.K_d, pygame.K_RIGHT): self.movement['right'] = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_UP): self.movement['up'] = False
            if event.key in (pygame.K_s, pygame.K_DOWN): self.movement['down'] = False
            if event.key in (pygame.K_a, pygame.K_LEFT): self.movement['left'] = False
            if event.key in (pygame.K_d, pygame.K_RIGHT): self.movement['right'] = False

    def update(self, screen_size):
        dx = (self.movement['right'] - self.movement['left']) * self.speed
        dy = (self.movement['down'] - self.movement['up']) * self.speed
        self.rect.move_ip(dx, dy)

        self.rect.clamp_ip(pygame.Rect(0, 0, *screen_size))

    def draw(self, screen):
        screen.blit(self.image, self.rect)