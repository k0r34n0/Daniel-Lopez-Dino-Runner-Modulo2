from calendar import c
from ctypes import sizeof
from distutils import core
from time import time
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles import obstacle_manager
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

from dino_runner.utils.constants import BG, DEFAULT_TYPE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE


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
        self.power_up_manager = PowerUpManager()
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
        self.reset_game()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                self.score = 0

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((209, 189, 131))
        self.draw_background()
        self.draw_score()
        self.draw_power_up_time()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
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
        text = f'Score: {self.score} '
        coords = (900,50)
        self.generic_text(text, coords)
        """ font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score: {self.score} ', True, (0, 0, 0))
        self.generic_text(text, 1000, 50) """

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks())/ 1000, 2) 
            if time_to_show >= 0:
                font = pygame.font.Font(FONT_STYLE, 30)
                text = f'{self.player.type.capitalize()} enabled for {time_to_show} seconds'
                coords = (300, 50)
                self.generic_text(text, coords)
            else:
                self.has_power_up = False
                self.player.type = DEFAULT_TYPE

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
            self.generic_text('Press any key to start...', (half_screen_width -180, half_screen_heigth))
        else:
            self.screen.blit(ICON, (half_screen_width -40, half_screen_heigth -50))
            self.generic_text('GAME OVER :c', (half_screen_width -100, half_screen_heigth -100))
            self.generic_text('Press any key to try again...', (half_screen_width -180, half_screen_heigth -150))
            self.draw_score_death()
            self.draw_death_count()
                

        pygame.display.update()
        self.handle_events_on_menu()

    def draw_score_death(self):
        text = f'Score: {self.score} '
        coords = (800,50)
        self.generic_text(text, coords)

    def draw_death_count(self):
        text = f'Your deaths count is: {self.death_count} '
        coords = (80,50)
        self.generic_text(text, coords)

    def generic_text(self, text, coords):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(text, True, (0, 0, 0))
        text_rec = text.get_rect()
        text_rec.center = (coords)
        self.screen.blit(text, coords)

    def reset_game(self):
        self.score = 0
        self.game_speed = 20
        self.obstacle_manager.reset_obstacle()
        self.power_up_manager.reset_power_ups()

