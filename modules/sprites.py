import pygame

images = {}

def LoadImage(path):
    global images
    if (path in images.keys()):
        return images[path]
    images[path] = pygame.image.load(path)
    return images[path]

class Sprite():
    _animations = {}
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

        #animations
        self.current_animation = None
        self.current_frame_index = 0
        self.last_frame_update = pygame.time.get_ticks()
        self.playing_animation = False
        self.setupSpritesheet(1,1)
        self.current_row = 0

    def setupSpritesheet(self,total_rows,total_cols):
        self.rows = total_rows
        self.cols = total_cols
        self.frame_width = self.rect.width // self.cols
        self.frame_height = self.rect.height // self.rows

    def addAnimation(self, name, row, frames,speed, loop):
        self._animations[name] = (row, frames, speed, loop)

    def setAnimation(self,animation):
        self.current_animation = animation
        self.current_frame_index = 0
        self.last_frame_update = pygame.time.get_ticks()
        self.playing_animation = True
        self.current_row = self.current_animation[0]

    def playAnimation(self,name):
        if (name in self._animations):
            self.setAnimation(self._animations[name])


    def stopAnimation(self):
        self.playing_animation = False


    def rotate(self, angle):
        self.image = pygame.transform.rotate(self._image, angle)

    def setPosition(self, position):
        self.rect.x = position.x
        self.rect.y = position.y
    
    def update(self, args=None):
        pass

    def clone(self):
        cloned = type(self)(self._imgpath,self.rect.x,self.rect.y,self.tag)
        if (len(self._animations) > 0):
            for anims in self._animations.keys():
                cloned.addAnimation(anims,self._animations[anims][0],self._animations[anims][1],self._animations[anims][2],self._animations[anims][3])
            cloned.setAnimation(self.current_animation)
        return cloned

    def draw(self, surface):
        # check animation state
        if (self.playing_animation and self.current_animation != None): # play animation frames
            current_time = pygame.time.get_ticks()

            if current_time - self.last_frame_update > self.current_animation[2]:
                self.last_frame_update = current_time
                self.current_frame_index += 1

                if self.current_frame_index >= self.current_animation[1]:
                    if self.current_animation[3]:
                        self.current_frame_index = 0
                    else:
                        self.current_frame_index = len(self.frames) - 1
                        self.playing_animation = False

        frame = self.image.subsurface(pygame.Rect(self.current_frame_index*self.frame_width, self.current_row*self.frame_height, self.frame_width,self.frame_height)).convert_alpha()
        surface.blit(frame, self.rect)
    
    def drawAt(self, x, y,surface):
        surface.blit(self.image, pygame.Rect(x,y,self.rect.width,self.rect.height))
    

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def getEval(self):
        return f"Sprite('{self._imgpath}',{self.rect.x},{self.rect.y},'{self.tag}')"
