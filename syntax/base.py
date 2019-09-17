# -*- coding:utf-8 -*-
from abap_parser.errors import SeriousException

class SyntaxBase:
    #def __init__(self, in_context_meta):
    #    self._context_meta = in_context_meta
    def parse(self, in_command):
        raise SeriousException()