# -*- coding:utf-8 -*-
from base_binary import BaseBinaryNode
from abap_parser.errors import SeriousException

class MemberNode(BaseBinaryNode):
    NAME = 'Member'
    STATIC = 'static'
    DYNAMIC = 'dynamic'
    FIELD = 'field'
    def __init__(self, in_type):
        BaseBinaryNode.__init__(self)
        self._node_name = self.NAME
        if not in_type in [self.STATIC, self.DYNAMIC, self.FIELD]:
            raise SeriousException()
#     def get_priority(self):
#         if self._subnode_list[0] == None or self._subnode_list[1] == None:
#             return 1001
#         else:
#             return 0