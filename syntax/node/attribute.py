# -*- coding:utf-8 -*-
from branch import BranchNode

class AttributeNode(BranchNode):
    NAME = 'Attribute'
    def __init__(self):
        BranchNode.__init__(self)
        self._node_name = self.NAME 