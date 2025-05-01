import pygame
import sys

class Button:
    TEXT_COLOR = (255, 255, 255)

    def __init__(self, text, x, y, width, height, color, hover_color, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = font
        self.action = action
        self.is_hovered = False
        self.text_surf = self.font.render(self.text, True, self.TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        surface.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:
                if self.action:
                    self.action()
                    return True
        return False

class Game:
    #CONSTANTS
    BG_COLOR = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    BUTTON_COLOR = (50, 50, 50)
    BUTTON_HOVER_COLOR = (70, 70, 70)
    TITLE_COLOR = (10, 10, 50)

    FONT_SIZE_LARGE = 60
    FONT_SIZE_MEDIUM = 30
    FONT_SIZE_SMALL = 20

    STATE_MAIN_MENU = "main_menu"
    STATE_PLAYING = "playing"

    PLAYER_SPEED = 5

    def __init__(self):
        pygame.init()

        self.screen_width = 1000
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Journey to Find a Leader')

        self.clock = pygame.time.Clock()

        self._load_fonts()
        self._load_images()
        
        
        self.game_state = self.STATE_MAIN_MENU

        if self.img:
            img_width = self.img.get_width()
            img_height = self.img.get_height()
            self.img_pos = [self.screen_width // 2 - img_width // 2,
                            self.screen_height // 2 - img_height // 2]
            self.img_rect = self.img.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        else:
            self.img_pos = [self.screen_width // 2 - 25, self.screen_height // 2 - 25]
            self.img_rect = pygame.Rect(self.img_pos[0], self.img_pos[1], 50, 50)

        self.movement = {'up': False, 'down': False, 'left': False, 'right': False}

        self._create_buttons()

    def _load_fonts(self):
            self.large_font = pygame.font.Font(None, self.FONT_SIZE_LARGE)
            self.medium_font = pygame.font.Font(None, self.FONT_SIZE_MEDIUM)
            self.small_font = pygame.font.Font(None, self.FONT_SIZE_SMALL)
            self.title_font = pygame.font.Font(None, self.FONT_SIZE_LARGE + 10)

    def _load_images(self):
        image_path = "data/images/entities/bimas.png"
        loaded_image = pygame.image.load(image_path)
        self.img = loaded_image.convert_alpha()
       
        bg_image_path = "data/images/entities/maps.png"
        loaded_bg_image = pygame.image.load(bg_image_path).convert()
        self.bg_image = pygame.transform.scale(loaded_bg_image, (self.screen_width, self.screen_height))
    
    def _create_buttons(self):
        btn_width = 200
        btn_height = 50
        btn_spacing = 20

        total_btn_height = (btn_height * 2) + btn_spacing
        start_y = (self.screen_height - total_btn_height) // 2 + 50
        btn_x = (self.screen_width - btn_width) // 2

        self.play_button = Button(
            text="Play Game",
            x=btn_x, y=start_y,
            width=btn_width, height=btn_height,
            color=self.BUTTON_COLOR, hover_color=self.BUTTON_HOVER_COLOR,
            font=self.medium_font,
            action=self.start_game
        )
        self.exitButton = Button(
            text="Exit",
            x=btn_x, y=start_y + btn_height + btn_spacing,
            width=btn_width, height=btn_height,
            color=self.BUTTON_COLOR, hover_color=self.BUTTON_HOVER_COLOR,
            font=self.medium_font,
            action=self.quit_game
        )

        self.mainMenu_btn = [self.play_button, self.exitButton]
        self.ingame_buttons = []

    def start_game(self):
        print("Starting game...")
        self.game_state = self.STATE_PLAYING

        if self.img:
             self.img_rect.center = (self.screen_width // 2, self.screen_height // 2)
        else:
             self.img_rect.center = (self.screen_width // 2, self.screen_height // 2)

        self.movement = {'up': False, 'down': False, 'left': False, 'right': False}

    def quit_game(self):
        print("Exiting game..")
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if self.game_state == self.STATE_MAIN_MENU:
                for button in self.mainMenu_btn:
                    button.handle_event(event)
            elif self.game_state == self.STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.movement['up'] = True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.movement['down'] = True
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.movement['left'] = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.movement['right'] = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.movement['up'] = False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.movement['down'] = False
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.movement['left'] = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.movement['right'] = False

    def _update(self):
        if self.game_state == self.STATE_PLAYING:
            posisi_x = 0
            posisi_y = 0
            if self.movement['up']:
                posisi_y -= self.PLAYER_SPEED
            if self.movement['down']:
                posisi_y += self.PLAYER_SPEED
            if self.movement['left']:
                posisi_x -= self.PLAYER_SPEED
            if self.movement['right']:
                posisi_x += self.PLAYER_SPEED

            self.img_rect.x += posisi_x
            self.img_rect.y += posisi_y

            if self.img_rect.left < 0:
                self.img_rect.left = 0
            if self.img_rect.right > self.screen_width:
                self.img_rect.right = self.screen_width
            if self.img_rect.top < 0:
                self.img_rect.top = 0
            if self.img_rect.bottom > self.screen_height:
                self.img_rect.bottom = self.screen_height

    def _draw(self):
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill(self.BG_COLOR)

        if self.game_state == self.STATE_MAIN_MENU:
            title_surf = self.title_font.render('Journey to Find a Leader', True, self.TITLE_COLOR)
            title_rect = title_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
            self.screen.blit(title_surf, title_rect)

            for button in self.mainMenu_btn:
                button.draw(self.screen)

        elif self.game_state == self.STATE_PLAYING:
            if self.img:
                self.screen.blit(self.img, self.img_rect) 
            else:
                pygame.draw.rect(self.screen, self.GRAY, self.img_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()