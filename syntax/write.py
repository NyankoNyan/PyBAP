# -*- coding:utf-8 -*-

from base import SyntaxBase
from abap_parser.errors import BadReceiverError, SyntaxException
from name_parser import NameParser
from syntax.node.write import WriteNode

class SyntaxWrite(SyntaxBase):
    
    NAME = 'Write'
    
    def __init__(self):
        pass
    
    def parse(self, in_command):
        if (in_command[0]['name'] != 'word' 
            or in_command[0]['body'] != 'WRITE'):
            raise BadReceiverError()  
        if len(in_command) <= 1:
            raise SyntaxException()
        context = dict(
            new_line = False,
            text_node = None
            )
        token_id = 1
        token_id = self.__read_slash(token_id, in_command, context)
        token_id = self.__read_text(token_id, in_command, context)
        if (token_id < len(in_command) 
            or context['text_node'] == None):
            raise SyntaxException()
        node = WriteNode(
            context['new_line'], 
            context['text_node'],
            )
        return node
        
    def __read_slash(self, token_id, in_command, context):
        if token_id < len(in_command):
            token = in_command[token_id]
            if token['name'] == 'word' and token['body'] == '/':
                context['new_line'] = True
                token_id += 1
        return token_id
    
    def __read_text(self, token_id, in_command, context):
        if token_id < len(in_command):
            context['text_node'], token_id = NameParser(in_command, token_id).parse()
        return token_id
        
        