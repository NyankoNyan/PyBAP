# -*- coding:utf-8 -*-

from abap_parser.errors import SyntaxException
from syntax.node.value import ValueNode
from syntax.node.name import NameNode
from syntax.node.component import ComponentNode


class NameParser:
    def __init__(self, in_command, in_pos):
        self._command = in_command
        self._pos = in_pos
    def parse(self):
        if self._pos > len(self._command):
            raise SyntaxException()
        node = None
        while True:
            token = self._command[self._pos]
            is_value = False
            is_component = False
            if token['name'] == 'word':
                try:
                    new_node = ValueNode(token['body'], ValueNode.IN_WORD)
                    is_value = True
                except:
                    new_node = NameNode(token['body'])
                if node == None:
                    node = new_node
                else:
                    node = ComponentNode(node, new_node)
                    is_component = True   
            elif token['name'] == 'charstr':
                node = ValueNode(token['body'], ValueNode.IN_CHARVAL)
                is_value = True
            else:
                raise SyntaxException()
            self._pos += 1
            if self._pos >= len(self._command):
                break
            token_next = self._command[self._pos]
            if token_next['name'] == 'field':
                self._pos += 1
            else:
                break
            if self._pos <= len(self._command): 
                raise SyntaxException()
        if is_value and is_component:
            raise SyntaxException()
        return (node, self._pos)
