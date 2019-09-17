# -*- coding:utf-8 -*-

from .syntax_converter import SyntaxConverter
from ..brackets_dissolver import BracketsDissolver

class SynWrite(SyntaxConverter):
    
    def __init__(self, context):
        SyntaxConverter.__init__(self, context)
        self.const = ''
        self.var = ''
        self.next_line = False
        
    def debug_print(self):
        print ('SynWrite ' + str(self)
               + '\n\tConst: ' + str(self.const)
               + '\n\tVar: ' + str(self.var)
               + '\n\tNext line: '+ str(self.next_line))
        
    def _convert(self):
        self._tokens = BracketsDissolver().run_with_list(self._tokens)
        self._read_word('WRITE')
        if self._is_word('/'):
            self._skip()
            self.next_line = True
        if self._is_const():
            self.const = self._read_const()
        else:
            self.var = self._context.get_variable(self._read_word())
