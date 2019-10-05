# -*- coding:utf-8 -*-

from abap_parser.string_source import StringSource
from abap_parser.errors import ParserEndException
from abap_parser.base_tokens_parser import BaseTokensParserS
from abap_parser.stream import ParserStack
from abap_parser.colon_parser import ColonParserS
from abap_parser.remove_comment import RemoveCommentParser


class ParserTest:
    
    def __init__(self, parser):
        self._parser = parser
    
    def from_file(self, file_name):
        result = []
        cfile = open(file_name, 'r')
        if cfile.mode == 'r':
            source = StringSource(cfile.read())
            self._parser.set_source(source)
            while True:
                try:
                    result.append(self._parser.get_next())
                except ParserEndException:
                    break
        cfile.close()
        return result
        

def rep_tokens(tokens):
    return ''.join([
        token['name']+'\t'+token['body']+'\n' 
        for token in tokens
        ])
    
def rep_commands(commands):
    return ''.join([
        'command:\n'+''.join([
            '\t'+token['name']+'\t'+token['body']+'\n'
            for token in command
            ])
        for command in commands
        ])
    
    
def output_rep(file_name, content):
    cfile = open(file_name, 'w')
    if cfile.mode == 'w':
        cfile.write(content)
    cfile.close()


def test_file_parse(module_file):
    ptest = ParserTest(
        ParserStack([
            BaseTokensParserS(),
            RemoveCommentParser(),
            ColonParserS(),
            ])
        )
    pres = ptest.from_file(
        '../test_codes/'+module_file+'.abap'
        )
    output_rep(
        'output/'+module_file+'_tokens.txt', 
        rep_commands(pres),
        )


def test():
    test_file_parse('first_file_test')
    
    
if __name__ == "__main__":
    test()