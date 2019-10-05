# -*- coding:utf-8 -*-
import errors
from stream_parser import StreamParser


class RemoveCommentParser(StreamParser):
    
    def __init__(self):
        StreamParser.__init__(self)
        self._token_buffer = []
        self._stream_ended = False
        
    def get_next(self):
        if not self._stream_ended:
            try:
                while len(self._token_buffer) == 0:
                    self._parser_step()
            except errors.ParserEndException:
                self._stream_ended = True
        if len(self._token_buffer) == 0:
            raise errors.ParserEndException()
        else:
            return self._token_buffer.pop(0)
        
    def set_source(self, in_source):
        StreamParser.set_source(self, in_source)
        if in_source.get_output_type() != 'dict_token':
            raise errors.ParserInitException()
        
    def get_output_type(self):
        return 'dict_token'
    
    def _parser_step(self):
        token = self._source.get_next()
        if token['name'] not in ('comment', 'comment_begin'):
            self._token_buffer.append(token)