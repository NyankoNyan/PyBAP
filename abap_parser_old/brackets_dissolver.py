# -*- coding:utf-8 -*-

from .token import Tokens
from .exceptions import SeriousException

class BracketsDissolver:
    
    def __init__(self):
        self._last_space = True
        self._lb_space = False
        self._lb_wait = False
        self._rb_space = False
        self._rb_wait = False
        self._result = []
    
    def run_with_list(self, tokens, start_index=0):
        for index in range(start_index, len(tokens)):
            self._single_token(tokens[index])
        return self._result
    
    def _single_token(self, token):        
        if self._lb_wait:
            self._lb_wait = False
            if token['name'] == Tokens.SPACE:
                if self._lb_space:
                    self._result.append({'name':Tokens.LB_SINGLE})
                else:
                    self._result.append({'name':Tokens.LB_CLOSE})
            else:
                if self._lb_space:
                    self._result.append({'name':Tokens.LB_FAR})
                else:
                    self._result.append({'name':Tokens.LB_SOLID})                    
        if self._rb_wait:
            self._rb_wait = False
            if token['name'] == Tokens.SPACE:
                if self._rb_space:
                    self._result.append({'name':Tokens.RB_SINGLE})
                else:
                    self._result.append({'name':Tokens.RB_CLOSE})
            else:
                if self._rb_space:
                    self._result.append({'name':Tokens.RB_FAR})
                else:
                    self._result.append({'name':Tokens.RB_SOLID})  
        if token['name'] == Tokens.WORD or token['name'] == Tokens.STRING:
            self._result.append(token.copy())
        elif token['name'] == Tokens.SPACE:
            pass
        elif token['name'] == Tokens.DELIMITER and token['body'] == '+':
            if self._last_space:
                self._result.append({'name':Tokens.WORD, 'body':'+'})
            else:
                self._result.append({'name':Tokens.OFFSET_PLUS})
        elif token['name'] == Tokens.DELIMITER and token['body'] == '(':
            self._lb_space = self._last_space
            self._lb_wait = True
        elif token['name'] == Tokens.DELIMITER and token['body'] == ')':
            self._rb_space = self._last_space
            self._rb_wait = True
        else:
            raise SeriousException()        
        self._last_space = token['name'] == Tokens.SPACE