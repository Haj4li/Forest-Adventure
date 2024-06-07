import pygame
from modules import sprites


class Player(sprites.Sprite):
    gravityValue = 5
    grabbedCup = False
    jumpForce = 20
    _jumpingTo = 0
    _jumped = False
    _doubleJumped = False
    speed = 5
    coins = 0
    health = 3
    isDead = False
    _invinsible = 0

    def __init__(self, image_path,x,y,tag="Player"):
        super().__init__(image_path,x,y,tag)
    def draw(self,screen,position = None):
        if (self._invinsible <= 0):
            super().draw(screen,position)
        else:
            self._invinsible -= 1
            if (self._invinsible % 10 == 0):
                super().draw(screen,position)

    
    def update(self, entities):
        if (self.isDead):
            return
       
        velocity = [0,0]

        
       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            velocity[0] -= self.speed
            super().playAnimation('run')
            super().flip(True,False)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
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
        breaked = False
        fixedRect = pygame.Rect((self.rect.x + 12),(self.rect.y),self.rect.width-24,self.rect.height)
        prect = pygame.Rect(fixedRect.x + velocity[0],fixedRect.y + velocity[1],fixedRect.width,fixedRect.height)
        for layer in entities.keys():
            if (breaked):
                break
            for entity in entities[layer]:
                if entity.tag == "ground" and prect.colliderect(entity.rect):
                    # check down 
                    if (not _isgrounded and pygame.Rect(fixedRect.x,fixedRect.y+ velocity[1],fixedRect.width,fixedRect.height).colliderect(entity.rect)):
                        _isgrounded = True
                        self._doubleJumped = False
                    # check up (so player can jump if it's clear)
                    if (canJump and pygame.Rect(fixedRect.x,fixedRect.y - self.gravityValue,fixedRect.width,fixedRect.height).colliderect(entity.rect)):
                        canJump = False
                    # check left and right
                    if (canMove and pygame.Rect(fixedRect.x + velocity[0],fixedRect.y,fixedRect.width,fixedRect.height).colliderect(entity.rect)):
                        canMove = False
                    
                    if (not canMove and _isgrounded and not canJump ):
                        breaked = True
                        break
                elif entity.tag[:5] == "money" and prect.colliderect(entity.rect):
                    self.coins += int(entity.tag[5:])
                    pygame.mixer.Sound('assets/Music/pickupCoin.wav').play()
                    entities[layer].remove(entity)
                elif entity.tag == "Bat" and prect.colliderect(entity.rect) and self._invinsible <= 0:
                    self._invinsible = 200
                    self.health -= 1
                    if (self.health <= 0):
                        print("Is dead")
                        self.isDead = True
                    pygame.mixer.Sound('assets/Music/pickupCoin.wav').play()
                    entities[layer].remove(entity)
                elif entity.tag == "win" and prect.colliderect(entity.rect):
                    self.grabbedCup = True

        # jump
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (_isgrounded and canJump):
            self._jumpingTo = self.jumpForce

        
        # add jump force to velocity
        if (self._jumpingTo > 0 and canJump):
            
            super().playAnimation('jump')
            self.move(0,-self.gravityValue)
            self._jumpingTo -= 1
        elif (not canJump): # cancel jumping if hit something
            self.move(0,self.gravityValue)
            self._jumpingTo = 0
        
        # add gravity to velocity if not jumping
        elif (not _isgrounded and self._jumpingTo <= 0):
            super().playAnimation('fall')
            self.move(0,velocity[1])
        
        # move player
        if (canMove):
            self.move(velocity[0],0)

        if (self.rect.y >= 650):
            self.isDead = True
        
        pass

    def getEval(self):
        return super().getEval('Player')