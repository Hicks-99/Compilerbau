# Semantische Analyse

## Grammatik und Sprache

Syntaktisch korrekt (ein Beispiel):

```mini
int add(int a, int b) {
  return a + b;
}
int z = add(2, 3);
```

Syntaktisch inkorrekt (ein Beispiel):

```mini
int x = 1
x = x + 1;
```

Fehler: fehlendes Semikolon nach `int x = 1`.

Semantisch inkorrekt (ein Beispiel):

```mini
int a = 1;
int a = 2;
```

Fehler: doppelte Deklaration von `a` im selben Scope.

## AST

[ast_builder.py](./ast_builder.py)

## Aufbau der Symboltabelle

[symbol_table.py](./symbol_table.py)

## Symboltabelle: Referenzierungen und Funktionsaufrufe

[semantic_pass2.py](./semantic_pass2.py)
