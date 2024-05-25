import pygame
from modules import sprites


class Player(sprites.Sprite):
    gravityValue = 5
    jumpForce = 10
    _jumpingTo = 0
    speed = 5
    _coins = 0

    def __init__(self, image_path,x,y,tag="Player"):
        super().__init__(image_path,x,y,tag)


    def update(self, entities):
       
        velocity = [0,0]

        
       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            velocity[0] -= self.speed
            super().playAnimation('run')
            super().flip(True,False)
        if keys[pygame.K_d]:
            velocity[0] += self.speed
            super().playAnimation('run')
            super().flip(False,False)
        
        if (velocity == [0,0]):
            super().playAnimation('idle')

         # affect gravity
        velocity[1] += self.gravityValue

        # check left and right
        canMove = True
        _isgrounded = False
        canJump = True
        prect = pygame.Rect((self.rect.x) + velocity[0],(self.rect.y) + velocity[1],self.rect.width,self.rect.height)
        for layer in entities.keys():
            for entity in entities[layer]:
                if entity.tag == "ground" and prect.colliderect(entity.rect):
                    # check down 
                    if (not _isgrounded and pygame.Rect((self.rect.x),(self.rect.y)+ velocity[1],self.rect.width,self.rect.height).colliderect(entity.rect)):
                        _isgrounded = True
                    # check up (so player can jump if it's clear)
                    if (canJump and pygame.Rect((self.rect.x),(self.rect.y) - self.gravityValue,self.rect.width,self.rect.height).colliderect(entity.rect)):
                        canJump = False
                    # check left and right
                    if (canMove and pygame.Rect((self.rect.x) + velocity[0],(self.rect.y),self.rect.width,self.rect.height).colliderect(entity.rect)):
                        canMove = False
                    
                    if (not canMove and _isgrounded and not canJump ):
                        break
                elif entity.tag == "money" and prect.colliderect(entity.rect):
                    self._coins += 1
                    pygame.mixer.Sound('assets/Music/pickupCoin.wav').play()
                    entities[layer].remove(entity)

        # jump
        if keys[pygame.K_w] and _isgrounded and canJump:
            self._jumpingTo = self.jumpForce
        
        # add jump force to velocity
        if (self._jumpingTo > 0 and canJump):
            self.move(0,-self.gravityValue)
            self._jumpingTo -= 1
        elif (not canJump): # cancel jumping if hit something
            self.move(0,self.gravityValue)
            self._jumpingTo = 0
        
        # add gravity to velocity if not jumping
        elif (not _isgrounded and self._jumpingTo <= 0):
            self.move(0,velocity[1])
        
        # move player
        if (canMove):
            self.move(velocity[0],0)
        
        pass

    def getEval(self):
        return super().getEval('Player')