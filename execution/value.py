# -*- coding:utf-8 -*-

from syntax.node.value import ValueNode
from abap_parser.errors import SeriousException
from runtime.variable import RuntimeVariable 
import runtime.type

class ExecutorValue:
    
    NAME = 'Value'
    
    def run(self, in_syntax_node, in_context, in_code_execution):
        if in_syntax_node.type == ValueNode.INT:
            metadata = in_context.request_simple_type_meta('I', 0, 0)
            value = int(in_syntax_node.value)
            metaname = metadata.get_full_name()
        elif in_syntax_node.type == ValueNode.CHARVAL:
            value = str(in_syntax_node.value)
            metadata = in_context.request_simple_type_meta('C', len(value), 0)
            metaname = metadata.get_full_name()
        else:
            raise SeriousException()
        variable = RuntimeVariable(
            metaname=metaname, 
            value=value,
            )
        return (variable, runtime.type.VALUE)