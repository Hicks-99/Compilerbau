grammar Grammatik;

start: stmt* ;

stmt: literal
    | expr+;

expr: '(' ((operator (literal | expr)+)
    | function
    | functioncall) COMMENT* ')';

operator:  COMP
        | ARITH;

literal: NUM
       | ID
       | BOOL
       | COMMENT
       | STRING;

function: 'defn' ID '(' (ID)* ')' expr;

functioncall: ID (literal | expr)+;

NUM     : [0-9]+ ;
BOOL    : 'true' | 'false';
STRING  : ["]~["]*["];
ID      : [a-z][a-zA-Z]* ;
COMP    : [=<>];
ARITH   : [+\-*/];
WS      : [ \t\n]+ -> skip;
COMMENT : ';;' ~[\n]*;