import argparse
import ply.lex as lex

# List of token names
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'EQUALS',
    'COLON',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'COMMA',
    'IDENTIFIER',
    'TYPE',
    'STRUCT',
    'NAMESPACE',
    'CLASS',
    'INTERFACE',
    'ACCESS_SPECIFIER',
    'TEMPLATE',
    'LESS_THAN',
    'GREATER_THAN',
    'IF',
    'ELSE',
    'EQ',
    'NEQ',
    'LTE',
    'GTE',
    'INLINE',
    'EXTENDS',
    'NAMESPACE_OPERATOR',
    'FOR',
    'WHILE',
    'FOREACH',
    'LBRACKET',
    'RBRACKET',
    'TYPEDEF',
    'INCLUDE',
    'CONSTRUCTOR',
    'DESTRUCTOR',
    'THIS',
    'INCREMENT',
    'DECREMENT',
    'PREFIX_INCREMENT',
    'PREFIX_DECREMENT',
    'RETURN',
    'OBJECT_INITIALIZATION',
    'OBJECT_DECLARATION',
    'BIT_SHIFT_LEFT',
    'BIT_SHIFT_RIGHT',
    'XOR',
    'AND',
    'OR',
    'MEMBER_ACCESS',
    'MEMBER_FUNCTION_ACCESS',
    'LOGICAL_AND',
    'LOGICAL_OR',
    'TRUE',
    'FALSE',
    'LOGICAL_AND', 
    'LOGICAL_OR',
)

# Regular expression rules for simple tokens
t_PLUS               = r'\+'
t_MINUS              = r'-'
t_TIMES              = r'\*'
t_DIVIDE             = r'/'
t_MOD                = r'%'
t_EQUALS             = r'='
t_COLON              = r':'
t_LPAREN             = r'\('
t_RPAREN             = r'\)'
t_LBRACE             = r'\{'
t_RBRACE             = r'\}'
t_SEMICOLON          = r';'
t_COMMA              = r','
t_IDENTIFIER         = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_ACCESS_SPECIFIER   = r'\b(public|protected|private)\b'
t_LESS_THAN          = r'<'
t_GREATER_THAN       = r'>'
t_EQ                 = r'=='
t_NEQ                = r'!='
t_LTE                = r'<='
t_GTE                = r'>='
t_NAMESPACE_OPERATOR = r'::'
t_LBRACKET           = r'\['
t_RBRACKET           = r'\]'

def t_TYPE(t):
    r'\b(int|void|char|long|uint128|uint256|uint64|uint32|bool)\b'
    return t

def t_STRUCT(t):
    r'\bstruct\b'
    return t

def t_NAMESPACE(t):
    r'\bnamespace\b'
    return t

def t_CLASS(t):
    r'\bclass\b'
    return t

def t_INTERFACE(t):
    r'\binterface\b'
    return t

def t_TEMPLATE(t):
    r'\btemplate\b'
    return t

def t_IF(t):
    r'\bif\b'
    return t

def t_ELSE(t):
    r'\belse\b'
    return t

def t_INLINE(t):
    r'\binline\b'
    return t

def t_EXTENDS(t):
    r'\bextends\b'
    return t

def t_FOR(t):
    r'\bfor\b'
    return t

def t_WHILE(t):
    r'\bwhile\b'
    return t

def t_FOREACH(t):
    r'\bforeach\b'
    return t

def t_TYPEDEF(t):
    r'\btypedef\b'
    return t

def t_INCLUDE(t):
    r'\#include \<[a-zA-Z0-9\.]+\>'
    return t

def t_CONSTRUCTOR(t):
    r'\b([A-Z][a-zA-Z_0-9]*)\b(?=\s*\()'
    return t

def t_DESTRUCTOR(t):
    r'~\b([A-Z][a-zA-Z_0-9]*)\b(?=\s*\()'
    return t

def t_THIS(t):
    r'\bthis->\b'
    return t

def t_INCREMENT(t):
    r'\+\+'
    return t

def t_DECREMENT(t):
    r'--'
    return t

def t_PREFIX_INCREMENT(t):
    r'\+\+[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_PREFIX_DECREMENT(t):
    r'--[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_RETURN(t):
    r'\breturn\b'
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'//.*'
    pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_TRUE(t):
    r'true'
    t.value = True
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    return t

def t_OBJECT_INITIALIZATION(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*\s*(::\s*[a-zA-Z_][a-zA-Z_0-9]*)?\s+[a-zA-Z_][a-zA-Z_0-9]*\s*=\s*[a-zA-Z_][a-zA-Z_0-9]*\s*(::\s*[a-zA-Z_][a-zA-Z_0-9]*)?\s*\([^\)]*\)\s*;'
    return t

def t_OBJECT_DECLARATION(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*\s*(::\s*[a-zA-Z_][a-zA-Z_0-9]*)?\s+[a-zA-Z_][a-zA-Z_0-9]*\s*;'
    return t

def t_BIT_SHIFT_LEFT(t):
    r'<<'
    return t

def t_BIT_SHIFT_RIGHT(t):
    r'>>'
    return t

def t_XOR(t):
    r'\^'
    return t

def t_MEMBER_FUNCTION_ACCESS(t):
    r'\.[a-zA-Z_][a-zA-Z_0-9]*\([^\)]*\)'
    return t

def t_MEMBER_ACCESS(t):
    r'\.[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_LOGICAL_AND(t):
    r'&&'
    return t

def t_LOGICAL_OR(t):
    r'\|\|'
    return t

def t_AND(t):
    r'&'
    return t

def t_OR(t):
    r'\|'
    return t

# Build the lexer
lexer = lex.lex()

