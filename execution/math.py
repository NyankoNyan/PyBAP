# -*- coding:utf-8 -*-

from abap_parser.errors import SyntaxException
from abap_parser.errors import SeriousException
from syntax.node.math_unary import MathUnaryNode
from syntax.node.math_binary import MathBinaryNode
from runtime.variable import RuntimeVariable
import runtime.type


class ExecutorMath:
    
    NAME = 'Math'
    
    def run(self, in_syntax_node, in_context, in_code_execution):
        if in_syntax_node.get_name() == MathUnaryNode.NAME:
            var1, _ = in_code_execution.get_math_value(
                in_syntax_node.get_nodes()[0])
            if in_syntax_node.type == MathUnaryNode.MINUS:
                result = -var1.value
            elif in_syntax_node.type == MathUnaryNode.PLUS:
                result = var1.value
            else:
                raise SeriousException()
        elif in_syntax_node.get_name() == MathBinaryNode.NAME:
            var1, _ = in_code_execution.get_math_value(
                in_syntax_node.get_nodes()[0])
            var2, _ = in_code_execution.get_math_value(
                in_syntax_node.get_nodes()[1])
            if var1.metaname != var2.metaname:
                raise SyntaxException()
            #todo add type conversion
            if in_syntax_node.type == MathBinaryNode.PLUS:
                result = var1.value + var2.value
            elif in_syntax_node.type == MathBinaryNode.MINUS:
                result = var1.value - var2.value
            elif in_syntax_node.type == MathBinaryNode.DIV:
                result = var1.value / var2.value
            elif in_syntax_node.type == MathBinaryNode.MULT:
                result = var1.value * var2.value
            elif in_syntax_node.type == MathBinaryNode.INT_DIV:
                result = var1.value // var2.value
            elif in_syntax_node.type == MathBinaryNode.INT_MOD:
                result = var1.value % var2.value              
            else:
                raise SeriousException()
        else:
            return SeriousException()
        return (RuntimeVariable(var1.metaname, result), runtime.type.VALUE)
