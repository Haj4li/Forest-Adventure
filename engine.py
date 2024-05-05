import pygame
import os

from modules.sprites import *
from modules.player import Player
from modules.camera import Camera
from modules.clouds import Cloud

class Game:
    _isRunning = True
    _loggingEnabled = True
    _editingLevelEnabled = True
    _entityIndex = 0
    _selectedSprite = None
    _mousepos = pygame.Vector2(0,0)
    _font = None
    _removeFlag = False
    _mapSaved = False
    _editorCam = None
    _scenes = []

    # camera handler

    # _entities list
    _entities = []
    _editorModeEntities = []

    def __init__(self, title, screen_width, screen_height):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._screen = pygame.display.set_mode((screen_width, screen_height))  ## pygame.FULLSCREEN
        self._editorCam = pygame.Rect(screen_width/2, screen_height/2, 1,1)

        pygame.display.set_caption(title)
        self._clock = pygame.time.Clock()
        self._font =pygame.font.Font(None, 15)
        self._mainCamera = Camera(screen_width/2,screen_height/2)
        pass

    def _loadScene(self,scene_index):
        if (scene_index <= len(self._scenes)-1):
            # clear entities
            self._entities.clear()
            # load new scene
            scenepath = self._scenes[scene_index]
            # check saved level
            if (os.path.exists(scenepath)):
                # load entities from level.lfa
                loadLevel = open(scenepath, "r").readlines()
                for line in loadLevel:
                    self._entities.append(eval(line))
        else:
            print(f"Error in loading scene {scene_index} .")

    def _start(self):
        # add game scenes
        self._scenes.append('level1.lfa')
        self._scenes.append('level2.lfa')

        # add all entities to the editor entities if editing is enabled
        
        self._editorModeEntities.append(Player("assets/fox.png",0,0))
        self._editorModeEntities.append(Sprite("assets/s1.png",0,0,"ground"))
        
        self._editorModeEntities.append(Cloud("assets/cl.png",0,0))

        self._selectedSprite = self._editorModeEntities[0].clone()
        

    def _updateCameraRect(self):
        if (self._editingLevelEnabled):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self._editorCam.x -= 5
            elif keys[pygame.K_d]:
                 self._editorCam.x += 5
            elif keys[pygame.K_w]:
                 self._editorCam.y -= 5
            elif keys[pygame.K_s]:
                 self._editorCam.y += 5
            

    def _update(self):
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._isRunning = False
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                if self._editingLevelEnabled and event.button == 1: # add new entity to the game
                    self._mapSaved = False
                    self._entities.append(self._selectedSprite.clone())
                elif self._editingLevelEnabled and event.button == 3: # remove hovering entity from the game
                    self._removeFlag = True
            
            # handle user input
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_TAB): # change game mode (Game/Editor)
                    self._editingLevelEnabled = not self._editingLevelEnabled
                    if (self._editingLevelEnabled):
                        self._mainCamera.Follow(self._editorCam)
                    else:
                        self._mainCamera.UnFollow()

                elif (self._editingLevelEnabled and event.key == pygame.K_e): # select next entity editor mode 
                    self._entityIndex += 1
                    if (self._entityIndex >= len(self._editorModeEntities)):
                        self._entityIndex = 0
                    del self._selectedSprite
                    self._selectedSprite = self._editorModeEntities[self._entityIndex].clone()
                elif (event.key == pygame.K_DELETE and self._editingLevelEnabled): # clear the map 
                    self._entities.clear()
                elif (event.key == pygame.K_z): # Save the game
                    so = open("level.lfa",'w')
                    id = 0
                    for entity in self._entities:
                        id +=1
                        so.write(f"{entity.getEval()} # entity # {id}\n")
                    self._mapSaved = True
                    so.close()
                elif (event.key == pygame.K_1):
                    self._loadScene(0)
                elif (event.key == pygame.K_2):
                    self._loadScene(1)
                elif (event.key == pygame.K_ESCAPE): # Escape the game
                    self._isRunning = False
                    return
    
        
        self._mousepos = pygame.Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

        # handle game conditions
        if (not self._editingLevelEnabled):
            # handle _entities update
            for entity in self._entities:
                if (entity.tag == "Player"):
                    entity.update(self._entities) # update player
                    if (not self._mainCamera.IsFollowing()): # update main camera if not following anything
                        self._mainCamera.Follow(entity.rect)
                else:
                    entity.update()
        elif (self._editingLevelEnabled and self._selectedSprite != None):
            if (not self._mainCamera.IsFollowing()):
                self._mainCamera.Follow(self._editorCam)
            self._updateCameraRect()
            # limit the position of mouse and selected sprite
            # due to the sprite rect
            fixedPos = pygame.Vector2(int(self._mousepos.x / self._selectedSprite.rect.width)*self._selectedSprite.rect.width,int(self._mousepos.y / self._selectedSprite.rect.height)*self._selectedSprite.rect.height)
            self._selectedSprite.setPosition(fixedPos)

        # Update the main Camera
        self._mainCamera.Update(self._entities)

    def _drawLog(self):
        text_render = self._font.render(f"Total Entities {len(self._entities)} Loaded Images {len(images)} Mouse Pos {self._mousepos}", True, (0,0, 0))
        text_rect = text_render.get_rect()
        text_rect.x = 50
        text_rect.y = 50
        self._screen.blit(text_render, text_rect)
        if (self._mapSaved):
            text_render = self._font.render(f"Map Saved !", True, (0,0, 0))
        else:
            text_render = self._font.render(f"Map has not Saved.", True, (0,0, 0))
        text_rect = text_render.get_rect()
        text_rect.x = 50
        text_rect.y = 75
        self._screen.blit(text_render, text_rect)
        pass

    def _draw(self):
        # fill screen with white color
        self._screen.fill((255,255,255))


        # draw _entities
        for entity in self._entities:
            if (self._removeFlag == True and entity.rect.collidepoint(self._mousepos)) : # check hovering entity and remove it from list
                self._removeFlag = False
                self._entities.remove(entity)
            else:
                entity.draw(self._screen)

        offset_y=self.screen_height-64
        for i in range(0,len(self._editorModeEntities)):
            self._editorModeEntities[i].drawAt((i*32) + (5*i),offset_y,self._screen)


        if (self._selectedSprite != None and self._editingLevelEnabled):
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
