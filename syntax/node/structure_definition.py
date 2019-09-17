# -*- coding:utf-8 -*-
from base import BaseNode

class StructureDefinitionNode(BaseNode):
    NAME = 'StructureDefinition'
    def __init__(self):
        BaseNode.__init__(self)
        self._node_name = self.NAME