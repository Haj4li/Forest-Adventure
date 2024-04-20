import pygame

from modules import sprites
from modules import player


class Game:
    _isRunning = True

    # camera handler

    # _entities list
    _entities = []

    def __init__(self, title, screen_width, screen_height):
        pygame.init()
        self._screen = pygame.display.set_mode((screen_width, screen_height))  ## pygame.FULLSCREEN
        pygame.display.set_caption(title)
        self._clock = pygame.time.Clock()
        pass

    def _start(self):
        # add sprites
        _player = player.Player("assets/fox.png",50,50)
        # _player.gravityValue = 0
        self._entities.append(_player)
        for i in range (10):
            self._entities.append(sprites.Sprite("assets/ground.png",i*64,500,"ground"))
        
        pass

    def _update(self):
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._isRunning = False
                return
        # handle user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self._isRunning = False
            return
        # handle _entities update
        for entity in self._entities:
            if (entity.tag == "Player"):
                entity.update(self._entities)
            else:
                entity.update()

        # handle game conditions
        pass

    def _draw(self):
        # fill screen with white color
        self._screen.fill((255,255,255))

        # draw _entities
        for entity in self._entities:
            entity.draw(self._screen)

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








