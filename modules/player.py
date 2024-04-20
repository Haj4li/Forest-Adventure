import pygame
from modules import sprites

class Player(sprites.Sprite):
    gravityValue = 8
    speed = 5
    _isgrounded = False

    def __init__(self, image_path,x,y):
        super().__init__(image_path,x,y,"Player")

    def update(self, entities):
        # affect gravity
        velocity = [0,0]

        velocity[1] += self.gravityValue
       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            velocity[0] -= self.speed
        if keys[pygame.K_d]:
            velocity[0] += self.speed
        if keys[pygame.K_w] and self._isgrounded:
            velocity[1] -= self.gravityValue

        # check left and right
        canMove = True
        prect = pygame.Rect((self.rect.x + self.rect.width/2) + velocity[0],(self.rect.y + self.rect.height/2) + velocity[1],1,1)
        for entity in entities:
            if entity.tag == "ground":
                if (prect.colliderect(entity.rect)):
                    self._isgrounded = True
                    canMove = False
                    break
        if (canMove):
            self.move(velocity[0],velocity[1])
        


        # get keyboard values
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_d]:
        #     self.move(self.speed,0)
        # elif keys[pygame.K_a]:
        #     self.move(-self.speed,0)

        # if keys[pygame.K_w]:
        #     self.move(0,-8)

        pass
    
    def draw(self, surface):
        super().draw(surface)