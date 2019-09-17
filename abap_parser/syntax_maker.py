# -*- coding:utf-8 -*-

from string_source import StringSource
from base_tokens_parser import BaseTokensParser
from colon_parser import ColonParser
from name_parser import NameParserDynamicAttr
from name_parser import NameParserOffset
from name_parser import NameParserStaticAttr
from name_parser import NameParserStructComp
from upper_case_parser import UpperCaseParser
from command_parser import CommandParserDefault


class SyntaxMaker:
    def __init__(self, in_code):
        source = StringSource(in_code)
        base_parser = BaseTokensParser()
        base_parser.set_source(source)
        static_attr = NameParserStaticAttr()
        static_attr.set_source(base_parser)
        dynamic_attr = NameParserDynamicAttr()
        dynamic_attr.set_source(static_attr)
        struct_comp = NameParserStructComp()
        struct_comp.set_source(dynamic_attr)
        parser_offset = NameParserOffset()
        parser_offset.set_source(struct_comp)
        uppercase_parser = UpperCaseParser()
        uppercase_parser.set_source(parser_offset)
        colon_parser = ColonParser()
        colon_parser.set_source(uppercase_parser)        
        command_parser = CommandParserDefault()
        command_parser.set_source(colon_parser)
        self._command_parser = command_parser
    def get_next(self):
        return self._command_parser.get_next()