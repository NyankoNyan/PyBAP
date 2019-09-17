# -*- coding:utf-8 -*-
from branch import BranchNode

class OffsetNode(BranchNode):
    NAME = 'Offset'
    def __init__(self):
        BranchNode.__init__(self)
        self._node_name = self.NAME
        self._sub_count = 3
#     def get_priority(self):
#         if self._subnode_list[0] == None or self._subnode_list[1] == None or self._subnode_list[2] == None:
#             return 1000
#         else:
#             return 0
