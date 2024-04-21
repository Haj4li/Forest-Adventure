import pygame
from modules import sprites

class Player(sprites.Sprite):
    gravityValue = 5
    jumpForce = 20
    _jumpingTo = 0
    speed = 5

    def __init__(self, image_path,x,y,tag="Player"):
        super().__init__(image_path,x,y,tag)

    def update(self, entities):
        # affect gravity
        velocity = [0,0]

        velocity[1] += self.gravityValue
       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            velocity[0] -= self.speed
        if keys[pygame.K_d]:
            velocity[0] += self.speed
        
        

        # check left and right
        canMove = True
        _isgrounded = False
        prect = pygame.Rect((self.rect.x) + velocity[0],(self.rect.y) + velocity[1],self.rect.width,self.rect.height)
        for entity in entities:
            if entity.tag == "ground":
                if (prect.colliderect(entity.rect)):
                    _isgrounded = True
                    break
        
        if keys[pygame.K_w] and _isgrounded:
            self._jumpingTo = self.jumpForce
        
        if (self._jumpingTo > 0):
            self.move(0,-self.gravityValue)
            self._jumpingTo -= 1
        
        elif (not _isgrounded and self._jumpingTo <= 0):
            self.move(0,velocity[1])
        
        if (canMove):
            self.move(velocity[0],0)
        


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