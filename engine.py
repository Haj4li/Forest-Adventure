import pygame
import os

from modules.bats import Bat
from modules.sprites import *
from modules.player import Player
from modules.camera import Camera
from modules.clouds import Cloud
from modules.audio import *

class Game:
    _isRunning = True
    _totalRendered = 0
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
    _controlHeld = False
    _isInMenu = False


    _currentScene = 0

    _currentLayer = 0

    # camera handler

    # _entities list
    _entities = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
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
    
    def _initSprite(self,evalstring):
        evals = evalstring.split(';')
        cloned = eval(evals[0])
        for e in evals[1:]:
            eval(e)
        return cloned
    
    def _loadScene(self,scene_index):

        if (scene_index <= len(self._scenes)-1):
            self._currentScene = scene_index
            # clear entities
            self._entities.clear()
            self._entities = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
            # load new scene
            scenepath = self._scenes[scene_index]
            self._mainCamera.UnFollow()
            # check saved level
            if (os.path.exists(scenepath)):
                # load entities from level.lfa
                loadLevel = open(scenepath, "r").readlines()
                for line in loadLevel:
                    self._entities[0].append(self._initSprite(line))
        else:
            print(f"Error in loading scene {scene_index} .")
    
    def _start(self):
        # add game scenes
        self._scenes.append('level.lfa')
        self._scenes.append('level1.lfa')

        # add all entities to the editor entities if editing is enabled
        # self._editorModeEntities.append(Player("assets/fox.png",0,0))
        self._editorModeEntities.append(Sprite("assets/s1.png",0,0,"ground"))
        self._editorModeEntities.append(Sprite("assets/wall.png",0,0,"ground"))
        
        self._editorModeEntities.append(Sprite("assets/tree2.png",0,0,"tree"))
        treeAnimated = Sprite("assets/treeAnim.png",0,0,"tree")
        treeAnimated.setupSpritesheet(1,7)
        treeAnimated.addAnimation('idle',0,7,200,True)
        treeAnimated.playAnimation('idle')
        self._editorModeEntities.append(treeAnimated)

        self.uiCoin = pygame.image.load("assets/coin2.png")
        self.uiCoinImage = self.uiCoin.get_rect()
        self.uiCoinImage.x = self.screen_width - 50
        self.uiCoinImage.y = 50

        self._player_coins = 0
            
        self._editorModeEntities.append(Sprite("assets/coin.png",0,0,"money"))
        self._editorModeEntities.append(Sprite("assets/coin2.png",0,0,"money"))

        coinAnimated = Sprite("assets/coinAnim.png",0,0,"money")
        coinAnimated.setupSpritesheet(1,7)
        coinAnimated.addAnimation('idle',0,7,200,True)
        coinAnimated.playAnimation('idle')
        self._editorModeEntities.append(coinAnimated)
        self._editorModeEntities.append(Sprite("assets/cup.png",0,0,"win"))
        self._editorModeEntities.append(Sprite("assets/greeen.png",0,0,"object"))
        self._editorModeEntities.append(Sprite("assets/signleft.png",0,0,"object"))
        self._editorModeEntities.append(Sprite("assets/signright.png",0,0,"object"))
        self._editorModeEntities.append(Sprite("assets/mushroom.png",0,0,"object"))
        self._editorModeEntities.append(Sprite("assets/Rock.png",0,0,"ground"))

        # load audios
        play_audio('assets/Music/bgmusic.mp3',-1,0.8)


        # menu
        self._menubg = Sprite("assets/menu.png",0,0,'bg')
        self._mPlayButton = Sprite("assets/play.png",400,250,'button')
        self._mPlayButton.setupSpritesheet(2,1)
        self._mPlayButton.addAnimation('normal',0,1,1,False)
        self._mPlayButton.addAnimation('hover',1,1,1,False)



        self._editorModeEntities.append(Cloud("assets/cl.png",0,0))

        self._selectedSprite = self._editorModeEntities[0].clone()

        bat = Bat("assets/bat.png",0,0,"Bat")
        self._editorModeEntities.append(bat)

        character = Player("assets/character.png",200,200)
        character.setupSpritesheet(5,12)

        character.addAnimation('idle',0,11,25,True)
        character.addAnimation('run',1,12,25,True)
        character.addAnimation('fall',3,1,500,False)
        character.addAnimation('jump',4,1,500,False)

        character.playAnimation('idle')
        
        self._editorModeEntities.append(character)
        

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
        
        if (self._isInMenu):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._isRunning = False
                    return
        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._isRunning = False
                    return
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._editingLevelEnabled and event.button == 1: # add new entity to the game
                        self._mapSaved = False
                        self._entities[self._currentLayer].append(self._selectedSprite.clone())
                    elif self._editingLevelEnabled and event.button == 3: # remove hovering entity from the game
                        self._removeFlag = True
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_LCTRL):
                        self._controlHeld = True
                # handle user input
                elif event.type == pygame.KEYUP:
                    if (event.key == pygame.K_TAB): # change game mode (Game/Editor)
                        self._editingLevelEnabled = not self._editingLevelEnabled
                        if (self._editingLevelEnabled):
                            self._mainCamera.Follow(self._editorCam)
                        else:
                            self._mainCamera.UnFollow()
                    elif (event.key == pygame.K_r):
                        self._loadScene(self._currentScene)
                    elif (event.key == pygame.K_LCTRL):
                        self._controlHeld = False
                    elif (self._editingLevelEnabled and event.key == pygame.K_e): # select next entity editor mode 
                        self._entityIndex += 1
                        if (self._entityIndex >= len(self._editorModeEntities)):
                            self._entityIndex = 0
                        del self._selectedSprite
                        self._selectedSprite = self._editorModeEntities[self._entityIndex].clone()
                    elif (self._editingLevelEnabled and event.key == pygame.K_q): # select previus entity editor mode 
                        self._entityIndex -= 1
                        if (self._entityIndex < 0):
                            self._entityIndex = len(self._editorModeEntities)-1
                        del self._selectedSprite
                        self._selectedSprite = self._editorModeEntities[self._entityIndex].clone()
                    elif (event.key == pygame.K_DELETE and self._editingLevelEnabled): # clear the map 
                        self._entities.clear()
                        self._entities = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
                    elif (event.key == pygame.K_z): # Save the game
                        so = open("level.lfa",'w')
                        id = 0
                        for layer in self._entities.keys():
                            for entity in self._entities[layer]:
                                id +=1
                                so.write(f"{entity.getEval()}\n")
                        # todo: camera eval

                        self._mapSaved = True
                        so.close()


                    elif (event.key == pygame.K_1):
                        self._currentLayer = 0
                    elif (event.key == pygame.K_2):
                        self._currentLayer = 1
                    elif (event.key == pygame.K_3):
                        self._currentLayer = 2
                    elif (event.key == pygame.K_4):
                        self._currentLayer = 3
                    elif (event.key == pygame.K_5):
                        self._currentLayer = 4
                    elif (event.key == pygame.K_6):
                        self._currentLayer = 5
                    elif (event.key == pygame.K_7):
                        self._currentLayer = 6
                    elif (event.key == pygame.K_0):
                        self._loadScene(0)
                    elif (event.key == pygame.K_ESCAPE): # Escape the game
                        self._isRunning = False
                        return
        
            
            self._mousepos = pygame.Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

            # handle game conditions
            if (not self._editingLevelEnabled):
                # handle _entities update
                for layer in self._entities.keys():
                    for entity in self._entities[layer]:
                        if (entity.tag == "Player"):
                            entity.update(self._entities) # update player
                            self._player_coins = entity.coins
                            if (entity.grabbedCup):
                                self._loadScene(1)
                                entity.grabbedCup = False
                                return
                            if (not self._mainCamera.IsFollowing()): # update main camera if not following anything
                                self._mainCamera.Follow(entity.rect)
                        elif (entity.tag == "Bat"):
                            entity.update(self._entities) # update Bats
                        else:
                            entity.update()
            elif (self._editingLevelEnabled and self._selectedSprite != None):
                if (not self._mainCamera.IsFollowing()):
                    self._mainCamera.Follow(self._editorCam)
                self._updateCameraRect()
                # limit the position of mouse and selected sprite
                # due to the sprite rect
                if (self._controlHeld):
                    fixedPos = pygame.Vector2(int(self._mousepos.x / self._selectedSprite.rect.width)*self._selectedSprite.rect.width,int(self._mousepos.y / self._selectedSprite.rect.height)*self._selectedSprite.rect.height)
                else:
                    fixedPos = self._mousepos
                self._selectedSprite.setPosition(fixedPos)

            # Update the main Camera
            self._mainCamera.Update(self._entities)

    def _drawLog(self):
        enc = 0
        for layer in self._entities.keys():
            enc += len(self._entities[layer])
        text_render = self._font.render(f"Total Entities {enc}, Rendering {self._totalRendered} Loaded Images {len(images)} Mouse Pos {self._mousepos} ", True, (0,0, 0))
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

        text_render = self._font.render(f"Current Layer: {self._currentLayer}", True, (0,0, 0))
        text_rect = text_render.get_rect()
        text_rect.x = 50
        text_rect.y = 100
        self._screen.blit(text_render, text_rect)

        pass

    def _draw(self):
        # fill screen with white color
        self._screen.fill((109, 197, 209))
        if (not self._isInMenu):
            # draw _entities
            deleted = False
            screenRect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
            self._totalRendered = 0
            for layer in self._entities.keys():
                for entity in self._entities[layer]:
                    if (self._removeFlag == True and entity.rect.collidepoint(self._mousepos)) : # check hovering entity and remove it from list
                        self._removeFlag = False
                        deleted = True
                        self._entities[layer].remove(entity)
                    else:
                        if (entity.rect.colliderect(screenRect)):
                            self._totalRendered += 1
                            entity.draw(self._screen)
            
            if (deleted == False):
                self._removeFlag = False
            
            if (self._editingLevelEnabled):
                offset_y=self.screen_height-64
                for i in range(0,len(self._editorModeEntities)):
                    self._editorModeEntities[i].drawAt((i*32) + (5*i),offset_y,self._screen)


            if (self._selectedSprite != None and self._editingLevelEnabled):
                self._selectedSprite.draw(self._screen)

            self._screen.blit(self.uiCoin,self.uiCoinImage)
            text_render = self._font.render(f"{self._player_coins}", True, (0,0, 0))
            text_rect = text_render.get_rect()
            text_rect.x = self.screen_width - 75
            text_rect.y = 55
            self._screen.blit(text_render, text_rect)


            # draw logs
            if (self._loggingEnabled and self._editingLevelEnabled):
                self._drawLog()
        else:
            self._menubg.draw(self._screen)
            self._mPlayButton.draw(self._screen)
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
