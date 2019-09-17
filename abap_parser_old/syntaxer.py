# -*- coding:utf-8 -*-

#from .__init__ import *
import command.syn_data
from .command.syn_data import SynData
from .command.syn_write import SynWrite
from .command.syn_compute import SynCompute
#from .syn_data import SynData
#from .command.syn_write import SynWrite
from abap_parser_old.context_description import ContextDescription
from .token import Tokens

class Syntaxer:
    def __init__(self):
        self._context = ContextDescription()
        self._commands = []
    
    def send(self, tokens):
        self._create_pre_tree(tokens)
    
    @staticmethod
    def _compress_body(token):
        return {
            'name':token['name'], 
            'body':''.join(token['body']).upper()
            }
    
    @staticmethod
    def _compress(tokens):
        result = []
        for token in tokens:
            result.append(Syntaxer._compress_body(token))
        return result
    
    def _create_pre_tree(self,tokens):
        if len(tokens) == 0:
            return []
        ctokens = self._compress(tokens)
        initial_token = ctokens[0]
        if initial_token['name'] == Tokens.WORD:
            if (ctokens[1]['name'] == Tokens.SPACE 
                  and ctokens[2]['name'] == Tokens.WORD 
                  and ctokens[2]['body'] == '='):
                syn_compute = SynCompute(self._context)
                syn_compute.convert(ctokens)
                self._commands.append(syn_compute)
            elif initial_token['body'] == 'DATA':
                syn_data = SynData(self._context)
                syn_data.convert(ctokens)
                self._commands.append(syn_data)
            elif initial_token['body'] == 'WRITE':
                syn_write = SynWrite(self._context)
                syn_write.convert(ctokens)
                self._commands.append(syn_write)
            else:
                pass
        else:
            pass
    
    def debug_print(self):
        print ('Syntaxer: ' + str(self)) 
        self._context.debug_print()
        for command in self._commands:
            command.debug_print()
        
        