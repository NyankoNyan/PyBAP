# -*- coding:utf-8 -*-
import errors
from stream_parser import StreamParser

class StringSource(StreamParser):
    def __init__(self, in_string):
        StreamParser.__init__(self)
        self._string = in_string
        self._len = len(in_string)
        self._counter = 0
    def get_next(self):
        if self._counter < self._len:
            symb = self._string[self._counter]
            self._counter += 1
            return symb
        else:
            raise errors.ParserEndException()
    def get_output_type(self):
        return 'symbol'
