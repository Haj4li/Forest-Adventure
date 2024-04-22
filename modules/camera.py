class Camera:
    _active = False
    _follow_last = (0,0)
    _centered = False
    def __init__(self,s_x,s_y):
        self._x = s_x
        self._y = s_y

    def Follow(self,follow):
        self._follow_last = (follow.x,follow.y)
        self._follow = follow
        self._active = True
        self._centered = False
    
    def UnFollow(self):
        self._active = False
        self._follow = None
        
    
    def IsFollowing(self):
        if (self._active and self._follow):
            return True
        return False
    
    def Update(self,entities):
        if (not self._active):
            return
        # center the camera
        if (not self._centered):
            self._follow_last = (self._x,self._y)
            self._centered = True
        
        moveto = [0,0]
        if (self._follow.x != self._follow_last[0] or self._follow.y != self._follow_last[1]):
            moveto = [self._follow.x - self._follow_last[0] , self._follow.y - self._follow_last[1]]
            
            for entity in entities:
                if (entity != self._follow):
                    entity.move(-moveto[0],-moveto[1])
            
            self._follow.x = self._follow_last[0]
            self._follow.y = self._follow_last[1]