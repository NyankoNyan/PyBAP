# -*- coding:utf-8 -*-

"""Context meta`s exception"""

class AlreadyExistError(Exception):
    def __init__(self, in_name):
        self._name = in_name


class NotExistError(Exception):
    def __init__(self, in_name):
        self._name = in_name
        
        
class InvalidTypeError(Exception):
    def __init__(self, in_name):
        self._name = in_name
        
        
class InvalidVariableError(Exception):
    def __init__(self, in_name):
        self._name = in_name
        

"""Types"""

class Type:
    # base types
    BT_CHAR = 'C'
    BT_RAW = 'X'
    BT_FLOAT = 'F'
    BT_INT = 'I'
    BT_DEC = 'P'
    BT_TIME = 'T'
    BT_DATE = 'D'
    BT_STRING = 'STRING'
    BT_XSTRING = 'XSTRING'
    # table kinds
    TK_NONE = 'NONE'
    TK_STANDARD = 'STANDARD'
    TK_SORTED = 'SORTED'
    TK_HASHED = 'HASHED'
    # fuzzy types
    FUZ_ANY = 'ANY'
    FUZ_TABLE = 'TABLE'
    FUZ_CSEQUENCE = 'CSEQUENCE'
    FUZ_CLIKE = 'CLIKE'
    def __init__(self):
        self.name = ''
        self.proto = ''
        self.proto_meta = None
        self.ref_table = ''
        self.ref_field = ''
        self.table_kind = self.TK_NONE
        self.keys = None
        self.components = None
        self.base_type = self.BT_CHAR
        self.base_length = 1
        self.base_decimals = 0
    def check(self):
        if (len(self.name) == 0
            or (self.name[0] == '<' and self.name[-1] == '>')):
            return False
        if ((self.base_type == self.BT_CHAR or self.base_type == self.BT_DEC)
             and self.base_length <= 0):
            return False
        if self.base_decimals < 0:
            return False 
        return True


"""Data"""


class Data:
    def __init__(self):
        self.name = ''
        self.type_meta = None
        self.static = False
    def check(self):
        if len(self.name) == 0:
            return False
        if self.type_meta == None:
            return False
        return True 
        

class Constant:
    def __init__(self):
        self.name = ''
        self.type_meta = None
        self.value = None
    def check(self):
        if len(self.name) == 0:
            return False
        if self.type_meta == None:
            return False
        if not self.meta.check():
            return False
        if self.value == None:
            return False
        return True


"""Complex storages"""


class ContextMeta:
    def __init__(self):
        self._parent_context = None
        self._types = {}
        self._variables = {}
        self._constants = {}
    def add_type(self, in_type):
        if in_type.name not in self._types:
            if len(in_type.proto) > 0:
                proto_type = self.get_type(in_type.proto) 
                in_type.proto_meta = proto_type
            if not in_type.check():
                raise InvalidTypeError(in_type.name)
            self._types[in_type.name] = in_type
        else:
            raise AlreadyExistError()
    def get_type(self, in_name):
        try:
            return self._types[in_name]
        except KeyError:
            if self._parent_context != None:
                self._parent_context.get_type(in_name)
            else:
                raise NotExistError()
    def add_variable_meta(self, in_variable):
        if in_variable.name not in self._variables:
            if not in_variable.check():
                raise InvalidVariableError(in_variable.name)
            self._variables[in_variable.name] = in_variable
        else:
            raise AlreadyExistError()
    def get_variable_meta(self, in_name):
        try:
            return self._variables[in_name]
        except KeyError:
            if self._parent_context != None:
                self._parent_context.get_variable_meta(in_name)
            else:
                raise NotExistError()
    def add_constant_meta(self, in_constant):
        if not in_constant.check():
            raise InvalidTypeError()
        if in_constant.meta.name in self._constants:
            raise AlreadyExistError()
        self._constants[in_constant.meta.name] = in_constant
    def get_constant_meta(self, in_name):
        try:
            return self._constants[in_name]
        except KeyError:
            if self._parent_context != None:
                self._parent_context.get_constant_meta(in_name)
            else:
                raise NotExistError()


class Form():
    def __init__(self):
        self.name = ''
        self.static_context_meta = None
        self.context_meta = None
        self.syntax_root = None
        
        
class Report():
    def __init__(self):
        self.name = ''
        self.context_meta = None
        self.forms = {}
        self.pai_modules = {} #future
        self.pbo_modules = {} #future
        self.includes = {} #future
        self.classes = {} #future
        self.dynpro_meta = None #future
        self.screens = {} #future
        self.type_pools = {} #future

        