from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import sys

from ast_builder import (
    parse_and_build_ast,
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
)


@dataclass
class SymbolEntry:
    name: str
    kind: str  # 'var' or 'fn'
    type: Optional[PrimType]
    params: Optional[List[PrimType]] = None
    ast_node: Optional[Any] = None


class SymbolTableBuilder:
    def __init__(self):
        self.scopes: List[Dict[str, SymbolEntry]] = [{}]
        self.errors: List[str] = []

    def current_scope(self) -> Dict[str, SymbolEntry]:
        return self.scopes[-1]

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def lookup(self, name: str) -> Optional[SymbolEntry]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def declare_var(self, name: str, typ: PrimType, node: Any):
        scope = self.current_scope()
        if name in scope:
            self.errors.append(
                f"Fehler: Symbol '{name}' bereits im aktuellen Scope definiert.")
            return
        scope[name] = SymbolEntry(name, 'var', typ, None, node)

    def declare_fn(self, name: str, return_type: PrimType, params: List[Param], node: Any):
        scope = self.current_scope()
        if name in scope:
            self.errors.append(
                f"Fehler: Symbol '{name}' bereits im aktuellen Scope definiert.")
            return
        param_types = [p.type for p in params]
        scope[name] = SymbolEntry(name, 'fn', return_type, param_types, node)

    def build(self, stmts: List[Any]):
        for s in stmts:
            self.visit_stmt(s)

    def visit_stmt(self, node: Any):
        if isinstance(node, VarDecl):
            # Evaluate initializer first (var not yet in scope)
            if node.initializer is not None:
                self.visit_expr(node.initializer)
            self.declare_var(node.name, node.type, node)

        elif isinstance(node, Assign):
            # LHS must be declared variable
            entry = self.lookup(node.name)
            if entry is None:
                self.errors.append(
                    f"Fehler: Zuweisung an undefinierte Variable '{node.name}'.")
            elif entry.kind != 'var':
                self.errors.append(
                    f"Fehler: '{node.name}' ist keine Variable und kann nicht zugewiesen werden.")
            self.visit_expr(node.value)

        elif isinstance(node, FnDecl):
            # declare function in current scope BEFORE processing body (so recursion allowed)
            self.declare_fn(node.name, node.return_type, node.params, node)
            # process body in new scope; parameters are declarations in function scope
            self.push_scope()
            # declare params
            for p in node.params:
                if p.name in self.current_scope():
                    self.errors.append(
                        f"Fehler: Parametername '{p.name}' mehrfach in Funktionsdefinition '{node.name}'.")
                self.current_scope()[p.name] = SymbolEntry(
                    p.name, 'var', p.type, None, p)
            # visit body statements
            for s in node.body.statements:
                self.visit_stmt(s)
            self.pop_scope()

        elif isinstance(node, ExprStmt):
            self.visit_expr(node.expr)

        elif isinstance(node, Block):
            self.push_scope()
            for s in node.statements:
                self.visit_stmt(s)
            self.pop_scope()

        elif isinstance(node, WhileStmt):
            self.visit_expr(node.condition)
            self.visit_stmt(node.body)

        elif isinstance(node, IfStmt):
            self.visit_expr(node.condition)
            self.visit_stmt(node.thenBranch)
            if node.elseBranch is not None:
                self.visit_stmt(node.elseBranch)

        elif isinstance(node, ReturnStmt):
            self.visit_expr(node.value)

        else:
            # Unknown statement type
            pass

    def visit_expr(self, node: Any):
        if isinstance(node, IntLiteral) or isinstance(node, StringLiteral) or isinstance(node, BoolLiteral):
            return
        if isinstance(node, Variable):
            entry = self.lookup(node.name)
            if entry is None:
                self.errors.append(
                    f"Fehler: Verwendung undefinierter Variable '{node.name}'.")
            return
        if isinstance(node, Call):
            entry = self.lookup(node.name)
            if entry is not None and entry.kind == 'var':
                self.errors.append(
                    f"Fehler: Symbol '{node.name}' ist eine Variable und kann nicht als Funktion aufgerufen werden.")
            # Do not error if function not found here; that is pass 2
            for a in node.args:
                self.visit_expr(a)
            return
        if isinstance(node, Binary):
            self.visit_expr(node.left)
            self.visit_expr(node.right)


def main(argv):
    if len(argv) < 2:
        print("Usage: python symbol_table.py <source.mc>")
        return 1
    src = argv[1]
    ast = parse_and_build_ast(src)
    builder = SymbolTableBuilder()
    builder.build(ast)
    if builder.errors:
        print("Semantic errors (pass 1):")
        for e in builder.errors:
            print(e)
        return 2
    else:
        print("Pass 1 completed: no errors found.")
        return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
