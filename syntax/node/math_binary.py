# -*- coding:utf-8 -*-
from base_binary import BaseBinaryNode
from abap_parser.errors import SeriousException

class MathBinaryNode(BaseBinaryNode):
    NAME = 'MathBinary'
    MINUS = '-'
    PLUS = '+'
    MULT = '*'
    DIV = '/'
    INT_DIV = 'div'
    INT_MOD = 'mod'
    
    def __init__(self, in_type):
        BaseBinaryNode.__init__(self)
        self._node_name = self.NAME
        if not in_type in [self.MINUS, self.PLUS, self.MULT, self.DIV, self.INT_DIV, self.INT_MOD]:
            raise SeriousException()
        self.type = in_type
#     def get_priority(self):
#         if self._subnode_list[0] == None or self._subnode_list[1] == None:
#             if self._type == self.INT_DIV or self._type == self.INT_MOD:
#                 return 12
#             elif self._type == self.DIV or self._type == self.MOD:
#                 return 11
#             elif self._type == self.MINUS or self._type == self._PLUS:
#                 return 10
#             else:
#                 raise errors.SeriousException()
#         else:
#             return 0
    def is_linked(self):
        return self._subnode_list[0] != None and self._subnode_list[1] != None
