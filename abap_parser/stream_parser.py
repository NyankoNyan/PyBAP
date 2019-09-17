# -*- coding:utf-8 -*-

import errors

class StreamParser:
    def __init__(self):
        self._source = None
    def get_next(self):
        return None
    def set_source(self, in_source):
        if not isinstance(in_source, StreamParser):
            raise errors.ParserInitException()
        self._source = in_source
    def get_output_type(self):
        return None