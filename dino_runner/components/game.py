from calendar import c
from ctypes import sizeof
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.running = False
        self.score = 0
        self.death_count = 0

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.obstacle_manager.reset_obstacle()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((209, 189, 131))
        self.draw_background()
        self.draw_score()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score: {self.score} ', True, (0, 0, 0))
        text_rec = text.get_rect()
        text_rec.center = (1000,50)
        self.screen.blit(text, text_rec)
        """ font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score: {self.score} ', True, (0, 0, 0))
        self.generic_text(text, 1000, 50) """

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0 and self.game_speed < 700:
            self.game_speed += 5


    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill((207, 155, 3))
        half_screen_heigth = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.generic_text('Press any key to start...', half_screen_width -180, half_screen_heigth)
        else:
                
            self.screen.blit(ICON, (half_screen_width +80, half_screen_heigth -50))
            self.generic_text('GAME OVER :c', half_screen_width -150, half_screen_heigth -10)
            print(self.death_count)
            print(self.score)
            


        pygame.display.update()
        self.handle_events_on_menu()

    def generic_text(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        font = pygame.font.Font(FONT_STYLE, 30)
        self.text = font.render(self.text, True, (0, 0, 0))
        text_rec = self.text.get_rect()
        text_rec.center = (x, y)
        self.screen.blit(self.text, (self.x, self.y))

