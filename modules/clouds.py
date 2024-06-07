import pygame
from modules import sprites
import random

class Cloud(sprites.Sprite):
    def __init__(self,image_path, start_pos,y,tag="cloud"):
        super().__init__(image_path,start_pos,y,tag)
        

    def _reset(self):
        self.rect.x = 850 + random.randint(0,300)
        self.rect.y = random.randint(0,50)

    def update(self):
        if (self.rect.x + self.rect.width < 0 ):
            self._reset()
        self.move(-1,0)
        
    def getEval(self):
        return super().getEval('Cloud')