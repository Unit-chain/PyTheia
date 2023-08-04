from ply import yacc
from lexer import tokens
from lexer import state_stack


# INITIAL state

# Start
def p_program(p):
    '''program : statements'''
    p[0] = p[1]

# Allows for an empty functions
def p_empty(p):
    'empty :'
    p[0] = None

# Error handling
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' at line {p.lineno}, position {p.lexpos}")
    else:
        print("Syntax error at EOF")

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2: # Single statement
        p[0] = [p[1]]
    else: # Recursive case
        p[0] = p[1] + [p[2]]

# Statemets
def p_statement(p):
    '''statement : typedef
                 | namespace
                 | interface
                 | struct
                 | function
                 | constructor
                 | destructor
                 | variable
                 | empty'''
    p[0] = p[1]

# What can be used as type of a variable/function
def p_types(p):
    '''types : TYPE
             | object_accessor'''
    p[0] = p[1]

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | expression LOGICAL_OP expression
                  | expression LSHIFT expression
                  | expression RSHIFT expression
                  | constant_expression'''  # Use constant_expression instead of NUMBER
    if len(p) == 2:  # If it's a single constant expression
        p[0] = p[1]
    else:  # If it's a binary operation
        p[0] = (p[1], p[2], p[3])

def p_constant_expression(p):
    '''constant_expression : INTEGER
                           | FLOAT
                           | BOOLEAN
                           | HEX
                           | char'''  # Include all your literal types here
    p[0] = p[1]

def p_char(p):
    '''char : INTEGER
            | CHAR'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

# parameters of function
def p_parameters(p):
    '''parameters : parameter
                  | parameters COMMA parameter
                  | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# parameters helper function to help with recursion
def p_parameter(p):
    'parameter : types IDENTIFIER'
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

# function handler
def p_function(p):
    'function : types IDENTIFIER LPAREN parameters RPAREN LBRACE statements RBRACE SEMICOLON'
    state_stack.append(p.lexer.current_state())
    p.lexer.begin('function')
    p[0] = (p[1], p[2], p[4], p[7])

# Defines function for interface
def p_interface_functions(p):
    '''interface_functions : interface_function
                           | interface_functions interface_function'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# functions Helper function to help with recursion
def p_interface_function(p):
    'interface_function : types IDENTIFIER LPAREN parameters RPAREN SEMICOLON'
    p[0] = (p[1], p[2], p[4])


# Access to user defined objects (including namespaces)
def p_object_accessor(p):
    '''object_accessor : IDENTIFIER
                       | object_accessor DOUBLE_COLON IDENTIFIER'''
    if len(p) == 2:  # Single identifier, base case
        p[0] = p[1]
    else:  # Recursive case
        p[0] = p[1] + p[2] + p[3]

# typedef keyword
def p_typedef(p):
    'typedef : TYPEDEF types IDENTIFIER SEMICOLON'
    p[0] = (p[1], p[2], p[3])

# namespace keyword
def p_namespace(p):
    'namespace : NAMESPACE IDENTIFIER LBRACE statements RBRACE'
    p[0] = (p[1], p[2], p[4])

# interface keyword
def p_interface(p):
    'interface : INTERFACE IDENTIFIER LBRACE interface_functions RBRACE SEMICOLON'
    p[0] = (p[1], p[2], p[4])

def p_constructor(p):
    'constructor : CONSTRUCTOR LPAREN parameters '

def p_destructor(p):
    'destructor : DESTRUCTOR LPAREN parameters '

def p_template_declaration_params(p):
    '''template_declaration_params : IDENTIFIER
                                   | template_declaration_params COMMA IDENTIFIER'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_template_accessor_params(p):
    '''template_accessor_params : types
                                | template_accessor_params COMMA IDENTIFIER'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_template_declaration(p):
    '''template_declaration : empty
                            | TEMPLATE LANGLE template_declaration_params RANGLE'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[3])

def p_template_accessor(p):
    '''template_accessor : TEMPLATE LANGLE template_accessor_params RANGLE
                         | empty''' 
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[3])

def p_implements(p):
    '''implements : IMPLEMENTS IDENTIFIER
                  | empty'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_variable(p):
    '''variable : types IDENTIFIER SEMICOLON
                | types IDENTIFIER EQUALS expression SEMICOLON'''
    if len(p) == 4:
        p[0] = (p[1], p[2])
    else:
        p[0] = (p[1], p[2], p[4])

def p_struct(p):
    'struct : template_declaration STRUCT IDENTIFIER implements LBRACE statement RBRACE'
    p[0] = (p[1], p[2], p[3], p[4] ,p[6])

parser = yacc.yacc(debug=True)