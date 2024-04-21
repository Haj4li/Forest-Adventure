import pygame
import os
from modules.sprites import *
from modules.player import Player


class Game:
    _isRunning = True
    _loggingEnabled = True
    _editingLevelEnabled = True
    _entityIndex = 0
    _selectedSprite = None
    _mousepos = pygame.Vector2(0,0)
    _font = None
    _removeFlag = False

    # camera handler

    # _entities list
    _entities = []
    _editorModeEntities = { }

    def __init__(self, title, screen_width, screen_height):
        pygame.init()
        self._screen = pygame.display.set_mode((screen_width, screen_height))  ## pygame.FULLSCREEN
        pygame.display.set_caption(title)
        self._clock = pygame.time.Clock()
        self._font =pygame.font.Font(None, 15)
        self._entityKeys = self._editorModeEntities.keys()
        pass

    def _addEntity(self, entity):
        if (not entity.hash in self._entityKeys):
            self._editorModeEntities[entity.hash] = entity.clone()
            self._entityKeys = self._editorModeEntities.keys()
            if (self._loggingEnabled):
                print(f"Entity {entity.hash} added to editor")

        self._entities.append(entity)


    def _start(self):
        # TODO: seprate editing entities from other
        # TODO: remove entities with right click
        # TODO: remove add entity function 
        # check saved level
        if (os.path.exists("level.lfa")):
            # load entities from level.lfa
            loadLevel = open("level.lfa", "r").readlines()
            for line in loadLevel:
                self._addEntity(eval(line))
        else:
            # add sprites
            _player = Player("assets/fox.png",50,50)
            # _player.gravityValue = 0
            
            self._addEntity(_player)
            for i in range (10):
                self._addEntity(Sprite("assets/ground.png",i*64,500,"ground"))
            
        if (self._editingLevelEnabled):
            self._selectedSprite = self._entities[0].clone()
        pass

    def _update(self):
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._isRunning = False
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                if self._editingLevelEnabled and event.button == 1:
                    self._addEntity(self._selectedSprite.clone())
            
            # handle user input
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_TAB): # change game mode (Game/Editor)
                    self._editingLevelEnabled = not self._editingLevelEnabled
                elif (self._editingLevelEnabled and event.key == pygame.K_e): # select next entity editor mode 
                    self._entityIndex += 1
                    keys = list(self._editorModeEntities.keys())
                    if (self._entityIndex >= len(keys)):
                        self._entityIndex = 0
                    values = list(self._editorModeEntities.values())
                    del self._selectedSprite
                    self._selectedSprite = values[self._entityIndex].clone()
                elif (event.key == pygame.K_F1): # Save the game
                    so = open("level.lfa",'w')
                    id = 0
                    for entity in self._entities:
                        id +=1
                        so.write(f"{entity.getEval()} # entity # {id}\n")
                    so.close()
                elif (event.key == pygame.K_ESCAPE): # Escape the game
                    self._isRunning = False
                    return
    
        
        self._mousepos = pygame.Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                    
        if (not self._editingLevelEnabled):
            # handle _entities update
            for entity in self._entities:
                if (entity.tag == "Player"):
                    entity.update(self._entities)
                else:
                    entity.update()
    
        elif (self._editingLevelEnabled and self._selectedSprite != None):
            self._removeFlag = False
            # limit the position of mouse and selected sprite
            # due to the sprite rect
            fixedPos = pygame.Vector2(int(self._mousepos.x / self._selectedSprite.rect.width)*self._selectedSprite.rect.width,int(self._mousepos.y / self._selectedSprite.rect.height)*self._selectedSprite.rect.height)
            self._selectedSprite.setPosition(fixedPos)

        # handle game conditions
        pass

    def _drawLog(self):
        text_render = self._font.render(f"Total Entities {len(self._entities)} Loaded Images {len(images)} Mouse Pos {self._mousepos}", True, (0,0, 0))
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
