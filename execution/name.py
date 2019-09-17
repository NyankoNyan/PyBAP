# -*- coding:utf-8 -*-

import runtime.type

class ExecutorName:
    
    NAME = 'Name'
    
    def run(self, in_syntax_node, in_context, in_code_execution):
        return (in_syntax_node.name, runtime.type.NAME)