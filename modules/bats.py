import pygame
from modules import sprites


class Bat(sprites.Sprite):
    speed = 3
    maxmoves = 200


    def __init__(self, image_path,x,y,tag="Bat"):
        super().__init__(image_path,x,y,tag)
        self._movingDirection = 'right'
        self._currentMoves = 0
        self.maxright = 0
        self.maxleft = 0



    def update(self, entities):
       
        velocity = [0,0]

        self._currentMoves +=1
        if (self._currentMoves >= self.maxmoves):
            if (self._movingDirection == 'right'):
                self._movingDirection = 'left'
                self.maxright = self._currentMoves
            else:
                self._movingDirection = 'right'
                self.maxleft = self._currentMoves
            self._currentMoves =0
        
        predicted = False
        if (self.maxleft != 0 and self._movingDirection == 'left'):
            predicted = True
            if (self._currentMoves >= self.maxleft ):
                self._movingDirection = 'right'
                self._currentMoves =0
        elif (self.maxright != 0 and self._movingDirection == 'right'):
            predicted = True
            if (self._currentMoves >= self.maxright):
                self._movingDirection = 'left'
                self._currentMoves =0

        if (self._movingDirection == 'right'):
            velocity[0] += self.speed
        else:
            velocity[0] -= self.speed

        if (not predicted):
            # check left and right
            breaked = False
            for layer in entities.keys():
                if (breaked):
                    break
                for entity in entities[layer]:
                    if entity.tag == "ground" and self.rect.colliderect(entity.rect):
                        if (pygame.Rect((self.rect.x) + velocity[0],(self.rect.y),self.rect.width,self.rect.height).colliderect(entity.rect)):
                            if (self._movingDirection == 'right'):
                                self._movingDirection = 'left'
                                velocity[0] -= self.speed*2
                            else:
                                self._movingDirection = 'right'
                                velocity[0] += self.speed*2
                            self._currentMoves =0
                            breaked = False
                            break
        

        self.move(velocity[0],0)

        
        pass

    def getEval(self):
        return super().getEval('Bat')