import pygame

import hashlib

def calculate_md5(data):
    # Create an instance of the MD5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the data
    if isinstance(data, str):
        data = data.encode()  # Convert string to bytes
    md5_hash.update(data)

    # Get the hexadecimal representation of the hash
    hex_digest = md5_hash.hexdigest()

    return hex_digest

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
        self._imgpath = image_path
        if image_path in images.keys():
            self._image = images[image_path]
        else:
            images[image_path] = pygame.image.load(image_path)
            self._image = images[image_path]
        self.image = self._image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = pygame.Vector2(x, y)
        self.tag = tag

        self.hash = calculate_md5(image_path)
    
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self._image, angle)

    def setPosition(self, position):
        self.rect.x = position.x
        self.rect.y = position.y
    
    def update(self, args=None):
        pass

    def clone(self):
        return type(self)(self._imgpath,self.rect.x,self.rect.y,self.tag)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def getEval(self):
        return f"Sprite('{self._imgpath}',{self.rect.x},{self.rect.y},'{self.tag}')"