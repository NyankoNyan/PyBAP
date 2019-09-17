# -*- coding:utf-8 -*-

from runtime.context import RuntimeContext
from abap_parser.syntax_maker import SyntaxMaker
from abap_parser.errors import ParserEndException
import execution.data
import execution.compute
import execution.math
import execution.name
import execution.value
import execution.write
import syntax.node
import syntax.node.write
import runtime.type
from gui.write_log import WriteLogBack, WriteLogFront

class ExecutionStatement:
    
    def __init__(self):
        class_list = [
            execution.data.ExecutorData,
            execution.compute.ExecutorCompute,
            execution.math.ExecutorMath,
            execution.name.ExecutorName,
            execution.value.ExecutorValue,
            execution.write.ExecutionWrite,
            ]
        self._executors = {}
        for class_ in class_list: 
            self._executors[class_.NAME] = class_()
        self._node_links = {
            syntax.node.compute.ComputeNode.NAME: 
                execution.compute.ExecutorCompute.NAME,
            syntax.node.variable_definition.VariableDefinitionNode.NAME: 
                execution.data.ExecutorData.NAME,
            syntax.node.math_unary.MathUnaryNode.NAME:
                execution.math.ExecutorMath.NAME,
            syntax.node.math_binary.MathBinaryNode.NAME:
                execution.math.ExecutorMath.NAME,
            syntax.node.value.ValueNode.NAME:
                execution.value.ExecutorValue.NAME,
            syntax.node.name.NameNode.NAME:
                execution.name.ExecutorName.NAME,
            syntax.node.write.WriteNode.NAME:
                execution.write.ExecutionWrite.NAME,
            }
        self._context = RuntimeContext()
        list_proc_front = WriteLogFront()
        self._list_proc = WriteLogBack()
        self._list_proc.set_front(list_proc_front)
        
    def run(self, in_code):
        syntax_maker = SyntaxMaker(in_code)
        while True:
            try:
                syntax_node = syntax_maker.get_next()
            except ParserEndException:
                break
            node_name = syntax_node.get_name()
            node_link = self._node_links[node_name]
            executor = self._executors[node_link]            
            executor.run(syntax_node, self._context, self)
        self._list_proc.sync()
                  
    def get_variable(self, in_name):
        return self._context.get_variable(in_name.upper())
        
    def get_node_value(self, node):
        node_name  = node.get_name()
        executor_name = self._node_links[node_name]
        excecutor = self._executors[executor_name]
        result_value, result_type = excecutor.run(node, self._context, self)
        #todo type conversion
        return (result_value, result_type)
    
    def get_math_value(self, node):
        value, type_ = self.get_node_value(node)
        if type_ == runtime.type.NAME:
            value = self._context.get_variable(value)
        return (value, runtime.type.VALUE)
    
    def get_writable_variable(self, node):
        return self.get_math_value(node)
    
    def get_list_proc(self):
        return self._list_proc
    
