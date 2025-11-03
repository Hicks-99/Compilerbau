grammar PrettyLang;

// -----------------------------
// Parser-Regeln
// -----------------------------

program
    : statement+ EOF
    ;

statement
    : assignment
    | ifStatement
    | whileStatement
    | expression NEWLINE
    ;

assignment
    : IDENT ':=' expression NEWLINE
    ;

ifStatement
    : IF condition DO NEWLINE statement+
      (ELSE DO NEWLINE statement+)? END NEWLINE?
    ;

whileStatement
    : WHILE condition DO NEWLINE statement+ END NEWLINE?
    ;

condition
    : expression
    ;

// -----------------------------
// Ausdrücke mit Vorrangregeln
// -----------------------------

expression
    : expression op=('*'|'/') expression   # MulDivExpr
    | expression op=('+'|'-') expression   # AddSubExpr
    | expression op=('<'|'>'|'=='|'!=') expression # CompareExpr
    | '(' expression ')'                   # ParenExpr
    | literal                              # LiteralExpr
    | IDENT                                # VarExpr
    ;

// -----------------------------
// Literale
// -----------------------------

literal
    : INT
    | STRING
    ;

// -----------------------------
// Lexer-Regeln
// -----------------------------

IF      : 'if';
ELSE    : 'else';
WHILE   : 'while';
DO      : 'do';
END     : 'end';

INT     : [0-9]+;
STRING  : '"' (~["\r\n])* '"';
IDENT   : [a-zA-Z_][a-zA-Z0-9_]*;

// Kommentare
COMMENT : '#' ~[\r\n]* -> skip;

// Whitespace und Zeilenumbrüche
WS      : [ \t\r]+ -> skip;
NEWLINE : '\n'+;

// Operatoren und Sonstiges
ASSIGN  : ':=';
PLUS    : '+';
MINUS   : '-';
STAR    : '*';
SLASH   : '/';
EQ      : '==';
NEQ     : '!=';
LT      : '<';
GT      : '>';
