# -*- coding:utf-8 -*-

from abap_parser.errors import ParserEndException


class ExpressionSource:
    def __init__(self, in_token_list, in_base_index):
        self._token_list = in_token_list
        self._index = in_base_index
    def get_next(self):
        if self._index < len(self._token_list):
            token = self._token_list[self._index]
            self._index += 1
            return token
        else:
            raise ParserEndException()
    def get_index(self):
        return self._index
    def is_end(self):
        return self._index >= len(self._token_list)  