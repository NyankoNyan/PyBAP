# -*- coding:utf-8 -*-

from abap_parser.errors import ParserEndException, SyntaxException, SeriousException
from syntax.node.value import ValueNode
from syntax.node.math_unary import MathUnaryNode
from syntax.node.math_binary import MathBinaryNode
from name_parser import NameParser
from syntax.node.member import MemberNode
from syntax.node.offset import OffsetNode

class ExpressionParser:
    def __init__(self, in_expr_source, in_brackets = False):
        self._expr_source = in_expr_source
        self._last_linked = True
        self._node_line = []
        self._brackets = in_brackets
    def get_syntax_node(self):
        #nodes creation
        try:
            while True:
                self.create_node()
        except ParserEndException:
            pass
        if len(self._node_line) == 0:
            raise SyntaxException()
        #tree creation
        while True:
            max_priority = 0
            work_list = []          
            for index in range(len(self._node_line)):
                node = self._node_line[index]  
#                 priority = node.get_priority()
                priority = self._get_priority(node)
                if priority > max_priority:
                    max_priority = priority
                    del work_list[:]
                if priority == max_priority:
                    work_list.append(index)
            if max_priority == 0:
                break
            offset = 0
            for index in work_list:
                index += offset
                node = self._node_line[index]
                left_node = None
                right_node = None
                if index > 0:
                    left_node = self._node_line[index - 1]
                if node.send_left(left_node):
                    del self._node_line[index - 1]
                    offset -= 1
                    index -= 1
                if index + 1 < len(self._node_line):
                    right_node = self._node_line[index + 1]
                if node.send_right(right_node):
                    del self._node_line[index + 1]
                    offset -= 1
        #tree check
        if len(self._node_line) != 1:
            raise SeriousException()   
        return self._node_line[0]             
    def create_node(self):
        token = self._expr_source.get_next()
        if self._last_linked:
            self._last_linked = False
            if token['name'] == 'word':
                if token['body'] == '-':
                    self._node_line.append(MathUnaryNode(MathUnaryNode.MINUS))
                elif token['body'] == '+':
                    self._node_line.append(MathUnaryNode(MathUnaryNode.PLUS))
                else:
                    try:
                        new_node = ValueNode(token['body'], ValueNode.IN_WORD)
                        self._node_line.append(new_node)
                    except SyntaxException:
                        #todo refactor this shit
                        new_node, self._expr_source._index = NameParser(self._expr_source._token_list, self._expr_source._index - 1).parse()
                        self._node_line.append(new_node)
            elif token['name'] == 'charval':
                self._node_line.append(ValueNode(token['body'], ValueNode.IN_CHARVAL))
            elif token['name'] == 'string':
                self._node_line.append(ValueNode(token['body'], ValueNode.IN_STRING))
            elif token['name'] == 'single_lb':
                subparser = ExpressionParser(self._expr_source)
                subparser.get_syntax_node()
            elif token['name'] == 'single_rb':
                if self._brackets:
                    raise ParserEndException()
                else:
                    raise SyntaxException()
            elif token['name'] == 'far_lb':
                pass
            elif token['name'] == 'far_rb':
                if self._brackets and self._expr_source.is_end():
                    raise ParserEndException()
                else:
                    raise SyntaxException()
            elif token['name'] == 'close_lb':
                pass
            elif token['name'] == 'close_rb':
                raise SyntaxException()
            elif token['name'] == 'solid_lb':
                pass
            elif token['name'] == 'solid_rb':
                raise SyntaxException()
            else:
                raise SeriousException()
        else:
            if token['name'] == 'word':
                if token['body'] == '+':
                    node_type = MathBinaryNode.PLUS
                elif token['body'] == '-':
                    node_type = MathBinaryNode.MINUS
                elif token['body'] == '*':
                    node_type = MathBinaryNode.MULT
                elif token['body'] == '/':
                    node_type = MathBinaryNode.DIV
                elif token['body'] == 'DIV':
                    node_type = MathBinaryNode.INT_DIV
                elif token['body'] == 'MOD':
                    node_type = MathBinaryNode.INT_MOD
                else:
                    raise SeriousException()
                self._node_line.append(MathBinaryNode(node_type))
                self._last_linked = True
            elif token['name'] == 'static_attr':
                self._node_line.append(MemberNode(MemberNode.STATIC))
            elif token['name'] == 'dynamic_attr':
                self._node_line.append(MemberNode(MemberNode.DYNAMIC))
            elif token['name'] == 'field':
                self._node_line.append(MemberNode(MemberNode.FIELD))
            elif token['name'] == 'offset':
                self._node_line.append(OffsetNode())
            else:
                raise SeriousException()
    def _get_priority(self, node):
        if isinstance(node, MathBinaryNode):
            if not node.is_linked():
                if node.type == MathBinaryNode.INT_DIV or node.type == MathBinaryNode.INT_MOD:
                    return 12
                elif node.type == MathBinaryNode.DIV or node.type == MathBinaryNode.MULT:
                    return 11
                elif node.type == MathBinaryNode.MINUS or node.type == MathBinaryNode.PLUS:
                    return 10
                else:
                    raise SeriousException()
        elif isinstance(node, MathUnaryNode):
            if node.is_linked():
                return 100
        return 0
