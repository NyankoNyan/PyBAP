# -*- coding:utf-8 -*-

class ParseError(Exception):
    pass

class ConstParse:

    @staticmethod
    def convert_numeric(in_str):
        if not in_str.isdigit():
            raise ValueError()
        return in_str
    
    @staticmethod
    def convert_float(in_str):
        try:
            return float(in_str)
        except ValueError:
            raise ParseError()
        
    @staticmethod
    def convert_int(in_str):
        try:
            return int(in_str)
        except ValueError:
            raise ParseError()
        