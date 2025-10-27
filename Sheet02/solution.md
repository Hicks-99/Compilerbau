# CFG

## A2.1: PDA

## A2.2: Akzeptierte Sprache

## A2.3: Kontextfreie Sprache

Die Grammatik erzeugt die folgende Sprache:

- if `<Bedingung>` `<Anweisung>`
- if `<Bedingung>` `<Anweisung>` else `<Anweisung>`

Die Grammatik ist mehrdeutig, da es in der erzeugten Sprache ein Wort gibt, das auf mehr als eine Weise abgeleitet werden kann. Zum Beispiel kann der Ausdruck

```Python
if B1 if B2 A1 else A2
```

auf zwei verschiedene Arten interpretiert werden:

1. Die `else` gehört zum inneren `if`:

   ```Python
   if B1:
       if B2:
           A1
       else:
           A2
   ```

2. Die `else` gehört zum äußeren `if`:

    ```Python
    if B1:
            if B2:
                A1
    else:
            A2
    ```

## A2.4: Kontextfreie Grammatik

G = {
&nbsp;&nbsp;&nbsp;&nbsp;    {S, A, C, D, E}
&nbsp;&nbsp;&nbsp;&nbsp;    {a, b ,c}
&nbsp;&nbsp;&nbsp;&nbsp;    P,
&nbsp;&nbsp;&nbsp;&nbsp;    S
}

P = {
&nbsp;&nbsp;&nbsp;&nbsp;    S -> D | A
&nbsp;&nbsp;&nbsp;&nbsp;    A -> aA | E | ϵ
&nbsp;&nbsp;&nbsp;&nbsp;    C -> cC | ϵ
&nbsp;&nbsp;&nbsp;&nbsp;    D -> aDb | C | ϵ
&nbsp;&nbsp;&nbsp;&nbsp;    E -> bEc | ϵ
}

Die Grammatik ist mehrdeutig, da das Wort "abc" auf zwei verschiedene Arten abgeleitet werden kann:

1. S -> A -> aA -> abEc -> abc
2. S -> D -> aDb -> abC -> abc

![PDA](pda4.svg)
