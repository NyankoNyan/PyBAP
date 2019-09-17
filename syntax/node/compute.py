# -*- coding:utf-8 -*-
from base import BaseNode

class ComputeNode(BaseNode):
    NAME = 'Compute'
    def __init__(self, target_list, result):
        BaseNode.__init__(self)
        self._node_name = self.NAME
        self.target_list = target_list
        self.result = result
