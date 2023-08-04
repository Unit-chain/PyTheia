import argparse
import ply.lex as lex


states = (
    ('namespace', 'inclusive'),
    ('interface', 'exclusive'),
    ('parameter', 'exclusive'),
    ('struct', 'inclusive'),
    ('function', 'inclusive')
)

state_stack = []

tokens = (
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LANGLE',
    'RANGLE',
    'SEMICOLON',
    'COMMA',
    'DOT',
    'COLON',
    'DOUBLE_COLON',
    'QUOTE',
    'DOUBLE_QUOTE',
    'EQ',
    'NEQ',
    'GT',
    'LT',
    'GTE',
    'LTE',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'POW',
    'LSHIFT',
    'RSHIFT',
    'EQUALS',
    'LOGICAL_OP',
    'INTEGER',
    'HEX',
    'FLOAT',
    'TYPE',
    'TYPEDEF',
    'BOOLEAN',
    'NAMESPACE',
    'INTERFACE',
    'TEMPLATE',
    'STRUCT',
    'THIS',
    'CONSTRUCTOR',
    'DESTRUCTOR',
    'IMPLEMENTS',
    'RETURN',
    'VISIBILITY',
    'IDENTIFIER',
    'CHAR',
)

#----INITIAL RULES----#

t_LBRACE        = r'\{'
t_RBRACE        = r'\}'

def t_LPAREN(t):
    r'\('
    state_stack.append(t.lexer.current_state())
    t.lexer.begin('parameter')
    return t

t_RPAREN        = r'\)'
t_LBRACKET      = r'\['
t_RBRACKET      = r'\]'
t_LANGLE        = r'\<'
t_RANGLE        = r'\>'
t_SEMICOLON     = r'\;'
t_COMMA         = r'\,'
t_DOT           = r'\.'
t_COLON         = r'\:'
t_DOUBLE_COLON  = r'\:\:'
t_QUOTE         = r"\'"
t_DOUBLE_QUOTE  = r'\"'
t_EQ            = r'\=\='
t_NEQ           = r'\!\='
t_GT            = r'\>'
t_LT            = r'\<'
t_GTE           = r'\>\='
t_LTE           = r'\<\='
t_PLUS          = r'\+'
t_MINUS         = r'\-'
t_TIMES         = r'\*'
t_DIVIDE        = r'\/'
t_MOD           = r'\%'
t_POW           = r'\*\*'
t_LSHIFT        = r'\<\<'
t_RSHIFT        = r'\>\>'
t_EQUALS        = r'\='

def t_LOGICAL_OP(t):
    r'\b(and|\&\&|or|\|\|)'    
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_HEX(t):
    r'0x[0-9a-fA-F]+'
    t.value = int(t.value, 16)  # Convert the hex string to an integer
    return t

def t_FLOAT(t):
    r'\d*\.\d+([eE][-+]?\d+)?'
    t.value = float(t.value)
    return t

def t_TYPE(t):
    r'\b(bool|int|void|char|long|uint128|uint256|uint64|uint32)\b'
    return t

def t_TYPEDEF(t):
    r'\btypedef\b'
    return t

def t_BOOLEAN(t):
    r'\b(true|false)\b'
    t.value = True if t.value == 'true' else False
    return t

def t_NAMESPACE(t):
    r'\bnamespace\b'
    state_stack.append(t.lexer.current_state())
    t.lexer.begin('namespace')
    return t

def t_INTERFACE(t):
    r'\binterface\b'
    state_stack.append(t.lexer.current_state())
    t.lexer.begin('interface')
    return t

def t_TEMPLATE(t):
    r'\btemplate\b'
    return t

def t_STRUCT(t):
    r'\bstruct\b'
    state_stack.append(t.lexer.current_state())
    t.lexer.begin('struct')
    print(t.lexer.current_state())
    return t

def t_IMPLEMENTS(t):
    r'\bimplements\b'
    return t

def t_RETURN(t):
    r'\breturn\b'
    return t

def t_COMMENT(t):
    r'//.*'
    pass

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # print(t.lexer.lineno, t.value, state_stack, t.lexer.current_state())
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

t_ignore  = ' \t'

#-----NAMESPACE RULES-----#

def t_namespace_RBRACE(t):
    r'\}'
    t.lexer.begin(state_stack.pop()) 
    return t

#-----INTERFACE RULES-----#

def t_interface_TYPE(t):
    r'\b(bool|int|void|char|long|uint128|uint256|uint64|uint32)\b'
    return t

def t_interface_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

t_interface_LBRACE          = r'\{'

def t_interface_LPAREN(t):
    r'\('
    state_stack.append(t.lexer.current_state())
    t.lexer.begin('parameter')
    return t

t_interface_DOUBLE_COLON    = r'\:\:'
t_interface_SEMICOLON       = r'\;'

def t_interface_RBRACE(t):
    r'\}'
    t.lexer.begin(state_stack.pop()) 
    return t

def t_interface_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_interface_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

t_interface_ignore  = ' \t'

#-----PARAMETER RULES-----#

t_parameter_DOUBLE_COLON    = r'\:\:'
t_parameter_COMMA           = r'\,'

def t_parameter_TYPE(t):
    r'\b(bool|int|void|char|long|uint128|uint256|uint64|uint32)\b'
    return t

def t_parameter_RPAREN(t):
    r'\)'
    t.lexer.begin(state_stack.pop()) 
    return t

def t_parameter_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_parameter_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_parameter_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

t_parameter_ignore  = ' \t'

#-----STRUCT RULES-----#

def t_struct_CONSTRUCTOR(t):
    r'\bconstructor\b'
    return t

def t_struct_DESTRUCTOR(t):
    r'\bdestructor\b'
    return t

def t_struct_VISIBILITY(t):
    r'\b(hidden)\b'
    return t

def t_struct_TEMPLATE(t):
    r'\btemplate\b'
    print(t.lexer.lineno)
    raise SyntaxError("temlate is not allowed inside of a class")

def t_struct_LPAREN(t):
    r'\('
    state_stack.append(t.lexer.current_state())
    t.lexer.begin('parameter')
    return t

def t_struct_RBRACE(t):
    r'\}'
    t.lexer.begin(state_stack.pop()) 
    return t

#-----FUNCTION RULES----#

def t_function_RBRACE(t):
    r'\}'
    t.lexer.begin(state_stack.pop()) 
    return t

def t_function_NAMESPACE(t):
    r'\bnamespace\b'
    t_error(t)

def t_function_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_function_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

t_function_ignore  = ' \t'

def t_CHAR(t):
    r'\'.\''
    return t

lexer = lex.lex(optimize=1)