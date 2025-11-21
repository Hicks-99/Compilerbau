"""Semantic pass 2: check function calls (existence, visibility, signature)

Usage: python semantic_pass2.py <source.mc>

This script builds AST (using ast_builder), then performs a traversal that
ensures:
- Called functions are defined and visible in the current scope (functions may
  be defined later in the same scope -> we pre-collect all function declarations
  in each scope before checking statements).
- Argument count and types match the function signature.

It also performs expression type-checking needed for signature checks.
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional
import sys

from ast_builder import (
    parse_and_build_ast,
    Stmt,
    VarDecl,
    Assign,
    FnDecl,
    ReturnStmt,
    ExprStmt,
    Block,
    WhileStmt,
    IfStmt,
    IntLiteral,
    StringLiteral,
    BoolLiteral,
    Variable,
    Binary,
    Call,
    Param,
    PrimType,
    Operator,
)


class Pass2Checker:
    def __init__(self):
        # scope stack: each scope is dict name->symbol info {'kind': 'var'|'fn', 'type':PrimType, 'params':[PrimType]}
        self.scopes: List[Dict[str, Dict[str, Any]]] = []
        self.errors: List[str] = []

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def current_scope(self) -> Dict[str, Dict[str, Any]]:
        return self.scopes[-1]

    def lookup(self, name: str) -> Optional[Dict[str, Any]]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def precollect_functions(self, stmts: List[Stmt]):
        # collect function declarations in this statement list so forward calls are allowed
        for s in stmts:
            if isinstance(s, FnDecl):
                self.current_scope()[s.name] = {'kind': 'fn', 'type': s.return_type, 'params': [
                    p.type for p in s.params], 'node': s}

    def visit_program(self, stmts: List[Stmt]):
        self.push_scope()
        self.precollect_functions(stmts)
        for s in stmts:
            self.visit_stmt(s)
        self.pop_scope()

    def visit_stmt(self, node: Stmt):
        if isinstance(node, VarDecl):
            # declare var (must be visible after declaration)
            self.current_scope()[node.name] = {
                'kind': 'var', 'type': node.type, 'node': node}
            if node.initializer:
                self.type_of(node.initializer)

        elif isinstance(node, Assign):
            # ensure var exists and type matches (type checking done here)
            sym = self.lookup(node.name)
            if sym is None:
                self.errors.append(
                    f"Fehler: Zuweisung an undefinierte Variable '{node.name}'.")
            else:
                if sym['kind'] != 'var':
                    self.errors.append(
                        f"Fehler: '{node.name}' ist keine Variable.")
                else:
                    expr_t = self.type_of(node.value)
                    if expr_t is not None and expr_t != sym['type']:
                        self.errors.append(
                            f"Fehler: Typfehler bei Zuweisung an '{node.name}': erwartet {sym['type'].value}, gefunden {expr_t.value}.")

        elif isinstance(node, FnDecl):
            # function already pre-collected in this scope; visit body in new scope
            self.push_scope()
            # declare params as vars
            for p in node.params:
                self.current_scope()[p.name] = {
                    'kind': 'var', 'type': p.type, 'node': p}
            # precollect nested functions in body
            self.precollect_functions(node.body.statements)
            for s in node.body.statements:
                self.visit_stmt(s)
            self.pop_scope()

        elif isinstance(node, ExprStmt):
            self.type_of(node.expr)

        elif isinstance(node, Block):
            self.push_scope()
            self.precollect_functions(node.statements)
            for s in node.statements:
                self.visit_stmt(s)
            self.pop_scope()

        elif isinstance(node, WhileStmt):
            cond_t = self.type_of(node.condition)
            if cond_t is not None and cond_t != PrimType.BOOL:
                self.errors.append(
                    "Fehler: Bedingung eines while muss vom Typ bool sein.")
            self.visit_stmt(node.body)

        elif isinstance(node, IfStmt):
            cond_t = self.type_of(node.condition)
            if cond_t is not None and cond_t != PrimType.BOOL:
                self.errors.append(
                    "Fehler: Bedingung eines if muss vom Typ bool sein.")
            self.visit_stmt(node.thenBranch)
            if node.elseBranch is not None:
                self.visit_stmt(node.elseBranch)

        elif isinstance(node, ReturnStmt):
            # return checking vs function signature could be done if we track current function return type
            self.type_of(node.value)

        else:
            pass

    def type_of(self, expr) -> Optional[PrimType]:
        if isinstance(expr, IntLiteral):
            return PrimType.INT
        if isinstance(expr, StringLiteral):
            return PrimType.STRING
        if isinstance(expr, BoolLiteral):
            return PrimType.BOOL
        if isinstance(expr, Variable):
            sym = self.lookup(expr.name)
            if sym is None:
                self.errors.append(
                    f"Fehler: Verwendung undefinierter Variable '{expr.name}'.")
                return None
            if sym['kind'] != 'var':
                self.errors.append(
                    f"Fehler: '{expr.name}' ist keine Variable.")
                return None
            return sym['type']
        if isinstance(expr, Call):
            sym = self.lookup(expr.name)
            if sym is None:
                self.errors.append(
                    f"Fehler: Aufruf undefinierter Funktion '{expr.name}'.")
                # still check arg types
                for a in expr.args:
                    self.type_of(a)
                return None
            if sym['kind'] != 'fn':
                self.errors.append(
                    f"Fehler: Symbol '{expr.name}' ist keine Funktion.")
                return None
            # check arg count
            expected = sym.get('params', [])
            if len(expected) != len(expr.args):
                self.errors.append(
                    f"Fehler: Aufruf von '{expr.name}' erwartet {len(expected)} Argumente, gefunden {len(expr.args)}.")
            # check arg types
            for i, a in enumerate(expr.args):
                at = self.type_of(a)
                if at is None:
                    continue
                if i < len(expected) and at != expected[i]:
                    self.errors.append(
                        f"Fehler: Typfehler im Aufruf von '{expr.name}': Parameter {i+1} erwartet {expected[i].value}, gefunden {at.value}.")
            return sym['type']
        if isinstance(expr, Binary):
            lt = self.type_of(expr.left)
            rt = self.type_of(expr.right)
            if lt is None or rt is None:
                return None
            if lt != rt:
                self.errors.append(
                    f"Fehler: Binärer Operator benötigt gleiche Typen, gefunden {lt.value} und {rt.value}.")
                return None
            op = expr.op
            if op == Operator.PLUS:
                if lt in (PrimType.INT, PrimType.STRING):
                    return lt
                self.errors.append(
                    "Fehler: '+' nur für int oder string erlaubt.")
                return None
            if op in (Operator.MINUS, Operator.MUL, Operator.DIV):
                if lt == PrimType.INT:
                    return PrimType.INT
                self.errors.append(
                    f"Fehler: Operator {op.value} nur für int erlaubt.")
                return None
            if op in (Operator.LT, Operator.GT, Operator.EQ, Operator.NEQ):
                if lt in (PrimType.INT, PrimType.STRING):
                    return PrimType.BOOL
                self.errors.append(
                    f"Fehler: Vergleichsoperator {op.value} nur für int oder string erlaubt.")
                return None
        # unknown expr
        return None


def main(argv):
    if len(argv) < 2:
        print("Usage: python semantic_pass2.py <source.mc>")
        return 1
    src = argv[1]
    ast = parse_and_build_ast(src)
    checker = Pass2Checker()
    checker.visit_program(ast)
    if checker.errors:
        print("Semantic errors (pass 2):")
        for e in checker.errors:
            print(e)
        return 2
    else:
        print("Pass 2 completed: no errors found.")
        return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
