# -*- coding:utf-8 -*-
from branch import BranchNode
from abap_parser.errors import SeriousException

class MathUnaryNode(BranchNode):
    NAME = 'MathUnary'
    MINUS = '-'
    PLUS = '+'
    def __init__(self, in_type):
        BranchNode.__init__(self)
        self._node_name = self.NAME
        self._sub_count = 1
        self._subnode_list.append(None)
        if not in_type in [self.MINUS, self.PLUS]:
            raise SeriousException()
        self.type = in_type
    #===========================================================================
    # def get_priority(self):
    #     if self._subnode_list[0] == None:
    #         return 100
    #     else:
    #         return 0
    #===========================================================================
    def is_linked(self):
        return self._subnode_list[0] != None
    def send_right(self, in_node):
        if self._subnode_list[0] == None and in_node != None:
            self._subnode_list[0] = in_node
        else:
            raise SeriousException()
        return True
    def _check_self(self):
        if self._subnode_list[0] == None:
            raise SeriousException()
