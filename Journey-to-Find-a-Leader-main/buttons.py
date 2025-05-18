import pygame

class Button:
    
    def __init__(self, image_normal, x, y, action=None, image_hover=None):
        
        self.image_normal = image_normal
        self.image_hover = image_hover if image_hover is not None else image_normal
        self.action = action

        self.rect = self.image_normal.get_rect()
        self.rect.topleft = (x, y)

        self.is_hovered = False

    def draw(self, surface):
        current_image = self.image_hover if self.is_hovered else self.image_normal
        surface.blit(current_image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                self.action()  
                return True    
        return False