# -*- coding:utf-8 -*-
from leaf import LeafNode
from abap_parser.errors import SeriousException, SyntaxException

class ValueNode(LeafNode):
    NAME = 'Value'
    IN_WORD = 'word'
    IN_CHARVAL = 'charval'
    IN_STRING = 'string'
    STRING = 'string'
    CHARVAL = 'charval'
    FLOAT = 'float'
    INT = 'int'
    def __init__(self, in_value, in_type):
        LeafNode.__init__(self)
        self._node_name = self.NAME
        if in_type == self.IN_WORD:
            try:
                self.value = int(in_value)
                self.type = self.INT
            except:
                raise SyntaxException()
        elif in_type == self.IN_CHARVAL:
            if type(in_value) != str and type(in_value) != unicode:
                raise SeriousException()
            try:
                self.value = float(in_value)
                self.type = self.FLOAT
            except:
                self.value = in_value.rstrip()
                self.type = self.CHARVAL
        elif in_type == self.IN_STRING:
            if type(in_value) != str and type(in_value) != unicode:
                raise SeriousException()
            self.value = in_value
            self.type = self.STRING
        else:
            raise SeriousException()
