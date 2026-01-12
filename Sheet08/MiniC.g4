grammar MiniC;

// Parser Rules

program
    : declaration*
    ;

declaration
    : classDefinition
    | functionDefinition
    ;

classDefinition
    : CLASS Identifier (COLON PUBLIC Identifier)? LBRACE PUBLIC COLON classMember* RBRACE SEMI?
    ;

classMember
    : methodDefinition
    | constructorDefinition
    | variableDeclaration
    ;

variableDeclaration
    : type Identifier (ASSIGN expression)? SEMI
    ;

functionDefinition
    : type Identifier LPAREN parameterList? RPAREN block
    ;

methodDefinition
    : VIRTUAL? type Identifier LPAREN parameterList? RPAREN block
    ;

constructorDefinition
    : Identifier LPAREN parameterList? RPAREN block
    ;

parameterList
    : parameter (COMMA parameter)*
    ;

parameter
    : type Identifier
    ;

type
    : primitiveType REF?
    ;

primitiveType
    : BOOL
    | INT
    | CHAR
    | STRING
    | VOID
    | Identifier
    ;

block
    : LBRACE statement* RBRACE
    ;

statement
    : variableDeclaration
    | expression SEMI
    | ifStatement
    | whileStatement
    | returnStatement
    | block
    ;

ifStatement
    : IF LPAREN expression RPAREN statement (ELSE statement)?
    ;

whileStatement
    : WHILE LPAREN expression RPAREN statement
    ;

returnStatement
    : RETURN expression? SEMI
    ;

// Expression precedence (highest to lowest)
expression
    : LPAREN expression RPAREN                         # ParenExpr
    | expression DOT Identifier '(' argumentList? ')'  # MethodCallExpr
    | expression DOT Identifier                        # MemberAccessExpr
    | Identifier '(' argumentList? ')'                 # CallExpr
    | (PLUS | MINUS | NOT) expression                  # UnaryExpr
    | expression (STAR | DIV | MOD) expression         # MultiplicativeExpr
    | expression (PLUS | MINUS) expression             # AdditiveExpr
    | expression (LT | LE | GT | GE) expression        # ComparisonExpr
    | expression (EQ | NEQ) expression                 # EqualityExpr
    | expression AND expression                        # LogicAndExpr
    | expression OR expression                         # LogicOrExpr
    | expression ASSIGN expression                     # AssignmentExpr
    | Identifier                                       # IdExpr
    | literal                                          # LiteralExpr
    ;

argumentList
    : expression (COMMA expression)*
    ;

literal
    : BoolLiteral
    | IntLiteral
    | CharLiteral
    | StringLiteral
    ;

// Lexer Rules

IF : 'if';
ELSE : 'else';
WHILE : 'while';
RETURN : 'return';
CLASS : 'class';
PUBLIC : 'public';
VIRTUAL : 'virtual';

BOOL : 'bool';
INT : 'int';
CHAR : 'char';
STRING : 'string';
VOID : 'void';

BoolLiteral : 'true' | 'false';

IntLiteral : [0-9]+;

CharLiteral : '\'' ( ESCAPE_SEQ | ~['\\] ) '\'';

StringLiteral : '"' ( ESCAPE_SEQ | ~["\\] )* '"';

fragment ESCAPE_SEQ
    : '\\' [abfnrtv\\'"]
    | '\\' [0-7] [0-7]? [0-7]?
    | '\\' 'x' [0-9a-fA-F]+
    ;

Identifier : [a-zA-Z_] [a-zA-Z0-9_]*;

PLUS : '+';
MINUS : '-';
STAR : '*';
DIV : '/';
MOD : '%';
ASSIGN : '=';
EQ : '==';
NEQ : '!=';
LT : '<';
LE : '<=';
GT : '>';
GE : '>=';
AND : '&&';
OR : '||';
NOT : '!';
REF : '&';
DOT : '.';
COMMA : ',';
SEMI : ';';
COLON : ':';
LPAREN : '(';
RPAREN : ')';
LBRACE : '{';
RBRACE : '}';

WS : [ \t\r\n]+ -> skip;

LINE_COMMENT : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT : '/*' .*? '*/' -> skip;
PREPROCESSOR : '#' ~[\r\n]* -> skip;
