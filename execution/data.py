# -*- coding:utf-8 -*-

from abap_parser.errors import SeriousException, SyntaxException
from syntax.node.variable_definition import VariableDefinitionNode


class ExecutorData:
    
    NAME = 'Data'
    
    def run(self, in_syntax_node, in_context, in_code_execution):
        if in_context.is_variable_exist( in_syntax_node.name ):
            raise SyntaxException()
        if in_syntax_node.reftype == VariableDefinitionNode.LIKE:
            try:
                metadata = in_context.get_var_metadata(in_syntax_node.name)
            except:
                raise SyntaxException()
        elif in_syntax_node.reftype == VariableDefinitionNode.TYPE:
            typename, _ = in_code_execution.get_node_value(in_syntax_node.typename)
            if self.__is_type_simple(typename):
                if in_syntax_node.length == None:
                    length = 0
                else:
                    length, _ = in_code_execution.get_node_value(
                        in_syntax_node.length)
                if in_syntax_node.decimals == None:
                    decimals = 0
                else:
                    decimals, _ = in_code_execution.get_node_value(
                        in_syntax_node.decimals)
                metadata = in_context.request_simple_type_meta(
                    typename=in_code_execution.get_node_value(
                        in_syntax_node.typename)[0], 
                    length=length, 
                    decimals=decimals,
                    )
            else:
                metadata = in_context.get_type_metadata(typename)
        else:
            raise SeriousException()
        in_context.define_variable(
            name=in_syntax_node.name,
            metadata=metadata,
            )
        return (True, None)

    def __is_type_simple(self, type_name):
        return type_name in ['I']