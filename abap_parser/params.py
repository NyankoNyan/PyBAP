# -*- coding:utf-8 -*-

import re
import syntax.node.value as sn_value
import syntax.node.name as sn_name


class NoPathError(Exception):
    
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
      
        
class SetupError(Exception):
    
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class NodeIter():
    
    def __init__(self, tokens, index):
        self._tokens = tokens
        self._index = index
    
    def next(self):
        if len(self._tokens) <= self._index+1:
            raise NoPathError()
        return NodeIter(tokens=self._tokens, index=self._index)
    
    def value(self):
        return self._tokens[self._index]
    

class Node():
    
    def __init__(self):
        pass
    
    def parse(self, node_iter):
        raise Exception("Parse method hasn't reailized")
    
    def _concat_names(self, dict_target, dict_ext):
        for (key, value) in dict_ext.items():
            if dict_target.has_key(key):
                dict_target[key] += value
            else:
                dict_target[key] = value
            
                
class Ref(Node):
    
    def __init__(self, child_node, name):
        Node.__init__(self)
        self._child_node = child_node
        self._name = name
        
    def parse(self, node_iter):
        (sub_result, _) = self._child_node.parse(node_iter)
        names = {}
        names[self._name] = sub_result
        return (None, names)
    
    
class Bank(Node):
    
    bank={}
    
    def __init__(self, name):
        Node.__init__(self)
        self._name = name
        
    def parse(self, node_iter):
        return Bank.bank[self._name].parse(node_iter)
    
    @staticmethod
    def save(name, node):
        if Bank.bank.has_key(name):
            raise SetupError()
        Bank.bank[name] = node
        
    
class TokenCond(Node):
    
    def __init__(self, check_func):
        Node.__init__(self=self)
        self._check_func = check_func
        
    def parse(self, node_iter):
        token = node_iter.value()
        if self._check_func(token):
            return (token, {})
        else:
            raise NoPathError()
        
        
class WordCond(TokenCond):
    
    def __init__(self, word):
        TokenCond.__init__(self, lambda x: x['name'] == 'word' and x['body'] == word)
           
    
class SingleNode(Node):
    
    def __init__(self, child_node, obligatory=False, repeat=False):
        Node.__init__(self)
        self._child_node = child_node
        self._obligatory = obligatory
        self._repeat = repeat
        
    def parse(self, node_iter):
        count = 0
        temp_node_iter = node_iter
        ret_names = {}
        while True:
            try:
                _, names = self._child_node.parse(temp_node_iter)
            except NoPathError:
                if self._obligatory:
                    if count > 0:
                        break
                    else:
                        raise NoPathError()
                else:
                    break
            else:
                self._concat_names(ret_names, names)
            if not self._repeat:
                break
            try:
                temp_node_iter = node_iter.next()
            except NoPathError:
                break
            count += 1
        return (None, ret_names)
                
        


class Optional(SingleNode):
    
    def __init__(self, child_node):
        SingleNode.__init__(
            self = self, 
            child_node = child_node,
            obligatory = False,
            repeat = False,
            )
        

class Obligatory(SingleNode):
    
    def __init__(self, child_node):
        SingleNode.__init__(
            self = self, 
            child_node = child_node,
            obligatory = True,
            repeat = False,
            )


class AnyCount(SingleNode):
    
    def __init__(self, child_node):
        SingleNode.__init__(
            self = self, 
            child_node = child_node,
            obligatory = False,
            repeat = True,
            )
        
        
class ListNode(Node):
    
    def __init__(self, children, spaced):
        Node.__init__(self)
        self._children = children
        self._spaced = spaced


class OneOf(ListNode):
    
    def __init__(self, children):
        ListNode.__init__(
            self = self, 
            children = children,
            spaced = False,
            )


class FreeList(ListNode):
    
    def __init__(self, children, spaced=True):
        ListNode.__init__(
            self = self, 
            children = children,
            spaced = spaced,
            )
        
        
class LockedList(ListNode):
    
    def __init__(self, children, spaced=True):
        ListNode.__init__(
            self = self, 
            children = children,
            spaced = spaced,
            ) 
        
        
class Result():
    def __init__(self, child_node, result_func):
        self._child_node = child_node
        self._result_func = result_func
        
        
n_space_opt = AnyCount(TokenCond(lambda x: x['name'] == 'space'))

n_space = SingleNode(
    child_node = TokenCond(lambda x: x['name'] == 'space'),
    obligatory = True,
    repeat = True,
    )

def label(node, name, value=True):
    return Ref(
        Result(
            node,
            lambda _: value,
            ), 
        name,
        )

    
n_var_charval = Result(
    child_node = TokenCond(lambda x: x['name'] == 'charval'),
    result_func = lambda x: sn_value.ValueNode(
        x['body'], 
        sn_value.ValueNode.CHARVAL,
        ),
    )

n_var_string = Result(
    child_node = TokenCond(lambda x: x['name'] == 'string'),
    result_func = lambda x: sn_value.ValueNode(
        x['body'], 
        sn_value.ValueNode.STRING,
        ),
    )

n_var_float = Result(
    child_node = TokenCond(lambda x: x['name'] == 'float' 
                           and re.match(r'[-\+]?[0-9]+.[0-9]+', 
                                        x['body'],
                                        re.IGNORECASE) != None),
    result_func = lambda x: sn_value.ValueNode(
        float(x['body']),
        sn_value.ValueNode.FLOAT,
        )
    )

def is_number(value):
    return all(s in list('0123456789') for s in value)

