# -*- coding:utf-8 -*-

from .token import Tokens
from abap_parser_old.exceptions import SeriousException, SyntaxException
       
class VarNameSplitter:
    def run_with_list(self, tokens, start_index=0):
        result = []
        for index in range(start_index, len(tokens)):
            token = tokens[index]
            if token['name'] == Tokens.WORD:
                new_tokens = VarNameSplitter.split_var_name(token)
                if len(new_tokens) > 0:
                    result.join(new_tokens)
            else:
                result.append(token.copy())
        return result
    
    @staticmethod
    def split_var_name(token):
        if token['name'] != Tokens.WORD:
            raise SeriousException()
        result_tokens = []
        body = token['body']
        place = body.search('=>')
        if place > 0:
            result_tokens.append({'name':Tokens.WORD, 'body':body[:place]})
        if place >= 0:
            result_tokens.append({'name':Tokens.CLASS_STATIC})
        if place < len(body)-2:
            other_part = body[place+2:]
        if other_part.search('=>') != -1:
            raise SyntaxException()
        while len(other_part) > 0:
            class_symb = other_part.search('->')
            struct_symb = other_part.search('-')
            if struct_symb != -1 and (class_symb == -1 or struct_symb < class_symb):
                if struct_symb == 0 or struct_symb == len(other_part) - 1:
                    raise SyntaxException()
                result_tokens.append({'name':Tokens.WORD, 'body':other_part[:struct_symb]})
                result_tokens.append({'name':Tokens.STRUCT_MEMBER})
                other_part = other_part[struct_symb + 1:]
            elif class_symb != -1:
                if class_symb > 0:
                    result_tokens.append({'name':Tokens.WORD, 'body':other_part[:class_symb]})
                result_tokens.append({'name':Tokens.CLASS_OBJECT})
                if class_symb < len(other_part) - 2:
                    other_part = other_part[class_symb + 2:]
                else:
                    other_part = ''
            else:
                result_tokens.append({'name':Tokens.WORD, 'body':other_part})
                other_part = '' 
