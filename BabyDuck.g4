grammar BabyDuck;

// Non-Regex Keywords
PROGRAM: 'program';
SEMI_COLON: ';';
MAIN: 'main';
END: 'end';
VAR: 'var';
COMMA: ',';
COLON: ':';
INT: 'int';
FLOAT: 'float';
IF: 'if';
ELSE: 'else';
LEFT_CURLY_BRACE: '{';
RIGHT_CURLY_BRACE: '}';
PRINT: 'print';
LEFT_PARENTHESIS: '(';
RIGHT_PARENTHESIS: ')';
ASSIGN: '=';
WHILE: 'while';
DO: 'do';
GREATER_THAN: '>';
LESS_THAN: '<';
NOT_EQUALS: '!=';
PLUS: '+';
MINUS: '-';
TIMES: '*';
DIVIDE: '/';
VOID: 'void';
LEFT_BRACKET: '[';
RIGHT_BRACKET: ']';

// Regex Keywords (ORDERED WITH PRIORITY)
CTE_FLOAT: ([0-9]+[.][0-9]+[eE][0-9]+[.][0-9])
         | ([0-9]+[.][0-9]+[eE][0-9]+)
         | ([0-9]+[.][0-9]+);
CTE_INT: ([0-9]+[eE][0-9]+)
       | ([0-9]+);
CTE_STRING: '"'(~["])*'"';
ID: [a-zA-Z][a-zA-Z0-9_-]*;
WHITESPACE: [ \t\r\n]+ -> skip; // We need this to skip whitespace

// Grammar
epsilon : ; // THIS IS FOR EMPTY/NULL GRAMMAR (epsilon)
program_id: ID;
main: MAIN;
programa: PROGRAM program_id SEMI_COLON dec_vars dec_funcs main body END;
dec_vars: epsilon
        | vars;
dec_funcs: epsilon 
         | funcs dec_funcs;
var_id: ID;
var_type: type;
vars: VAR vars_content;
vars_content: list_id COLON var_type SEMI_COLON mas_vars_content;
mas_vars_content: epsilon
                | vars_content;
list_id: var_id
       | var_id COMMA list_id;
type: INT
    | FLOAT;
func_id: ID;
funcs: VOID func_id LEFT_PARENTHESIS list_params RIGHT_PARENTHESIS LEFT_BRACKET dec_vars body RIGHT_BRACKET SEMI_COLON;
list_params: epsilon
           | var_id COLON var_type
           | var_id COLON var_type COMMA list_params;
body: LEFT_CURLY_BRACE dec_statement RIGHT_CURLY_BRACE;
dec_statement: epsilon
             | statement
             | statement dec_statement;
statement: assign
         | condition
         | cycle
         | f_call
         | print;
assign: ID ASSIGN expression SEMI_COLON;
condition: IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS body SEMI_COLON
         | IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS body ELSE body SEMI_COLON;
cycle: WHILE LEFT_PARENTHESIS expression RIGHT_PARENTHESIS DO body SEMI_COLON;
f_call: ID LEFT_PARENTHESIS list_expression RIGHT_PARENTHESIS SEMI_COLON;
list_expression: epsilon
               | expression
               | expression COMMA list_expression;
print: PRINT LEFT_PARENTHESIS print_args RIGHT_PARENTHESIS SEMI_COLON;
print_args: expression
          | CTE_STRING
          | print_args COMMA print_args;
expression_operation: GREATER_THAN
                    | LESS_THAN
                    | NOT_EQUALS;
expression: exp
          | exp expression_operation expression;
exp_operation: PLUS
             | MINUS;
exp: termino
   | termino exp_operation exp;
termino_operation: TIMES
                 | DIVIDE;
termino: factor
       | factor termino_operation termino;
factor: factor_with_parenthesis
      | factor_with_id
      | factor_with_cte;
factor_with_parenthesis_left_parenthesis: LEFT_PARENTHESIS;
factor_with_parenthesis_right_parenthesis: RIGHT_PARENTHESIS;
factor_with_parenthesis: factor_with_parenthesis_left_parenthesis expression factor_with_parenthesis_right_parenthesis; 
factor_with_id: factor_sign ID;
factor_with_cte: factor_sign cte;
factor_sign: epsilon
           | PLUS
           | MINUS;
cte: CTE_INT
   | CTE_FLOAT;