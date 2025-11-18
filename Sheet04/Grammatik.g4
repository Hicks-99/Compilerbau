grammar Grammatik;

start: stmt* EOF;

stmt: expr
    | comment;

expr: literal
    | sexpr;

sexpr: '(' operator expr+ ')'                          // Operatoren: (+1 2 3)
     | '(' 'if' expr expr expr? ')'                    // if-then-else
     | '(' 'do' expr+ ')'                              // do Block
     | '(' 'def' ID expr ')'                           // Variable definieren
     | '(' 'defn' ID '(' ID* ')' expr ')'              // Funktion definieren
     | '(' 'let' '(' binding+ ')' expr ')'             // lokaler Scope
     | '(' 'print' expr ')'                            // eingebaute Funktion
     | '(' 'str' expr+ ')'                             // eingebaute Funktion
     | '(' 'list' expr* ')'                            // Listen erstellen
     | '(' 'nth' expr expr ')'                         // Listenzugriff
     | '(' 'head' expr ')'                             // erstes Element
     | '(' 'tail' expr ')'                             // Rest der Liste
     | '(' ID expr+ ')';                               // Funktionsaufruf

binding: ID expr;

operator: COMP | ARITH;

literal: NUM
       | BOOL
       | STRING
       | ID;

comment: COMMENT;

NUM     : [0-9]+ ;
BOOL    : 'true' | 'false';
STRING  : '"' (~["\r\n] | '\\' .)* '"';
ID      : [a-z][a-zA-Z0-9]* ;
COMP    : '=' | '>' | '<';
ARITH   : '+' | '-' | '*' | '/';
WS      : [ \t\r\n]+ -> skip;
COMMENT : ';;' ~[\r\n]*;