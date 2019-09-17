# -*- coding:utf-8 -*-
from abap_parser.context_meta import ContextMeta
from stream_parser import StreamParser
from syntax.compute import SyntaxCompute
from syntax.data import SyntaxData
from syntax.write import SyntaxWrite
from abap_parser.errors import SyntaxException, BadReceiverError, ParserInitException

class CommandParser(StreamParser):
    def __init__(self):
        StreamParser.__init__(self)
        self._syntaxers = []
        self._global_context = ContextMeta()
    def set_source(self, in_source):
        StreamParser.set_source(self, in_source)
        if in_source.get_output_type() != 'command':
            raise ParserInitException()
    def get_output_type(self):
        return 'syntax_command'
    def get_next(self):        
        command = self._source.get_next()
        syntax_node = None
        for syntaxer in self._syntaxers:
            try:
                syntax_node = syntaxer().parse(command)
#             except SyntaxException:
#                 pass
            except BadReceiverError:
                continue
            else:
                break
        if syntax_node == None:
            raise SyntaxException()
        return syntax_node
    
    
class CommandParserDefault(CommandParser):
    
    def __init__(self):
        CommandParser.__init__(self)
        self._syntaxers.append(SyntaxCompute)
        self._syntaxers.append(SyntaxData)
        self._syntaxers.append(SyntaxWrite)
    