# -*- coding:utf-8 -*-

from .syntax_converter import SyntaxConverter
from ..token import Tokens
from ..exceptions import SyntaxException
from ..brackets_dissolver import BracketsDissolver

class SynData(SyntaxConverter):    
    
    def __init__(self, context):
        SyntaxConverter.__init__(self, context)
        self.varname = ''
        self.type_name = ''
        self.decimals = 0
        self.length = 1 
        
        self._length_ok = False
        self._decimals_ok = False       
        
    def debug_print(self):
        print ('SynData ' + str(self)
               + '\n\tName: ' + str(self.varname)
               + '\n\tType: ' + str(self.type_name)
               + '\n\tLength ' + str(self.length)
               + '\n\tDecimals ' + str(self.decimals))
        
    def _convert(self):
        self._tokens = BracketsDissolver().run_with_list(self._tokens)
        self._read_word('DATA')
        self.varname = self._read_word()
        if self._is_next(Tokens.LB_SOLID):
            self._skip()
            self.length = self._read_int_const()
            self._read_next(Tokens.RB_CLOSE)
            self._length_ok = True
        if not self._is_end():
            if self._is_word('TYPE'):
                like_mode = False
            elif self._is_word('LIKE'):
                like_mode = True
            else:
                raise SyntaxException()
            self._skip()
            if like_mode:
                self.type_name = self._context.get_like(self._read_word()).name
            else:
                self.type_name = self._read_word()
        if not self._is_end():
            self._add_optional_part()
        if not self._is_end():
            self._add_optional_part()
        if not self._is_end():
            raise SyntaxException()
        self._context.add_variable(self)
                    
    def _add_optional_part(self):
        if self._is_word('DECIMALS'):
            if self._decimals_ok:
                raise SyntaxException()
            self._skip()
            self.decimals = self._read_int_const()
            self._decimals_ok = True
        elif self._is_word('LENGTH'):
            if self._length_ok:
                raise SyntaxException()
            self._skip()
            self.length = self._read_int_const()
            self._length_ok = True
        else:
            raise SyntaxException()
