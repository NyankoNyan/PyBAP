# -*- coding:utf-8 -*-

class Tokens:

    DELIMITER = 'delimiter'
    SPACE = 'space'
    COMMENT = 'comment'
    COMMENT_BEGIN = 'comment_begin'
    STRING = 'string'
    WORD = 'word'
    OFFSET_PLUS = 'offset_plus'
    LB_SINGLE = 'lb_single' # _ ( _
    LB_CLOSE = 'lb_close' # _( _
    LB_SOLID = 'lb_solid' # _(_
    LB_FAR = 'lb_far' # _ (_
    RB_SINGLE = 'rb_single' # _ ) _
    RB_CLOSE = 'rb_close' # _) _
    RB_SOLID = 'rb_solid' # _)_
    RB_FAR = 'rb_far' # _ )_
    CLASS_STATIC = 'class_statis'
    CLASS_OBJECT = 'class_object'
    STRUCT_MEMBER = 'struct_member'
    
    @staticmethod
    def dissolve(tokens, index):
        del tokens[index]

