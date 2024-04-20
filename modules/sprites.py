import pygame

images = {}

def LoadImage(path):
    global images
    if (path in images.keys()):
        return images[path]
    images[path] = pygame.image.load(path)
    return images[path]


class Sprite():
    def __init__(self, image_path, x,y,tag="NOTAGE"):
        global images
        if image_path in images.keys():
            self._image = images[image_path]
        else:
            images[image_path] = pygame.image.load(image_path)
            self._image = images[image_path]
        self.image = self._image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.center = (x, y)
        self.position = pygame.Vector2(x, y)
        self.tag = tag
    
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self._image, angle)

    def setPosition(self, position):
        self.rect.x = position.x
        self.rect.y = position.y
    
    def update(self, args=None):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy