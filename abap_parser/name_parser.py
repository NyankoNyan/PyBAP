# -*- coding:utf-8 -*-
import errors
from stream_parser import StreamParser


class NameParserBase(StreamParser):
    def __init__(self, in_type_in, in_type_out, in_search_body, in_replace_name):
        StreamParser.__init__(self)
        self._token_buffer = []
        self._last_rbreaket = False 
        self._type_in = in_type_in
        self._type_out = in_type_out
        self._search_body = in_search_body
        self._replace_name = in_replace_name
        self._stream_ended = False
        self._ignore_standalone = False
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
        if in_source.get_output_type() != self._type_in:
            raise errors.ParserInitException()
    def get_output_type(self):
        return self._type_out
    def _parser_step(self):
        token = self._source.get_next()
        if (token['name'] == 'word' 
            and (not self._ignore_standalone 
                 or token['body'] != self._search_body)):
            static_attr_parts = token['body'].split(self._search_body)
            if len(static_attr_parts) == 1:
                self._token_buffer.append(token)
            else:
                if len(static_attr_parts[0]) == 0:
                    if not self._last_rbreaket:
                        raise errors.SyntaxException()
                else:
                    self._token_buffer.append({'name':'word', 'body':static_attr_parts[0]})
                self._token_buffer.append({'name':self._replace_name, 'body':''})    
                for index in range(1, len(static_attr_parts) - 1):
                    if len(static_attr_parts[index]) == 0:
                        raise errors.SyntaxException()
                    self._token_buffer.append({'name':'word', 'body':static_attr_parts[index]})
                    self._token_buffer.append({'name':self._replace_name, 'body':''})
                if len(static_attr_parts[-1]) > 0:
                    self._token_buffer.append({'name':'word', 'body':static_attr_parts[-1]})
        else:
            self._token_buffer.append(token)
        self._last_rbreaket = token['name'] == 'far_rb' or token['name'] == 'solid_rb'
        

class NameParserStaticAttr(NameParserBase):
    def __init__(self):
        NameParserBase.__init__(self, 'base_token_set', 'named_sub1_token_set', '=>', 'static_attr')


class NameParserDynamicAttr(NameParserBase):
    def __init__(self):
        NameParserBase.__init__(self, 'named_sub1_token_set', 'named_sub2_token_set', '->', 'dynamic_attr')


class NameParserStructComp(NameParserBase):
    def __init__(self):
        NameParserBase.__init__(self, 'named_sub2_token_set', 'named_sub3_token_set', '-', 'field')
        
        
class NameParserOffset(NameParserBase):
    def __init__(self):
        NameParserBase.__init__(self, 'named_sub3_token_set', 'named_token_set', '+', 'offset')
        self._ignore_standalone = True
