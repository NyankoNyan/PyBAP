# -*- coding:utf-8 -*-

import errors
from string_source import StringSource
from base_tokens_parser import BaseTokensParser
from colon_parser import ColonParser
from name_parser import NameParserDynamicAttr
from name_parser import NameParserOffset
from name_parser import NameParserStaticAttr
from name_parser import NameParserStructComp
from upper_case_parser import UpperCaseParser
from command_parser import CommandParserDefault
from execution.statement import ExecutionStatement
from stream_parser import StreamParser


class ParserStack(StreamParser):
    
    def __init__(self, parsers):
        StreamParser.__init__(self)
        self._parsers = parsers
        for i in range(0, len(self._parsers) - 1):
            self._parsers[i+1].set_source(self._parsers[i])
        
    def get_next(self):
        return self._parsers[-1].get_next()
    
    def set_source(self, in_source):
        self._parsers[0].set_source(in_source)
        
    def get_output_type(self):
        return self._parsers[-1].get_output_type()
        
    
class StringSourceTest():
    def test1(self):
        source = StringSource('Some funny text')
        try:
            while True:
                print str(source.get_next())
        except:
            pass


class BaseTokensParserTest:
    def test1(self):
        self._test('DATA: i1 type i, i2 type i, i3 type i.')
        self._test('i1 = i2 + i3.')
        self._test('write i1.')
    def test2(self):
        self._test('DATA: i1 type i, i2 type i, i3 type i.\ni1 = i2 + i3.\nwrite i1.')
    def test3(self):
        self._test('*this is comment\n"and this')
    def test4(self):
        self._test("var = 'some string text'.")
        self._test("var = `some string text`.")
        self._test("var = 'test with ''quotes'''.")
    def test5(self):
        self._test('formula = - ( ( a + b ) div x ) - length( str ).')
        self._test("call method ('LCL_CLASS')=>('METHOD').")
        self._test("sort x by ('FIELD').")
        self._test('a = b->c( )->d-e.')
        self._test('select a b from zt into: (l1, l2), (l3, l4).')
    def _test(self, in_string):
        source = StringSource(in_string)
        parser = BaseTokensParser()
        parser.set_source(source)
        try:
            while True:
                print str(parser.get_next())
        except errors.ParserEndException:
            print '\n'
        

class ColonParserTest:
    def test1(self):
        self._test('DATA: i1 type i, i2 type i, i3 type i.')
        self._test('write:/:i1:.')
        self._test('select a b from zt into: (l1, l2), (l3, l4).')
    def _test(self, in_string):
        source = StringSource(in_string)
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
        try:
            while True:
                print str(colon_parser.get_next())
        except errors.ParserEndException:
            print '\n'


class NameParserTest:
    def _test(self, in_str):
        source = StringSource(in_str)
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
        try:
            while True:
                print str(parser_offset.get_next())
        except errors.ParserEndException:
            print '\n'
    def test1(self):
        self._test('write a=>b( )->c-d+e(f).')
        self._test("('SOME_CLASS')=>('SOME_METHOD')( ).")
        

class UpperCaseParserTest:
    def test1(self):
        self._test('DATA: i1 type i, i2 type i, i3 type i.')
        self._test('write:/:i1:.')
        self._test('select a b from zt into: (l1, l2), (l3, l4).')
    def _test(self, in_string):
        source = StringSource(in_string)
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
        try:
            while True:
                print str(uppercase_parser.get_next())
        except errors.ParserEndException:
            print '\n'    


class CommandParserTest:
    
    def test1(self):
        self._test('data: i type i, i1 type i, i2 type i. i = i1 + i2.')
        
    def _test(self, in_str):
        source = StringSource(in_str)
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
        try:
            while True:
                print str(command_parser.get_next())
        except errors.ParserEndException:
            print '\n'


class TestExecution:
    
    def test1(self):
        code_execution = ExecutionStatement()
#         code_execution.run('data: i type i, i1 type i, i2 type i. i = i1 + i2.')
        code_execution.run('data: i type i, i1 type i, i2 type i. i1 = 1. i2 = 2. i = i1 + i2 + 3.')        
        print 'i1 =', code_execution.get_variable('i1').value
        print 'i2 =', code_execution.get_variable('i2').value
        print 'i =', code_execution.get_variable('i').value



if __name__ == '__main__':
#     StringSourceTest().test1()
#     BaseTokensParserTest().test1()
#     BaseTokensParserTest().test2()
#     BaseTokensParserTest().test3()
#     BaseTokensParserTest().test4()
#     BaseTokensParserTest().test5()
#     ColonParserTest().test1()
#     NameParserTest().test1()
#     CommandParserTest().test1()
#     UpperCaseParserTest().test1()
    TestExecution().test1()