# -*- coding:utf-8 -*-


class GUIBaseFront():
    
    def __init__(self):
        pass
    
    def sync(self):
        pass
    
class GUIBaseBack():
    
    def __init__(self):
        self._front = None
    
    def sync(self):
        pass
    
    def set_front(self, front):
        self._front = front