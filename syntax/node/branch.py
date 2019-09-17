# -*- coding:utf-8 -*-
from base import BaseNode

class BranchNode(BaseNode):
    
    def __init__(self):
        BaseNode.__init__(self)
        self._subnode_list = []
        self._sub_count = 0
        
    def get_nodes(self):
        return self._subnode_list