n_var_number = Result(
    child_node = TokenCond(lambda x: 
                           x['name'] == 'body' 
                           and is_number(x['body'])),
    result_func = lambda x: sn_value.ValueNode(
        int(x['body']),
        sn_value.ValueNode.INT,
        ),
    )

n_var_name = Result(
    child_node = TokenCond(lambda x:
                           x['name'] == 'body'
                           and not is_number(x['body'])),
    result_func = lambda x: sn_name.NameNode(x['body']),
    )
    
n_var = OneOf([
        n_var_number,
        n_var_string,
        n_var_float,
        n_var_charval,
        n_var_name,
    ])

n_int_const = OneOf([
    n_var_number,
    n_var_name,
    ])


n_write = LockedList([
    WordCond('WRITE'),
    Optional(WordCond('/')),
    Ref(n_var, 'source'),
    ])


n_dataname_with_brackets = LockedList(
    children=[
        Ref(n_var_name, 'dataname'),
        Obligatory(WordCond('(')),
        Ref(
            n_int_const,
            'length',
            ),
        Obligatory(WordCond(')')),
        ], 
    spaced=False,
    )

n_data = LockedList([
    WordCond('DATA'),
    OneOf([
        n_dataname_with_brackets,
        Ref(n_var_name, 'dataname'),
        ]),
    Optional(
        LockedList([
            WordCond('TYPE'),
            Ref(n_var_name, 'typename'),
        ])),    
    FreeList([
        LockedList([
            WordCond('LENGTH'),
            Ref(n_int_const, 'length'),
            ]),
        LockedList([
            WordCond('DECIMALS'),
            Ref(n_int_const, 'decimals'),
            ]),
        LockedList([
            WordCond('VALUE'),
            Ref(n_var, 'value'),
            ]),
        Ref(
            Result(
                LockedList(
                    [
                        WordCond('READ'),
                        WordCond('-'),
                        WordCond('ONLY'),
                    ],
                    spaced=False,
                    ),
                lambda _: True
                ), 
            'readonly',
            ),
        LockedList([
            WordCond('OCCURS'),
            Ref(n_var, 'occurs'),
            ]),
        ]),
    ])

n_data_s_begin = LockedList([
    WordCond('DATA'),
    WordCond('BEGIN'),
    WordCond('OF'),
    Ref(n_var_name, 'dataname'),
    ])

n_data_s_end = LockedList([
    WordCond('DATA'),
    WordCond('END'),
    WordCond('OF'),
    Ref(n_var_name, 'dataname'),
    ])

tabkind_standard = 'standard'
tabkind_sorted = 'sorted'
tabkind_hashed = 'hashed'
keykind_unique = 'unique'
keykind_non_unique = 'non-unique'

n_data_tab = LockedList([
    WordCond('DATA'),
    Ref(n_var_name, 'dataname'),
    WordCond('TYPE'),
    Optional(
        OneOf([
            label(WordCond('STANDARD'), 'tabkind', tabkind_standard),
            label(WordCond('SORTED'), 'tabkind', tabkind_sorted),
            label(WordCond('HASHED'), 'tabkind', tabkind_hashed),
            ])
        ),
    WordCond('TABLE'),
    WordCond('OF'),
    Ref(n_var_name, 'typename'),
    Optional(
        LockedList([
            WordCond('WITH'),
            OneOf([
                label(WordCond('UNIQUE'), 'keykind', keykind_unique),
                label(
                    LockedList(
                        [
                            WordCond('NON'),
                            WordCond('-'),
                            WordCond('UNIQUE'),
                        ],
                        spaced=False,
                        ),
                    'keykind',
                    keykind_non_unique,
                    ),
                ]),
            WordCond('KEY'),
            AnyCount(Ref(n_var_name, 'keypart')),
            ])
        ),
    ])

    
n_math_binary = ListNode(
    [
        Ref(Bank('expr_math'), 'operand'),
        n_space,
        OneOf([
            label(WordCond('+'), 'operation', '+'),
            label(WordCond('-'), 'operation', '-'),
            label(WordCond('*'), 'operation', '*'),
            label(WordCond('/'), 'operation', '/'),
            label(WordCond('DIV'), 'operation', 'div'),
            label(WordCond('MOD'), 'operation', 'mod' ),
            ]),
        n_space,
        Ref(Bank('expr_math'), 'operand'),
    ],
    spaced=False,
    )

n_math_unary = ListNode(
    [
        OneOf([
            label(WordCond('+'), 'operation', '+'),
            label(WordCond('-'), 'operation', '-'),
            ]),
        n_space,
        Ref(Bank('expr_math'), 'operand'),
    ],
    spaced=False,
    )

n_math_brackets = Result(
    ListNode(
        [
            WordCond('('),
            n_space,
            Ref(Bank('expr_math'), 'node'),
            n_space,
            WordCond(')'),
        ],
        spaced=False,
        ), 
    lambda x: x['node'][0],
    )

n_expr_math = OneOf([
    n_math_brackets,
    n_math_unary,
    n_math_binary,
    n_var,
    ])
Bank.save('expr_math', n_expr_math)



n_expr_logic_self = []
n_expr_logic = None
n_expr_logic_self[0] = n_expr_logic

n_compute = LockedList([
    Optional(WordCond('COMPUTE')),
    AnyCount(
        LockedList([
            Ref(n_var_name, 'target'),
            WordCond('='),
            ])
        ),
    Ref(n_expr_math, 'expr'),    
    ])