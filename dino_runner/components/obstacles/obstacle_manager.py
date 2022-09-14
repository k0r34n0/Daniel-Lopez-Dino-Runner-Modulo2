import pygame

from dino_runner.utils.constants import SCREEN_WIDTH, SMALL_CACTUS, LARGE_CACTUS
from dino_runner.components.obstacles.small_cactus import SmallCactus
from dino_runner.components.obstacles.large_cactus import LargeCactus



class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            small_cactus = SmallCactus(SMALL_CACTUS)
            large_cactus = LargeCactus(LARGE_CACTUS)
            self.obstacles.append(small_cactus)
            self.obstacles.append(large_cactus)


        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                print("collition")
                pygame.time.delay(1000)
                game.playing = False
                break


    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)