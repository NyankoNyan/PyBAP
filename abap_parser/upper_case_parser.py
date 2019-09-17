# -*- coding:utf-8 -*-
import errors
from stream_parser import StreamParser

class UpperCaseParser(StreamParser):
    def __init__(self):
        StreamParser.__init__(self)
    def get_next(self):
        token = self._source.get_next()
        if token['name'] == 'word':
            return {'name':'word', 'body':token['body'].upper()}
        else:
            return token        
    def set_source(self, in_source):
        StreamParser.set_source(self, in_source)
        if in_source.get_output_type() != 'named_token_set':
            raise errors.ParserInitException()
    def get_output_type(self):
        return 'uppercase_token_set'
