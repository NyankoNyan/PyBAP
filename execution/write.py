# -*- coding:utf-8 -*-

class ExecutionWrite():
    
    NAME = 'Write'
    
    def run(self, in_syntax_node, in_context, in_code_execution):
        list_proc = in_code_execution.get_list_proc()
        text = str(in_code_execution.get_math_value(in_syntax_node.text_node)[0].value)
        list_proc.write(
            text = text,
            newline = in_syntax_node.new_line,
            )
        