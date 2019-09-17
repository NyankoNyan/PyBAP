# -*- coding:utf-8 -*-
import errors
from stream_parser import StreamParser

class BaseTokensParser(StreamParser):
    STATE_DEFAULT = 0
    STATE_COMMENT = 1
    STATE_STRING = 2 
    STATE_CHARSTR = 3
    STATE_TEMPLATE = 4   
    LNST_BEGIN = 0
    LNST_OTHER = 1    
    STRWAIT_DEFAULT = 0
    STRWAIT_WAIT = 1
    BREAKET_NONE = 0
    BREAKET_LEFT = 1
    BREAKET_RIGHT = 2
    def __init__(self):
        StreamParser.__init__(self)
        self._token_buffer = []
        self._stream_ended = False
        self._main_state = self.STATE_DEFAULT    
        self._charstr_state = self.STRWAIT_DEFAULT
        self._string_state = self.STRWAIT_DEFAULT
        self._line_state = self.LNST_BEGIN
        self._symb_buffer = []
        self._last_space = True
        self._breaket_state = self.BREAKET_NONE
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
    def get_output_type(self):
        return 'base_token_set'
    def set_source(self, in_source):
        StreamParser.set_source(self, in_source)
        if in_source.get_output_type() != 'symbol':
            raise errors.ParserInitException()
    def _append_token(self, in_name, in_check_empty = True):
        if in_check_empty and len(self._symb_buffer) == 0:
            return            
        self._token_buffer.append({'name':in_name, 'body':''.join(self._symb_buffer)})
        del self._symb_buffer[:]
    def _parser_step(self):        
        try:
            symb = self._source.get_next()
        except errors.ParserEndException:
            if self._main_state == self.STATE_COMMENT:
                self._append_token('comment')
                self._main_state = self.STATE_DEFAULT
            raise errors.ParserEndException()
        
        if (self._main_state == self.STATE_CHARSTR 
            and self._charstr_state == self.STRWAIT_WAIT 
            and symb != '\''):
            self._charstr_state = self.STRWAIT_DEFAULT
            self._main_state = self.STATE_DEFAULT
            self._append_token('charstr', False)
            
        if self._breaket_state == self.BREAKET_LEFT:
            if symb in set('\n .,:'):
                if self._space_before:
                    self._append_token('single_lb', False)
                else:
                    self._append_token('close_lb', False)
            else:
                if self._space_before:
                    self._append_token('far_lb', False)
                else:
                    self._append_token('solid_lb', False)
            self._breaket_state = self.BREAKET_NONE
            
        if self._breaket_state == self.BREAKET_RIGHT:
            if symb in set('\n .,:'):
                if self._space_before:
                    self._append_token('single_rb', False)
                else:
                    self._append_token('close_rb', False)
            else:
                if self._space_before:
                    self._append_token('far_rb', False)
                else:
                    self._append_token('solid_rb', False)
            self._breaket_state = self.BREAKET_NONE
        
        if self._main_state == self.STATE_DEFAULT:
            if symb == '*' and self._line_state == self.LNST_BEGIN:
                self._main_state = self.STATE_COMMENT
                self._symb_buffer.append(symb)
                self._append_token('comment_begin')
            elif symb == '"':
                self._append_token('word')
                self._main_state = self.STATE_COMMENT
                self._symb_buffer.append(symb)
                self._append_token('comment_begin')  
            elif symb == '\'':
                if len(self._symb_buffer) > 0:
                    raise errors.SyntaxException()
                self._main_state = self.STATE_CHARSTR
            elif symb == '`':   
                if len(self._symb_buffer) > 0:
                        raise errors.SyntaxException()
                self._main_state = self.STATE_STRING   
            elif symb == '|':
                raise errors.SyntaxException()
                if len(self._symb_buffer) > 0:
                        raise errors.SyntaxException()
                self._main_state = self.STATE_TEMPLATE    
            elif symb == ' ' or symb == '\n':
                self._append_token('word')
            elif symb in set('.:,'):
                self._append_token('word')
                self._symb_buffer.append(symb)
                self._append_token('special')
            elif symb == '(':
                self._append_token('word')
                self._space_before = self._last_space
                self._breaket_state = self.BREAKET_LEFT
            elif symb == ')':
                self._append_token('word')
                self._space_before = self._last_space
                self._breaket_state = self.BREAKET_RIGHT
            else:
                self._symb_buffer.append(symb)
        elif self._main_state == self.STATE_COMMENT:
            if symb == '\n':
                self._append_token('comment', False)
                self._main_state = self.STATE_DEFAULT
            else:
                self._symb_buffer.append(symb)            
        elif self._main_state == self.STATE_CHARSTR:            
            if symb == '\'':
                if self._charstr_state == self.STRWAIT_WAIT:
                    self._charstr_state = self.STRWAIT_DEFAULT
                    self._symb_buffer.append(symb)
                else:
                    self._charstr_state = self.STRWAIT_WAIT
            else:
                self._symb_buffer.append(symb)
        elif self._main_state == self.STATE_STRING:
            if symb == '`':
                self._append_token('string', False)
                self._main_state = self.STATE_DEFAULT
            else:
                self._symb_buffer.append(symb)
        else:
            raise errors.SyntaxException()
        
        if symb == '\n':
            self._line_state = self.LNST_BEGIN
        else:
            self._line_state = self.LNST_OTHER
            
        self._last_space = symb in set('\n .,:')
