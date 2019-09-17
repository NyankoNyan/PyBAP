# -*- coding:utf-8 -*-

from base import SyntaxBase
from abap_parser.errors import BadReceiverError, SyntaxException
from name_parser import NameParser
from expression_source import ExpressionSource
from expression_parser import ExpressionParser
from syntax.node.compute import ComputeNode

class SyntaxCompute(SyntaxBase):
    NAME = 'Compute'
    def __init__(self):
        #SyntaxBase.__init__(self, in_context_meta)
        self._variable_nodes = []
        self._expression_node = None
    def parse(self, in_command):
        command_pos = 0
        while True:
            command_pos_before = command_pos
            try:
                variable_node, command_pos = NameParser(in_command, command_pos).parse()
            except:
                break;
            if len(in_command) < command_pos:
                raise BadReceiverError()
            if len(in_command) > command_pos:
                token = in_command[command_pos]
                if token['name'] == 'word' and token['body'] == '=':
                    self._variable_nodes.append(variable_node)
                    command_pos += 1
                else:
                    command_pos = command_pos_before
                    break  
            else:
                command_pos = command_pos_before
                break               
        #=======================================================================
        # while (var_iter * 2 + 1 < len(in_command) 
        #        and in_command[var_iter * 2 + 1]['name'] == 'word'
        #        and in_command[var_iter * 2 + 1]['body'] == '='):
        #     if in_command[var_iter * 2]['name'] != 'word':
        #         raise errors.BadReceiverError()
        #     try:
        #         variable_meta = NameParser(in_command['command'], context['pos']).parse()
        #         variable_meta = self._context_meta.get_variable_meta(in_command[var_iter * 2]['body'])
        #     except:
        #         pass
        #     self._variable_metas.append(variable_meta)
        #=======================================================================
        if len(self._variable_nodes) == 0:
            raise BadReceiverError()
        expr_source = ExpressionSource(in_command, command_pos)
        self._expression_node = ExpressionParser(expr_source).get_syntax_node()
        if expr_source.get_index() < len(in_command):
            raise SyntaxException()
        return ComputeNode(self._variable_nodes, self._expression_node)
