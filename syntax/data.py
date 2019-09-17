# -*- coding:utf-8 -*-

from base import SyntaxBase
from abap_parser.errors import SyntaxException, BadReceiverError
from syntax.node.variable_definition import VariableDefinitionNode
from name_parser import NameParser
from expression_source import ExpressionSource
from expression_parser import ExpressionParser


class SyntaxData(SyntaxBase):
    
    NAME = 'Data'
    
    def __init__(self):
        pass
        #SyntaxBase.__init__(self)        
    def parse(self, in_command):
        if in_command[0]['name'] != 'word' or in_command[0]['body'] != 'DATA':
            raise BadReceiverError()      
        if len(in_command) > 2 and in_command[1]['body'] == 'BEGIN' and in_command[2]['body'] == 'OF':
            if len(in_command) != 4:
                raise SyntaxException()
            pass
        else:            
            context = dict(
                command = in_command,
                pos = 1,
                name = '',
                length_complete = False, 
                decimals_complete = False, 
                value_complete = False,
                length_node = None,
                decimals_node = None,
                value_node = None,
                type_node = None,
                like = False,
                type_complete = False,
                is_table = False,
                tabkind = '',
                is_range = False,
                read_only = False)            
            self._parse_name(context)
            self._parse_len_short(context)
            self._parse_type(context)
            if context['is_table']:
                pass
            elif context['is_range']:
                pass
            else:
                self._parse_len(context)
                self._parse_decimals(context)
                self._parse_value(context)
                self._parse_is_initial(context)
                self._parse_read_only(context)
                node = VariableDefinitionNode(
                    name = context['name'],
                    reftype = VariableDefinitionNode.LIKE if context['like'] else VariableDefinitionNode.TYPE,
                    length = context['length_node'], 
                    decimals = context['decimals_node'],
                    value = context['value_node'],
                    typename = context['type_node'])
            if len(context['command']) > context['pos']:
                raise SyntaxException()
        return node
            
    def _parse_name(self, context):
        if len(context['command']) <= context['pos']:
            raise SyntaxException()
        if context['command'][context['pos']]['name'] != 'word':
            raise SyntaxException()
        context['name'] = context['command'][context['pos']]['body']
        context['pos'] += 1
    def _parse_len_short(self, context):
        if len(context['command']) <= context['pos']:
            return
        if context['command'][context['pos']]['name'] != 'solid_lb':
            return
        context['pos'] += 1
        context['length_node'], context['pos'] = NameParser(context['command'], context['pos']).parse()
        if len(context['command']) <= context['pos']:
            raise SyntaxException()
        if context['command'][context['pos']]['name'] != 'close_rb':
            raise SyntaxException()
        context['pos'] += 1
        context['length_complete'] = True
    def _parse_type(self, context):
        if len(context['command']) <= context['pos']:
            return
        token = context['command'][context['pos']]
        if token['name'] != 'word':
            return
        if token['body'] == 'TYPE':
            pass#ok
        elif token['body'] == 'LIKE':
            context['like'] = True
        else:
            return 
        context['pos'] += 1
        if len(context['command']) <= context['pos']:
            raise SyntaxException()
        if len(context['command']) > context['pos'] + 1:
            token = context['command'][context['pos']]
            token2 = context['command'][context['pos'] + 1]
            if token['name'] == 'word' and token2['name'] == 'word' and token2['body'] == 'OF':
                if token['body'] == 'RANGE':
                    context['is_range'] = True
                elif token['body'] == 'TABLE':
                    context['is_table'] = True
        if not context['is_table'] and not context['is_range'] and len(context['command']) > context['pos'] + 2:
            token3 = context['command'][context['pos'] + 2]
            if (token['name'] == 'word' and token2['name'] == 'word' and token3['name'] == 'word'
                and token2['body'] == 'TABLE' and token3['body'] == 'OF'):
                context['is_table'] = True
                context['typekind'] = token['body']
        context['type_node'], context['pos'] = NameParser(context['command'], context['pos']).parse()
        context['type_complete'] = True      
    def _parse_len(self, context):
        if len(context['command']) <= context['pos']:
            return
        token = context['command'][context['pos']]
        if token['name'] != 'word' or token['body'] != 'LENGTH':
            return 
        if context['length_complete']:
            raise SyntaxException()
        context['pos'] += 1
        if len(context['command']) <= context['pos']:
            raise SyntaxException()
        context['length_node'], context['pos'] = NameParser(context['command'], context['pos']).parse()
        context['length_complete'] = True
    def _parse_decimals(self, context):
        if len(context['command']) <= context['pos']:
            return
        token = context['command'][context['pos']]
        if token['name'] != 'word' or token['body'] != 'DECIMALS':
            return 
        if context['decimals_complete']:
            raise SyntaxException()
        context['pos'] += 1
        if len(context['command']) <= context['pos']:
            raise SyntaxException()
        context['decimals_node'], context['pos'] = NameParser(context['command'], context['pos']).parse()
        context['decimals_complete'] = True
    def _parse_value(self, context):
        if len(context['command']) <= context['pos']:
            return
        token = context['command'][context['pos']]
        if token['name'] != 'word' or token['body'] != 'VALUE':
            return 
        if context['value_complete']:
            raise SyntaxException()
        context['pos'] += 1
        if len(context['command']) <= context['pos']:
            raise SyntaxException()
        expr_source = ExpressionSource(context['command'], context['pos'])
        context['value_node'] = ExpressionParser(expr_source, False).get_syntax_node()
        context['pos'] = expr_source.get_index()
        context['value_complete'] = True
    def _parse_read_only(self, context):
        if len(context['command']) <= context['pos'] + 2:
            return
        token = context['command'][context['pos']]
        token2 = context['command'][context['pos'] + 1]
        token3 = context['command'][context['pos'] + 2]
        if (token['name'] != 'word' or token['body'] != 'READ'
            or token2['name'] != 'field'
            or token3['name'] != 'word' or token3['body'] != 'ONLY'):
            return
        if context['read_only']:
            raise SyntaxException()
        context['read_only'] = True
        context['pos'] += 3        
    def _parse_is_initial(self, context):
        if len(context['command']) <= context['pos'] + 1:
            return  
        token = context['command'][context['pos']]
        token2 = context['command'][context['pos'] + 1]           
        if (token['name'] != 'word' or token['body'] != 'IS'
            or token2['name'] != 'word' or token2['body'] != 'INITIAL'):
            return
        if context['value_complete']:
            raise SyntaxException()
        context['value_complete'] = True