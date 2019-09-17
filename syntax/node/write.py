# -*- coding:utf-8 -*-

from base import BaseNode

class WriteNode(BaseNode):
    
    NAME = 'Write'
    
    def __init__(self, new_line, text_node):
        BaseNode.__init__(self)
        self._node_name = self.NAME
        self.new_line = new_line
        self.text_node = text_node