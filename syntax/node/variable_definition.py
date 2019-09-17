# -*- coding:utf-8 -*-

from base import BaseNode


class VariableDefinitionNode(BaseNode):
    NAME = 'VariableDefinition'
    LIKE = 1
    TYPE = 2    
    
    def __init__(self, name, length, decimals, value, reftype, typename):
        BaseNode.__init__(self)
        self._node_name = self.NAME
        self.name = name
        self.length = length
        self.decimals = decimals
        self.value = value
        self.reftype = reftype
        self.typename = typename
