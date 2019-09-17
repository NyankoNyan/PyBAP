# -*- coding:utf-8 -*-
from branch import BranchNode
from abap_parser.errors import SyntaxException, SeriousException

class BaseBinaryNode(BranchNode):
    
    def __init__(self):
        BranchNode.__init__(self)
        self._subnode_list.append(None)
        self._subnode_list.append(None)
        self._sub_count = 2
        
    def send_left(self, in_node):
        if self._subnode_list[0] == None and in_node != None:
            self._subnode_list[0] = in_node
        else:
            raise SyntaxException()
        return True        
    
    def send_right(self, in_node):
        if self._subnode_list[1] == None and in_node != None:
            self._subnode_list[1] = in_node
        else:
            raise SyntaxException()
        return True
    
    def _check_self(self):
        if self._subnode_list[0] == None or self._subnode_list[1] == None:
            raise SeriousException()
