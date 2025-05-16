import pygame

class Subtitle:
    def __init__(self, screen, font=None, font_size=36, text_color=(0,0,0), y_offset=50, typing_speed=35):
        self.screen = screen
        self.font = pygame.font.Font("data/fonts/dogicapixelbold.otf", 21)
        self.text_color = text_color
        self.y_offset = 140
        self.typing_speed = typing_speed

        self.reset()

    def reset(self):
        self.text = ""
        self.typed_text = ""
        self.char_index = 0
        self.last_char_time = pygame.time.get_ticks()
        self.finished = False

    def show(self, text):
        self.reset()
        self.text = text

    def update(self):
        if self.char_index < len(self.text):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_char_time >= self.typing_speed:
                self.typed_text += self.text[self.char_index]
                self.char_index += 1
                self.last_char_time = current_time
        else:
            self.finished = True

    def draw(self):
        rendered_text = self.font.render(self.typed_text, True, self.text_color)
        text_rect = rendered_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - self.y_offset))
        self.screen.blit(rendered_text, text_rect)
