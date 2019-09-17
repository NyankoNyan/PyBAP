# -*- coding:utf-8 -*-
from abap_parser_old.context_description import ContextDescription
from abap_parser_old.exceptions import SeriousException

class RuntimeContext(object):

    def __init__(self, context_meta):
        self.parent_context = None
        if not isinstance(context_meta, ContextDescription):
            raise SeriousException()
        self.meta = None
        self.variables = []
        
