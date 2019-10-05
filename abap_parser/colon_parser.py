# -*- coding:utf-8 -*-
import errors
from stream_parser import StreamParser

class ColonParser(StreamParser):
    def __init__(self):
        StreamParser.__init__(self)
        self._command_buffer = []
        self._left_part = []
        self._left_complete = False
        self._tuple_count = 0
        self._right_part = []
    def get_next(self):
        while len(self._command_buffer) == 0:
            self._parser_step()
        return self._command_buffer.pop(0)
    def set_source(self, in_source):
        StreamParser.set_source(self, in_source)
        if in_source.get_output_type() != 'uppercase_token_set':
            raise errors.ParserInitException()
    def get_output_type(self):
        return 'command'
    def _append_token(self, in_token):
        if self._left_complete:
            self._right_part.append(in_token)
        else:
            self._left_part.append(in_token)
    def _append_command(self, in_end):
        if self._tuple_count != 0:
            raise errors.SeriousException()
        self._command_buffer.append(self._left_part + self._right_part)    
        del self._right_part[:]
        if in_end:
            del self._left_part[:]
            self._left_complete = False        
    def _parser_step(self):
        token = self._source.get_next()
        if token['name'] == 'special':
            if token['body'] == ':':
                self._left_complete = True
            elif token['body'] == ',':
                if self._tuple_count == 0 or not self._left_complete:
                    self._append_command(False)
                else:
                    self._append_token({'name':'word', 'body':','})
            elif token['body'] == '.':
                self._append_command(True)
            else:
                raise errors.SeriousException()
        elif token['name'] == 'far_lb':
            self._append_token(token)
            self._tuple_count += 1
        elif token['name'] == 'close_rb':
            self._append_token(token)
            self._tuple_count -= 1
        else:
            self._append_token(token)
            
            
class ColonParserS(StreamParser):
    
    def __init__(self):
        StreamParser.__init__(self)
        self._command_buffer = []
        self._left_part = []
        self._left_complete = False
        self._tuple_count = 0
        self._right_part = []
        
    def get_next(self):
        while len(self._command_buffer) == 0:
            self._parser_step()
        return self._command_buffer.pop(0)
    
    def set_source(self, in_source):
        StreamParser.set_source(self, in_source)
        if in_source.get_output_type() != 'dict_token':
            raise errors.ParserInitException()
        
    def get_output_type(self):
        return 'command'
    
    def _append_token(self, in_token):
        if self._left_complete:
            self._right_part.append(in_token)
        else:
            self._left_part.append(in_token)
            
    def _append_command(self, in_end):
        if self._tuple_count != 0:
            raise errors.SeriousException()
        self._command_buffer.append(self._left_part + self._right_part)    
        del self._right_part[:]
        if in_end:
            del self._left_part[:]
            self._left_complete = False
                    
    def _parser_step(self):
        token = self._source.get_next()
        if token['name'] == 'special':
            if token['body'] == ':':
                self._left_complete = True
                self._append_token({'name':'space', 'body':''})
            elif token['body'] == ',':
                if self._tuple_count == 0 or not self._left_complete:
                    self._append_command(False)
                else:
                    self._append_token({'name':'word', 'body':','})
            elif token['body'] == '.':
                self._append_command(True)
            else:
                raise errors.SeriousException()
        else:
            self._append_token(token)
                        