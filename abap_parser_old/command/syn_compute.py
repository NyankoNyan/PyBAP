# -*- coding:utf-8 -*-

from .syntax_converter import SyntaxConverter
from ..exceptions import SyntaxException, SeriousException, ConvertException
from ..token import Tokens
from ..brackets_dissolver import BracketsDissolver

class SynCompute(SyntaxConverter):
    
    def __init__(self, context):
        SyntaxConverter.__init__(self, context)
        self.expression = None
        self.var_desc = None
    
    def _convert(self):
        self._tokens = BracketsDissolver().run_with_list(self._tokens)
        if self._is_word('COMPUTE'):
            self._skip()
        var = self._read_word()
        self.var_desc = self._context.get_variable(var)
        if self.var_desc == None:
            raise SyntaxException()
        self._read_word('=')
        syn_expr = SynExpression(self._context)
        syn_expr.convert(self._tokens, self._index)
        self.expression = syn_expr
        
    def debug_print(self):
        print ('SynCompute: ' + str(self)
               + '\n\tVariable description: ' + str(self.var_desc)
               + '\n\tExpression: ' + str(self.expression))
        

class ExpNode:
    def get_priority(self):
        return 0
    
    def is_binary(self):
        return False
    
    def is_unary(self):
        return False
    
    def is_blind(self):
        return True
    
    def can_be_unary(self):
        return False
    
    def convert_to_unary(self):
        raise SeriousException()


class ExpSimpleValue(ExpNode):
    CHAR = 'character_string'
    INT = 'int32_value'
    FLOAT = 'double_value'
    NUM = 'numeric_string'
    STRING = 'string_object'
    def __init__(self, simple_type, value):
        if not simple_type in [self.CHAR, self.INT, self.FLOAT, self.NUM, self.STRING]:
            raise SeriousException()
        self._simple_type = simple_type
        self._value = value
    
    @staticmethod
    def convert_numeric(in_str):
        for symb in in_str:
            if not symb in set('0123456789'):
                raise ValueError()
        return in_str
    
    @staticmethod
    def convert_float(in_str):
        return float(in_str)
        
    @staticmethod
    def convert_int(in_str):
        return int(in_str)
    
    @staticmethod
    def create(token):
        if token['name'] == Tokens.STRING:
            try:
                value = ExpSimpleValue.convert_numeric(token['body'])
                simple_type = ExpSimpleValue.NUM
            except ValueError:
                try:
                    value = ExpSimpleValue.convert_float(token['body'])
                    simple_type = ExpSimpleValue.FLOAT
                except ValueError:
                    value = token['body']
                    simple_type = ExpSimpleValue.CHAR
        elif token['name'] == Tokens.WORD:
            try:
                value = ExpSimpleValue.convert_int(token['body'])
                simple_type = ExpSimpleValue.INT
            except ValueError:
                raise ConvertException()
        else:
            raise ConvertException()
        return ExpSimpleValue(simple_type, value)


class ExpLinkedValue(ExpNode):
    VAR = 'var'
    CONST = 'const'
    
    def __init__(self, var_type, var_desc):
        self._var_desc = var_desc
    
    @staticmethod
    def create(token, context):
        if token['name'] == Tokens.WORD:
            try:
                var_desc = context.get_variable(token['body'])
                if var_desc != None:
                    return ExpLinkedValue(ExpLinkedValue.VAR, var_desc)
            except:
                pass
            try:
                var_desc = context.get_constant(token['body'])
                if var_desc != None:
                    return ExpLinkedValue(ExpLinkedValue.CONST, var_desc)
            except:
                pass
            raise ConvertException()
        else:
            raise ConvertException()


class ExpBinary(ExpNode):
    PLUS = 'plus'
    MINUS = 'minus'
    MULT = 'mult'
    REAL_DIV = 'real_div'
    POWER = 'power'
    DIV = 'div'
    MOD = 'mod'
    def __init__(self, operation):
        self._left_node = None
        self._right_node = None
        self._operation = operation
        
    def get_priority(self):
        if self.is_complete():
            return 0
        elif self._operation == self.POWER:
            return 4
        elif self._operation == self.DIV or self._operation == self.MOD:
            return 3
        elif self._operation == self.MULT or self._operation == self.REAL_DIV:
            return 2
        elif self._operation == self.PLUS or self._operation == self.MINUS:
            return 1
        else:
            raise SeriousException() 
        
    def is_complete(self):
        return self._left_node != None and self._right_node != None
    
    def set_left_node(self, node):
        if not isinstance(node, ExpNode):
            raise SeriousException()
        self._left_node = node
        
    def set_right_node(self, node):
        if not isinstance(node, ExpNode):
            raise SeriousException()
        self._right_node = node



class SynExpression(SyntaxConverter):
    
    def __init__(self, context):
        SyntaxConverter.__init__(self, context)
        self._nodes = []
        
    def _convert(self): 
        self._tokens = BracketsDissolver().run_with_list(self._tokens, self._index)  
        self._index = 0     
        while(True):
            if self._is_end():
                break
            token = self._read_token()
            
            if token['name'] == Tokens.WORD:
                if token['body'] == '-':
                    self._nodes.append(ExpBinary(ExpBinary.MINUS))
                elif token['body'] == '+':
                    self._nodes.append(ExpBinary(ExpBinary.MULT))
                elif token['body'] == '*':
                    self._nodes.append(ExpBinary(ExpBinary.MULT))
                elif token['body'] == '/':
                    self._nodes.append(ExpBinary(ExpBinary.REAL_DIV))
                elif token['body'] == '**':
                    self._nodes.append(ExpBinary(ExpBinary.POWER))
                elif token['body'] == 'DIV':
                    self._nodes.append(ExpBinary(ExpBinary.DIV))
                elif token['body'] == 'MOD':
                    self._nodes.append(ExpBinary(ExpBinary.MOD))
                else:
                    try:
                        self._nodes.append(ExpSimpleValue.create(token))
                    except ConvertException:
                        try:
                            self._nodes.append(ExpLinkedValue.create(token, self._context))
                        except ConvertException:
                            raise SyntaxException()
            elif token['name'] == Tokens.STRING:
                pass
            elif token['name'] == Tokens.DELIMITER:
                if token['body'] == '(':
                    pass
                elif token['body'] == ')':
                    pass
                elif token['body'] == '+':
                    if self._is_last_word:
                        pass
                    else:
                        self._nodes.append(ExpBinary(ExpBinary.PLUS))
                else:
                    raise SyntaxException()
            else:
                raise SyntaxException()
            
            if token['name'] == Tokens.WORD:
                self._is_last_word = True
            else:
                self._is_last_word = False