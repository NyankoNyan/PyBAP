# -*- coding:utf-8 -*-

from .__init__ import *

class Workspace:
    
    STATE_DEFAULT = 0
    STATE_COMMENT = 1
    STATE_STRING = 2
    
    LNST_BEGIN = 0
    LNST_OTHER = 1
    
    STRWAIT_DEFAULT = 0
    STRWAIT_WAIT = 1
    
    SYMB_EOF = "EOF"
    SYMB_CEN = "CEN"
    
    SET_SPACE = " \n\t"
    SET_DELIMITER = "()+:.,"
    
    def __init__(self):
        self._buffer = ""
        self._buffer_state = self.STATE_DEFAULT
        self._line_state = self.LNST_BEGIN
        self._string_state = self.STRWAIT_DEFAULT
        self._token_queue = []
        self._command_buffer = []
        self._token = self._create_token("")
        self._syntaxer = Syntaxer()
    
    def send(self,command):
        for symb in command:
            self._parser_1(symb)
        self._parser_1(self.SYMB_CEN)
        self._separate_command()
        #debug      
        self._syntaxer.debug_print()  
        print "BUF:", self._buffer_state, " LINE:", self._line_state, " WAIT:", self._string_state
        
    def _separate_command(self):
        for token in self._token_queue:        
            self._command_buffer.append(token)
            if token['name'] == Tokens.DELIMITER and token['body'][0] == ".":
                self._process_colon(self._command_buffer)
                del self._command_buffer[:]
        del self._token_queue[:]
            
    def _process_colon(self,tokens):
        if len(tokens) == 0:
            return
        commands = self._colon_splitter(tokens)
        for command in commands:
            self._process_command(command)        
            
    def _reduce_spaces(self,a,b):           
        if b['name'] == Tokens.SPACE and (len(a) == 0 or a[-1]['name'] == Tokens.SPACE):   
            pass
        else:
            a.append(b)
        return a  
            
    def _process_command(self, tokens):
        tokens = reduce(self._reduce_spaces, tokens, [])
        if tokens[-1]['name'] == Tokens.SPACE:
            del tokens[-1]        
        self._syntaxer.send(tokens)
        #debug
        #for token in tokens:
        #    print token['name'], "".join(token['body'])
        #print 
    
    def _colon_splitter(self, tokens):
        result_buffer = []
        left_part = []
        right_part = []
        colon_processed = False
        for token in tokens:
            if token['name'] == Tokens.DELIMITER and token['body'][0] == ":":
                if colon_processed == False:
                    left_part.append(self._create_token(Tokens.SPACE))
                colon_processed = True              
            elif colon_processed == False:
                if token['name'] == Tokens.DELIMITER and token['body'][0] == ".":
                    result_buffer.append(left_part[:])
                    del left_part[:]
                else:
                    left_part.append(token)
            else:
                if token['name'] == Tokens.DELIMITER and (token['body'][0] == "," or token['body'][0] == "."):
                    result_buffer.append(left_part + right_part)
                    del right_part[:]
                else: 
                    right_part.append(token)
        return result_buffer
        
    def _create_token(self,name,body=None):
        result = {'name':name}
        if body == None:
            result['body'] = []
        else:
            result['body'] = body
        return result
    
    def _parser_1(self, symb):
        
        comment_breaker = symb == "\n" or symb == self.SYMB_EOF or symb == self.SYMB_CEN
        
        if self._string_state == self.STRWAIT_WAIT and symb != "'":
            self._string_state = self.STRWAIT_DEFAULT
            self._buffer_state = self.STATE_DEFAULT
            self._new_token()
        
        if self._line_state == self.LNST_BEGIN and symb == "*":
            self._buffer_state = self.STATE_COMMENT
            self._new_token(Tokens.COMMENT_BEGIN).append(symb)
            self._new_token(Tokens.COMMENT)
        elif self._buffer_state == self.STATE_DEFAULT and symb == "\"":
            self._buffer_state = self.STATE_COMMENT
            self._new_token(Tokens.COMMENT_BEGIN).append(symb)
            self._new_token(Tokens.COMMENT)            
        elif self._buffer_state == self.STATE_COMMENT and comment_breaker == True:
            self._buffer_state = self.STATE_DEFAULT
            self._new_token()
        elif self._buffer_state == self.STATE_COMMENT:
            self._old_token().append(symb)
        elif self._buffer_state == self.STATE_DEFAULT and comment_breaker == True:
            self._new_token()
        elif self._buffer_state == self.STATE_DEFAULT and symb == "'":
            self._buffer_state = self.STATE_STRING
            self._new_token(Tokens.STRING)
        elif self._buffer_state == self.STATE_STRING and symb == "'" and self._string_state == self.STRWAIT_DEFAULT:
            self._string_state = self.STRWAIT_WAIT
        elif self._buffer_state == self.STATE_STRING and self._string_state == self.STRWAIT_WAIT:
            if symb != "'":
                raise Exception("FUCK YOU!")
            self._string_state = self.STRWAIT_DEFAULT
            self._old_token().append(symb)
        elif self._buffer_state == self.STATE_STRING and comment_breaker == True:
            self._old_token().append(" ")
        elif self._buffer_state == self.STATE_STRING:
            self._old_token().append(symb)
        else:
            self._parser_2(symb)
        
        if comment_breaker == True:
            self._line_state = self.LNST_BEGIN
        else:
            self._line_state = self.LNST_OTHER
                
    def _parser_2(self,symb):
        if symb in self.SET_SPACE:
            self._new_token(Tokens.SPACE)
        elif symb in self.SET_DELIMITER:
            self._new_token(Tokens.DELIMITER).append(symb)
        elif self._token['name'] == Tokens.WORD:
            self._old_token().append(symb)            
        else:
            self._new_token(Tokens.WORD).append(symb)

    
    def _new_token(self, name = ""):
        if self._token['name'] != "" or len(self._token['body']) > 0:
            self._flush_token()
        self._token['name'] = name
        return self._token['body']
    
    def _old_token(self):
        return self._token['body']
    
    def _flush_token(self):
        self._token_queue.append(self._token)
        self._token = self._create_token("")
        
