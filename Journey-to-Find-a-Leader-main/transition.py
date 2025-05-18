import pygame

class Transition:
    def __init__(self, duration):
        self.duration = duration
        self.timer = 0
        self.active = False
        self.alpha = 0
        self.next_state = None

    def start(self, next_state):
        self.active = True
        self.timer = 0
        self.alpha = 0
        self.next_state = next_state

    def next_stage(self) :
        self.active = False
        self.timer = 0
        self.alpha = 0
        self.next_state = None

    def start_transition_to(self, target_state):
        self.transition.start(target_state)

    def update(self, dt):
        if self.active:
            self.timer += dt
            progress = min(1.0, self.timer / self.duration)
            self.alpha = int(progress * 255)
            if self.timer >= self.duration:
                self.active = False
                return self.next_state
        return None

    def draw(self, screen, color=(0, 0, 0)):
        if self.active:
            fade_surface = pygame.Surface(screen.get_size())
            fade_surface.fill(color)
            fade_surface.set_alpha(self.alpha)
            screen.blit(fade_surface, (0, 0))
