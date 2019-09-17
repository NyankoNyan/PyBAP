# -*- coding:utf-8 -*-

from base import BaseNode


class TableDefinitionNode(BaseNode):
    NAME = 'TableDefinition'
    def __init__(self):
        BaseNode.__init__(self)
        self._node_name = self.NAME