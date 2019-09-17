# -*- coding:utf-8 -*-


class RuntimeMetadata:
    
    def __init__(self, simple, name):
        self.simple = simple
        self.name = name
        self.default = None
        
    def get_full_path(self):
        pass
    
    
class RuntimeMetadataSimple(RuntimeMetadata):
    
    def __init__(self, typename, length, decimals, default):
        RuntimeMetadata.__init__(self, True, typename)
        self.length = length
        self.decimals = decimals
        self.default = default
        
    def get_full_name(self):
        path = '/TYPE=' + str(self.name)
        if self.name in ['C', 'P', 'X']:
            path += '/LENGTH=' + str(self.length)
        if self.name in ['P']:
            path += '/DECIMALS=' + str(self.decimals)
        return path
        

class RuntimeMetadataStruct(RuntimeMetadata):
    pass


class RuntimeMetadataTable(RuntimeMetadata):
    pass
    