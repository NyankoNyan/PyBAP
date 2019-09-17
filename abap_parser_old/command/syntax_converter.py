# -*- coding:utf-8 -*-

from ..exceptions import SeriousException, SyntaxException
from ..token import Tokens
from ..const_parse import ConstParse, ParseError

class SyntaxConverter:
    def __init__(self, context):
        self._context = context
        self._tokens = None
        self._index = 0
        
    def convert(self, ctokens, start_index=0):
        self._set_ctokens(ctokens)
        self._index = start_index
        self._convert()
        return self._index
    
    def debug_print(self):
        pass
        
    def _convert(self):
        pass
        
    def _set_ctokens(self,ctokens):
        self._tokens = ctokens
        self._index = 0
    
    @staticmethod
    def is_number(value):
        if len(value) == 0:
            raise SeriousException()
        for symb in set(value):
            if symb not in '0123456789':
                return False
        return True
    
    @staticmethod
    def is_float(value):
        if len(value) == 0:
            pass
    
    def _is_end(self):
        return self._index >= len(self._tokens)             
    
    def _read_token(self):
        if self._is_end():
            raise SyntaxException()
        index = self._index
        self._index += 1
        return self._tokens[index]
        
    
    def _read_space(self):
        if self._is_end():
            raise SyntaxException()        
        token = self._tokens[self._index]
        if token['name'] != Tokens.SPACE:
            raise SyntaxException()
        self._index += 1
    
    def _read_word(self, text=None):
        if self._is_end():
            raise SyntaxException()        
        token = self._tokens[self._index]
        if token['name'] != Tokens.WORD or (text != None and token['body'] != text):
            raise SyntaxException()
        self._index += 1
        return token['body']
    
    def _is_word(self, name=None):
        if self._is_end():
            return False
        token = self._tokens[self._index]
        return token['name'] == Tokens.WORD and (name == None or token['body'] == name)
    
    def _is_next(self, name, body=None):
        if self._is_end():
            return False
        token = self._tokens[self._index]
        return token['name'] == name and (body == None or token['body'] == body)
    
    def _read_next(self, name, body):
        if self._is_end():
            return False        
        token = self._tokens[self._index]
        if token['name'] != name or token['body'] != body:
            raise SyntaxException()
        self._index += 1
    
    def _skip(self):
        self._index += 1
        
    def _read_int_const(self):
        body = self._read_word()
        try:
            return ConstParse.convert_int(body)
        except ParseError:
            const = self._context.get_constant(body)
            if not const.is_int():
                raise SyntaxException()
            return const.get_value()
        
    def _read_const(self):
        ok, value = self._token_get_const(self._read_token())
        if ok:
            return value
        else:
            raise SyntaxException()
        
    def _is_const(self):
        ok = self._token_get_const(self._tokens[self._index])[0]
        return ok
    
    def _token_get_const(self, token):
        if token['name'] == Tokens.WORD:
            try:
                return True, ConstParse.convert_int(token['body'])
            except:
                try:
                    return True, self._context.get_constant_value(token['body'])
                except:
                    return (False, None)
        elif token['name'] == Tokens.STRING:
            try:
                return True, ConstParse.convert_numeric(token['body'])
            except:
                try:
                    return True, ConstParse.convert_float(token['body'])
                except:
                    return True, token['body']
        else:
            return False, None