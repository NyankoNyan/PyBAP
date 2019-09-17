# -*- coding:utf-8 -*-
from base import GUIBaseBack, GUIBaseFront


class WriteLogBack(GUIBaseBack):
    
    LINE = '--------------------------------------------------'
    
    def __init__(self):
        GUIBaseBack.__init__(self)
        self._initialized = False
        self._str_buff = []
        self._new_str = ''
        self._header_out = False
        self._prog_descr = ''
        self._screen_width = 80
        
    def sync(self):
        GUIBaseBack.sync(self)
        self.__send_new_str(skip_empty=True)
        if len(self._str_buff) > 0:
            if not self._initialized:
                self._initialized = True
                if self._header_out:
                    temp_buff = self._str_buff[:]
                    del self._str_buff[:]
                    self.write(
                        text=self._prog_descr,
                        newline=True,
                        )
                    self.write(
                        text=self.LINE,
                        newline=True
                        )
                    self.__send_new_str(skip_empty=True)
                    self._str_buff += temp_buff
                    del temp_buff[:]
            self._front.send(self._str_buff)
            del self._str_buff[:]         
        
        
    def set_screen_width(self, width):
        assert width > 0
        self._screen_width = width
        
    def set_prog_descr(self, descr):
        self._prog_descr = descr
        
    def set_pf_title(self, descr):
        self._prog_descr = descr
        
    def set_header_out(self, header_out):
        self._header_out = header_out
        
    def write(self, text='', newline=False):
        if newline:
            self.__send_new_str(skip_empty=True)
        if len(self._new_str) == 0:
            self._new_str = text
        else:
            self._new_str += ' ' + text
        if len(self._new_str) > self._screen_width:
            del self._new_str[self._screen_width:]
            
    def __send_new_str(self, skip_empty=False):
        if not skip_empty or len(self._new_str) > 0:
            self._str_buff.append(self._new_str)
            self._new_str = ''
    
    
class WriteLogFront(GUIBaseFront):
    
    def __init__(self):
        GUIBaseFront.__init__(self)
    
    def sync(self):
        GUIBaseFront.sync(self)
        
    def send(self, str_buff):
        for line in str_buff:
            print line
        