import pygame

from modules import sprites
from modules import player


class Game:
    _isRunning = True
    _loggingEnabled = True
    _editingLevelEnabled = True
    _entityIndex = 0
    _selectedSprite = None
    _mousepos = pygame.Vector2(0,0)
    _font = None

    # camera handler

    # _entities list
    _entities = []

    def __init__(self, title, screen_width, screen_height):
        pygame.init()
        self._screen = pygame.display.set_mode((screen_width, screen_height))  ## pygame.FULLSCREEN
        pygame.display.set_caption(title)
        self._clock = pygame.time.Clock()
        self._font =pygame.font.Font(None, 15)
        pass

    def _start(self):
        # add sprites
        _player = player.Player("assets/fox.png",50,50)
        # _player.gravityValue = 0
        
        self._entities.append(_player)
        for i in range (10):
            self._entities.append(sprites.Sprite("assets/ground.png",i*64,500,"ground"))
        if (self._editingLevelEnabled):
            self._selectedSprite = self._entities[0].clone()
        pass

    def _update(self):
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._isRunning = False
                return
            elif self._editingLevelEnabled and event.type == pygame.MOUSEBUTTONDOWN:
                # TODO: fix this shit
                self._entities.append(self._selectedSprite.clone())
    
        # handle user input
        keys = pygame.key.get_pressed()
        self._mousepos = pygame.Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

        if (keys[pygame.K_TAB]):
            self._editingLevelEnabled = not self._editingLevelEnabled

        if keys[pygame.K_ESCAPE]:
            self._isRunning = False
            return
        if self._editingLevelEnabled and keys[pygame.K_e]: # next entity
            temp = self._entities[self._entityIndex]
            checkdup = True
            while (temp.tag == self._selectedSprite.tag and checkdup):
                self._entityIndex += 1
                if (self._entityIndex >= len(self._entities)):
                    self._entityIndex = 0
                    checkdup = False
                
                temp = self._entities[self._entityIndex]
            del self._selectedSprite

            self._selectedSprite = temp.clone()
                    
            
        if (not self._editingLevelEnabled):
            # handle _entities update
            for entity in self._entities:
                if (entity.tag == "Player"):
                    entity.update(self._entities)
                else:
                    entity.update()
    
        elif (self._editingLevelEnabled and self._selectedSprite != None):
            # limit the position of mouse and selected sprite
            # due to the sprite rect
            fixedPos = pygame.Vector2(int(self._mousepos.x / self._selectedSprite.rect.width)*self._selectedSprite.rect.width,int(self._mousepos.y / self._selectedSprite.rect.height)*self._selectedSprite.rect.height)
            self._selectedSprite.setPosition(fixedPos)

        # handle game conditions
        pass

    def _drawLog(self):
        text_render = self._font.render(f"Total Entities {len(self._entities)} Loaded Images {len(sprites.images)} Mouse Pos {self._mousepos}", True, (0,0, 0))
        text_rect = text_render.get_rect()
        text_rect.x = 50
        text_rect.y = 50
        self._screen.blit(text_render, text_rect)
        pass

    def _draw(self):
        # fill screen with white color
        self._screen.fill((255,255,255))

        # draw _entities
        for entity in self._entities:
            entity.draw(self._screen)
        if (self._selectedSprite != None):
            self._selectedSprite.draw(self._screen)
        # draw logs
        if (self._loggingEnabled):
            self._drawLog()

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        self._clock.tick(60)

    def _exit(self):
        pygame.quit()


    def Run(self):
        self._start()

        while(self._isRunning):
            self._draw()

            self._update()

        self._exit()
