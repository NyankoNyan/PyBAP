# -*- coding:utf-8 -*-


class ExecutorCompute:
    
    NAME = 'Compute'
    
    def run(self, in_syntax_node, in_context, in_code_execution):
        var, _ = in_code_execution.get_node_value(
            in_syntax_node.result)
        for target_node in in_syntax_node.target_list:
            target_var, _ = in_code_execution.get_writable_variable(target_node)
            target_var.value = var.value
        return (True, None)
        #todo add deep analysys for full int operations