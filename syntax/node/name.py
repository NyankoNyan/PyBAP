# -*- coding:utf-8 -*-
from leaf import LeafNode

class NameNode(LeafNode):
    NAME = 'Name'
    def __init__(self, name):
        LeafNode.__init__(self)
        self._node_name = self.NAME
        self.name = name