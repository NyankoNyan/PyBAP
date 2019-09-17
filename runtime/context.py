# -*- coding:utf-8 -*-

from abap_parser.errors import SeriousException, SyntaxException
from variable import RuntimeVariable
from metadata import RuntimeMetadataSimple 


class RuntimeContext:
    
    def __init__(self):
        self._variables = {}
        self._metadatas = {}
        
    def get_variable(self, name):
        return self._variables[name]
    
    def set_variable(self, name, value):
        variable = self._variables[name]
        variable.value = value
    
    def is_variable_exist(self, name):
        return self._variables.has_key(name)
    
    def get_var_metadata(self, name):
        if not self._variables.has_key(name):
            raise SyntaxException()
        metaname = self._variables.get(name).metaname
        if not self._metadatas.has_key(metaname):
            raise SeriousException()
        return self._metadatas[name]
    
    def get_type_metadata(self, in_name):
        pass
    
    def define_variable(self, name, metadata):
        if self._variables.has_key(name):
            raise SyntaxException()
        variable = RuntimeVariable(metadata.get_full_name(), metadata.default)
        self._variables[name] = variable
        return variable
    
    def request_simple_type_meta(self, typename, length, decimals):
        if typename == 'I':
            default_value = 0
        elif typename == 'C':
            default_value = ' '
        else:
            raise SyntaxException()
        metadata = RuntimeMetadataSimple(
            typename=typename,
            length=length, 
            decimals=decimals,
            default=default_value
            )
        name = metadata.get_full_name()
        if self._metadatas.has_key(name):
            return self._metadatas.get(name)
        else:
            self._metadatas[name] = metadata
            return metadata