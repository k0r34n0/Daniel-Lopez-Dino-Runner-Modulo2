import pygame
import random
from dino_runner.components.obstacles.cactus import Cactus

from dino_runner.utils.constants import BIRD, SCREEN_WIDTH, SMALL_CACTUS, LARGE_CACTUS
from dino_runner.components.obstacles.bird import Bird
"""  if len(self.obstacles) == 0:
            cactus_type = 'SMALL' if random.randint(0,1) == 0 else 'LARGE'
            cactus = Cactus(cactus_type)
            self.obstacles.append(cactus) """



class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0,2) == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS, 325))

            elif random.randint(0,2) == 1:
                self.obstacles.append(Cactus(LARGE_CACTUS, 300))

            elif random.randint(0,2) == 2:
                self.obstacles.append(Bird(BIRD))
        

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                print("collition")
                pygame.time.delay(1000)
                game.death_count += 1
                game.score = 0
                game.game_speed = 20
                game.playing = False
                break


    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacle(self):
        self.obstacles = []