# -*- coding:utf-8 -*-


class ParserInitException(Exception):
    pass


class ParserEndException(Exception):
    pass


class SyntaxException(Exception):
    pass


class SeriousException(Exception):
    pass


class TodoException(Exception):
    pass


class BadReceiverError(Exception):
    pass