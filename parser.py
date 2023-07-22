from ply import yacc
from lexer import tokens  # assuming your lexer is in lexer.py

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
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
    '''statements : statement_list
                  | empty'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_template(p):
    'template : TEMPLATE LESS_THAN IDENTIFIER GREATER_THAN'
    p[0] = ('template', p[3])

def p_statement_template_struct(p):
    '''statement : template STRUCT IDENTIFIER LBRACE members RBRACE SEMICOLON
                 | template STRUCT IDENTIFIER IMPLEMENTS IDENTIFIER LBRACE members RBRACE SEMICOLON'''
    if len(p) == 8:
        p[0] = ('template_struct', p[1], ('struct', p[3], p[5]))
    else:
        p[0] = ('template_struct', p[1], ('struct', p[3], 'implements', p[5], p[7]))

def p_statement_struct(p):
    '''statement : STRUCT IDENTIFIER LBRACE members RBRACE SEMICOLON
                 | STRUCT IDENTIFIER IMPLEMENTS IDENTIFIER LBRACE members RBRACE SEMICOLON'''
    if len(p) == 7:
        p[0] = ('struct', p[2], p[4])
    else:
        p[0] = ('struct', p[2], 'implements', p[4], p[6])

def p_member(p):
    '''member : variable_declaration
              | method_declaration
              | access_specifier
              | constructor
              | destructor'''
    if len(p) == 3:  # If it's an access_specifier.
        p[0] = ('member', p[1], p[2])        
    else:  # If it's a variable_declaration or method_declaration.
        p[0] = ('member', p[1])

def p_access_specifier(p):
    '''access_specifier : HIDDEN COLON'''
    p[0] = ('access_specifier', p[1])

# Change the members_with_access_specifier rule to use the new access_specifier rule
def p_members_with_access_specifier(p):
    'members_with_access_specifier : access_specifier members'
    p[0] = (p[1], p[2])

def p_members(p):
    '''members : member
               | members member
               | method_declaration
               | members method_declaration
               | members_with_access_specifier
               | members members_with_access_specifier'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_variable_declaration(p):
    '''variable_declaration : TYPE IDENTIFIER SEMICOLON
                            | access_specifier variable_declaration'''
    p[0] = ('variable_declaration', p[1], p[2])

def p_method_declaration(p):
    '''method_declaration : TYPE IDENTIFIER LPAREN parameters RPAREN SEMICOLON
                          | TYPE IDENTIFIER LPAREN parameters RPAREN LBRACE statements RBRACE
                          | TYPE IDENTIFIER LPAREN RPAREN LBRACE statements RBRACE
                          | TYPE IDENTIFIER LPAREN RPAREN SEMICOLON 
                          | access_specifier method_declaration'''
    if len(p) == 6:  # If it's a method declaration without parameters and with a semicolon.
        p[0] = ('method_declaration', p[1], p[2], [])
    elif len(p) == 7:  # If it's a method declaration with parameters and with a semicolon.
        p[0] = ('method_declaration', p[1], p[2], p[4])
    elif len(p) == 8:  # If it's a method declaration without parameters and with a body.
        p[0] = ('method_declaration', p[1], p[2], [], p[6])
    elif len(p) == 9:  # If it's a method declaration with parameters and with a body.
        p[0] = ('method_declaration', p[1], p[2], p[4], p[7])
    else:  # If it's an access_specifier followed by a method_declaration.
        p[0] = ('method_declaration', p[1], p[2])

def p_parameters(p):
    '''parameters : parameter_list
                  | empty'''
    p[0] = p[1]

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA TYPE IDENTIFIER
                      | TYPE IDENTIFIER'''
    if len(p) == 3:
        p[0] = [(p[1], p[2])]
    else:
        p[0] = p[1] + [(p[3], p[4])]

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
                  | expression MOD expression
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

def p_statement_for(p):
    'statemnt : FOR LPAREN RPAREN LBRACE statements RBRACE'
    p[0] = ('for', p[3], p[6])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number', p[1])

def p_statement_interface(p):
    'statement : INTERFACE IDENTIFIER LBRACE members RBRACE SEMICOLON'
    p[0] = ('interface', p[2], p[4])

def p_statement_function_call(p):
    'statement : IDENTIFIER DOT IDENTIFIER LPAREN parameters RPAREN SEMICOLON'
    p[0] = ('function_call', p[1], p[3], p[5])

def p_constructor(p):
    'constructor : CONSTRUCTOR LPAREN parameters RPAREN LBRACE statements RBRACE SEMICOLON'
    p[0] = ('constructor', p[3], p[6])

def p_destructor(p):
    'destructor : DESTRUCTOR LPAREN RPAREN LBRACE statements RBRACE SEMICOLON'
    p[0] = ('destructor', p[5])

def p_interface(p):
    'statement : INTERFACE IDENTIFIER LBRACE interface_members RBRACE SEMICOLON'
    p[0] = ('interface', p[2], p[4])

def p_interface_members(p):
    '''interface_members : interface_member
                         | interface_members interface_member
                         | empty'''  # Allow for an empty interface
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_interface_member(p):
    '''interface_member : function_declaration_intrfc
                        | function_declaration_intrfc_no_params'''
    p[0] = ('member', p[1])

def p_function_declaration_intrfc_no_params(p):
    'function_declaration_intrfc_no_params : TYPE IDENTIFIER LPAREN RPAREN SEMICOLON'
    p[0] = ('method_declaration', p[1], p[2], [])

def p_function_declaration_intrfc(p):
    'function_declaration_intrfc : TYPE IDENTIFIER LPAREN parameters RPAREN SEMICOLON'
    p[0] = ('method_declaration', p[1], p[2], p[4])

#def p_namespace_nesting(p):
#    '''namespace_nesting : namespace_nesting NAMESPACE_OPERATOR IDENTIFIER
#                         | IDENTIFIER NAMESPACE_OPERATOR IDENTIFIER'''
#    if len(p) == 4:  # This is the recursive case.
#        # Here, p[1] is the already processed part of the namespace,
#        # p[2] is the "::" operator, and p[3] is the next part of the namespace.
#        p[0] = p[1] + p[2] + p[3]  # Concatenate these parts to form the full namespace.
#    else:  # This is the base case.
#        # Here, p[1] is the first part of the namespace.
#        p[0] = p[1]
#
#def p_object_usage(p):
#    'object_usage : namespace_nesting IDENTIFIER SEMICOLON'
#    p[0] = ('object_usage', p[1], p[2])

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' at line {p.lineno}, position {p.lexpos}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc(debug=True)

