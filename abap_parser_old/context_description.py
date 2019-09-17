# -*- coding:utf-8 -*-

from exceptions import SeriousException, SyntaxException


class TypeDescription:
    
    def __init__(self):
        pass
    
    def debug_print(self):
        pass

class TypeDescrBase(TypeDescription):
    
    INT4 = 'int4'
    
    def __init__(self, type_name, length=1, decimals=0):
        self.name = type_name
        self.type = self._get_type_id(type_name)
        self.length = length
        self.decimals = decimals
        
    def _get_type_id(self, type_name):
        if type_name == 'I':
            return self.INT4
        else:
            raise SeriousException()
        
    def debug_print(self):
        print (str(self)
               + '\n\tName: ' + str(self.name)
               + '\n\tType: ' + str(self.type)
               + '\n\tLength: ' + str(self.length)
               + '\n\tDecimals: ' + str(self.decimals))


class ValueDescription:
    
    def __init__(self, name, type_desc):
        self.name = name
        self.type_desc = type_desc
        
    def is_int(self):
        #todo implement
        raise Exception()
    
    def get_value(self):
        #todo implement
        raise Exception()
    
    def debug_print(self):
        print (str(self)
               + '\n\tName: ' + str(self.name)
               + '\n\tType description: ' + str(self.type_desc))
    
    

class ContextDescription:
    
    def __init__(self, top_context=None):
        if top_context != None and not isinstance(top_context, ContextDescription):
            raise SeriousException()
        self.top_context = top_context
        self.var_descs = {}
        self.type_descs = {}
        self.const_descs = {}
    
    def get_constant(self, name):
        desc = self.const_descs[name]
        if desc == None and self.top_context != None:
            desc = self.top_context.get_constant(name)
        return desc
    
    def get_constant_value(self, name):
        desc = self.get_constant(name)
        if desc == None:
            raise SyntaxException()
        return desc.value
    
    def get_like(self, name):
        var_desc = self.var_descs['name']
        if var_desc:
            return var_desc.type_desc
        else:
            const_desc = self.const_descs['name']
            if const_desc:
                return const_desc.type_desc
        if self.top_context:
            return self.top_context.get_like(name)
        else:
            raise SyntaxException()            
    
    def get_type(self, name):
        type_desc = self.type_descs['name']
        if not type_desc and self.top_context:
            type_desc = self.top_context.get_type(name)
        if type_desc:
            return type_desc
        else:
            raise SyntaxException()
    
    def _search_default_type(self, name):
        pass
        
    def add_variable(self, syn_data):
        if not self.var_descs.get(syn_data.varname) and not self.const_descs.get(syn_data.varname):
            try:
                type_desc = TypeDescrBase(syn_data.type_name, syn_data.length, syn_data.decimals)
            except:
                type_desc = self.get_type(syn_data.type_name)
            self.var_descs[syn_data.varname] = ValueDescription(syn_data.varname, type_desc)
        else:
            raise SyntaxException()
        
    def get_variable(self, name):
        var = self.var_descs.get(name)
        if not var:
            if self.top_context:
                var = self.top_context.get_variable(name)
            else:
                raise SyntaxException()
        return var
    
    def debug_print(self):
        print ('ContextDescription: ' + str(self)
               + '\n\tTop context: ' + str(self.top_context)
               + '\n\tTypes: vvv')
        for type_desc in self.type_descs.values():
            type_desc.debug_print()
        print '\tConstants: vvv'
        for const_desc in self.const_descs.values():
            const_desc.debug_print()
        print '\tVariables: vvv'
        for var_desc in self.var_descs.values():
            var_desc.debug_print()