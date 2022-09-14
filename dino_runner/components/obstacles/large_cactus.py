import random

from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import SCREEN_WIDTH


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325
        screen = 355
        screen.blit(self.image[self.obstacle_type], (self.rect.x, self.rect.y))


