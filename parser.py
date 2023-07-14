from ply import yacc
from lexer import tokens  # assuming your lexer is in lexer.py

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'BIT_SHIFT_RIGHT', 'BIT_SHIFT_LEFT', 'AND', 'OR', 'XOR'),
)

def p_program(p):
    '''program : statement
               | program statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement_typedef(p):
    'statement : TYPEDEF TYPE IDENTIFIER SEMICOLON'
    p[0] = ('typedef', p[2], p[3])

def p_statement_namespace(p):
    'statement : NAMESPACE IDENTIFIER LBRACE statements RBRACE'
    p[0] = ('namespace', p[2], p[4])

def p_statements(p):
    '''statements : statement
                  | statements statement
                  | empty'''
    if len(p) == 2:  # The empty rule
        if p[1] == ('empty',):
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_template(p):
    'template : TEMPLATE LESS_THAN IDENTIFIER GREATER_THAN'
    p[0] = ('template', p[3])

def p_statement_template_struct(p):
    'statement : template STRUCT IDENTIFIER LBRACE members RBRACE SEMICOLON'
    p[0] = ('template_struct', p[1], ('struct', p[3], p[5]))


def p_statement_struct(p):
    'statement : STRUCT IDENTIFIER LBRACE members RBRACE SEMICOLON'
    p[0] = ('struct', p[2], p[4])        

def p_member(p):
    'member : TYPE IDENTIFIER SEMICOLON'
    p[0] = ('member', p[1], p[2])

def p_members(p):
    '''members : member
               | members member
               | method_declaration
               | members method_declaration
               | access_specifier_block
               | members access_specifier_block'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_access_specifier_block(p):
    'access_specifier_block : ACCESS_SPECIFIER COLON members'
    p[0] = ('access_specifier_block', p[1], p[3])

def p_method_declaration(p):
    'method_declaration : TYPE IDENTIFIER LPAREN parameters RPAREN SEMICOLON'
    p[0] = ('method_declaration', p[1], p[2], p[4])

def p_statement_function_no_params(p):
    'statement : TYPE IDENTIFIER LPAREN RPAREN LBRACE statements RBRACE'
    p[0] = ('function', p[1], p[2], [], p[6])

def p_statement_function(p):
    'statement : TYPE IDENTIFIER LPAREN parameters RPAREN LBRACE statements RBRACE'
    p[0] = ('function', p[1], p[2], p[4], p[7])

def p_parameters(p):
    '''parameters : TYPE IDENTIFIER
                  | parameters COMMA TYPE IDENTIFIER'''
    if len(p) == 3:
        p[0] = [(p[1], p[2])]
    else:
        p[0] = p[1] + [(p[3], p[4])]

def p_statement_assign(p):
    'statement : IDENTIFIER EQUALS expression SEMICOLON'
    p[0] = ('assign', p[1], p[3])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LESS_THAN expression
                  | expression GREATER_THAN expression
                  | expression LTE expression
                  | expression GTE expression
                  | expression BIT_SHIFT_RIGHT expression
                  | expression BIT_SHIFT_LEFT expression
                  | expression AND expression
                  | expression OR expression
                  | expression XOR expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = ('id', p[1])    

def p_statement_return(p):
    'statement : RETURN expression SEMICOLON'
    p[0] = ('return', p[2])

def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN LBRACE statements RBRACE'
    p[0] = ('if', p[3], p[6])

def p_statement_if_else(p):
    'statement : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE'
    p[0] = ('if-else', p[3], p[6], p[10])

def p_statement_increment(p):
    'statement : IDENTIFIER INCREMENT SEMICOLON'
    p[0] = ('increment', p[1])

def p_statement_decrement(p):
    'statement : IDENTIFIER DECREMENT SEMICOLON'
    p[0] = ('decrement', p[1])

def p_statement_prefix_increment(p):
    'statement : INCREMENT IDENTIFIER SEMICOLON'
    p[0] = ('prefix_increment', p[2])

def p_statement_prefix_decrement(p):
    'statement : DECREMENT IDENTIFIER SEMICOLON'
    p[0] = ('prefix_decrement', p[2])

def p_declaration(p):
    'declaration : TYPE IDENTIFIER SEMICOLON'
    p[0] = ('declare', p[1], p[2])

def p_declaration_init(p):
    'declaration : TYPE IDENTIFIER EQUALS expression SEMICOLON'
    p[0] = ('declare_init', p[1], p[2], p[4])

def p_statement_declaration(p):
    'statement : declaration'
    p[0] = p[1]

def p_expression_bool(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = ('bool', p[1])

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LBRACE statements RBRACE'
    p[0] = ('while', p[3], p[6])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number', p[1])

def p_statement_interface(p):
    'statement : INTERFACE IDENTIFIER LBRACE members RBRACE SEMICOLON'
    p[0] = ('interface', p[2], p[4])

def p_constructor(p):
    'constructor : CONSTRUCTOR LPAREN parameters RPAREN LBRACE statements RBRACE'
    p[0] = ('constructor', p[3], p[6])

def p_destructor(p):
    'destructor : DESTRUCTOR LPAREN RPAREN LBRACE statements RBRACE'
    p[0] = ('destructor', p[6])

def p_statement_method_implementation(p):
    'statement : IDENTIFIER COLON COLON IDENTIFIER LPAREN parameters RPAREN LBRACE statements RBRACE'
    p[0] = ('method_impl', p[1], p[4], p[6], p[9])

def p_statement_function_call(p):
    'statement : IDENTIFIER DOT IDENTIFIER LPAREN parameters RPAREN SEMICOLON'
    p[0] = ('function_call', p[1], p[3], p[5])
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' at line {p.lineno}, position {p.lexpos}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

