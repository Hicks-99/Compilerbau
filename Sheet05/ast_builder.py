from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Any

try:
    from antlr4 import FileStream, CommonTokenStream
    from gen.MiniCLexer import MiniCLexer
    from gen.MiniCParser import MiniCParser
    from gen.MiniCVisitor import MiniCVisitor
except Exception as e:
    raise ImportError(
        "ANTLR generated modules not found.\n"
        f"(original error: {e})"
    )


class PrimType(Enum):
    INT = "int"
    STRING = "string"
    BOOL = "bool"


class Operator(Enum):
    EQ = "=="
    NEQ = "!="
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    LT = "<"
    GT = ">"


@dataclass
class Stmt:
    pass


@dataclass
class Expr:
    pass


@dataclass
class VarDecl(Stmt):
    type: PrimType
    name: str
    initializer: Optional[Expr] = None


@dataclass
class Assign(Stmt):
    name: str
    value: Expr


@dataclass
class FnDecl(Stmt):
    return_type: PrimType
    name: str
    params: List['Param']
    body: 'Block'


@dataclass
class ReturnStmt(Stmt):
    value: Expr


@dataclass
class ExprStmt(Stmt):
    expr: Expr


@dataclass
class Block(Stmt):
    statements: List[Stmt]


@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: Block


@dataclass
class IfStmt(Stmt):
    condition: Expr
    thenBranch: Block
    elseBranch: Block


@dataclass
class IntLiteral(Expr):
    value: int


@dataclass
class StringLiteral(Expr):
    value: str


@dataclass
class BoolLiteral(Expr):
    value: bool


@dataclass
class Variable(Expr):
    name: str


@dataclass
class Binary(Expr):
    left: Expr
    op: Operator
    right: Expr


@dataclass
class Call(Expr):
    name: str
    args: List[Expr]


@dataclass
class Param:
    type: PrimType
    name: str


class MiniCASTBuilder(MiniCVisitor):
    """Visitor that converts parse tree to AST nodes."""

    # program : stmt+ EOF ;
    def visitProgram(self, ctx: MiniCParser.ProgramContext) -> List[Stmt]:
        stmts: List[Stmt] = []
        for i in range(ctx.getChildCount() - 1):  # exclude EOF
            child = ctx.getChild(i)
            # each child is a stmt; use generic visit
            res = self.visit(child)
            if isinstance(res, list):
                stmts.extend(res)
            elif res is not None:
                stmts.append(res)
        return stmts

    # stmt alternatives
    def visitVardecl(self, ctx: MiniCParser.VardeclContext) -> VarDecl:
        typ = self._map_type(ctx.type_().getText())
        name = ctx.ID().getText()
        initializer = None
        if ctx.expr() is not None:
            initializer = self.visit(ctx.expr())
        return VarDecl(typ, name, initializer)

    def visitAssign(self, ctx: MiniCParser.AssignContext) -> Assign:
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        return Assign(name, value)

    def visitFndecl(self, ctx: MiniCParser.FndeclContext) -> FnDecl:
        return_type = self._map_type(ctx.type_().getText())
        name = ctx.ID().getText()
        params = []
        if ctx.params() is not None:
            params = self.visit(ctx.params())
        body = self.visit(ctx.block())
        return FnDecl(return_type, name, params, body)

    def visitReturn_(self, ctx: Any) -> ReturnStmt:
        return ReturnStmt(self.visit(ctx.expr()))

    def visitExprStmt(self, ctx: Any) -> ExprStmt:
        expr = self.visit(ctx.expr())
        return ExprStmt(expr)

    def visitBlock(self, ctx: MiniCParser.BlockContext) -> Block:
        stmts: List[Stmt] = []
        for s in ctx.stmt():
            stmts.append(self.visit(s))
        return Block(stmts)

    def visitWhile(self, ctx: MiniCParser.WhileContext) -> WhileStmt:
        cond = self.visit(ctx.expr())
        body = self.visit(ctx.block())
        return WhileStmt(cond, body)

    def visitCond(self, ctx: MiniCParser.CondContext) -> IfStmt:
        cond = self.visit(ctx.expr())
        then_b = self.visit(ctx.block(0))
        else_b = Block([])
        if ctx.block(1) is not None:
            else_b = self.visit(ctx.block(1))
        return IfStmt(cond, then_b, else_b)

    # params: type ID (',' type ID)* ;
    def visitParams(self, ctx: MiniCParser.ParamsContext) -> List[Param]:
        params: List[Param] = []
        types = ctx.type_()
        ids = ctx.ID()
        for t, i in zip(types, ids):
            ptype = self._map_type(t.getText())
            pname = i.getText()
            params.append(Param(ptype, pname))
        return params

    # fncall: ID '(' args? ')' ;
    def visitFncall(self, ctx: MiniCParser.FncallContext) -> Call:
        name = ctx.ID().getText()
        args: List[Expr] = []
        if ctx.args() is not None:
            args = self.visit(ctx.args())
        return Call(name, args)

    # args: expr (',' expr)* ;
    def visitArgs(self, ctx: MiniCParser.ArgsContext) -> List[Expr]:
        res: List[Expr] = []
        for e in ctx.expr():
            res.append(self.visit(e))
        return res

    # expr handling (covers literals, variables, calls, binary ops, parens)
    def visitExpr(self, ctx: MiniCParser.ExprContext) -> Expr:
        # fncall (first alt)
        if ctx.fncall() is not None:
            return self.visit(ctx.fncall())

        # direct children expressions: binary ops have two expr children
        expr_children = list(ctx.expr())
        if len(expr_children) == 2:
            left = self.visit(expr_children[0])
            right = self.visit(expr_children[1])
            op_text = ctx.getChild(1).getText()
            op = self._map_op(op_text)
            return Binary(left, op, right)

        # single child: ID | NUMBER | STRING | 'T'|'F' | '(' expr ')'
        if ctx.ID() is not None:
            return Variable(ctx.ID().getText())
        if ctx.NUMBER() is not None:
            return IntLiteral(int(ctx.NUMBER().getText()))
        if ctx.STRING() is not None:
            s = ctx.STRING().getText()
            # remove surrounding quotes
            return StringLiteral(s[1:-1])

        # booleans 'T' and 'F' are literal tokens; detect via text
        txt = ctx.getText()
        if txt == 'T':
            return BoolLiteral(True)
        if txt == 'F':
            return BoolLiteral(False)

        # parenthesized
        if ctx.getChildCount() == 3 and ctx.getChild(0).getText() == '(':
            return self.visit(ctx.expr(0))

        # fallback
        raise NotImplementedError(f"Unhandled expr node: {ctx.getText()}")

    # helper methods
    def _map_type(self, s: str) -> PrimType:
        s = s.strip()
        if s == 'int':
            return PrimType.INT
        if s == 'string':
            return PrimType.STRING
        if s == 'bool':
            return PrimType.BOOL
        raise ValueError(f"Unknown type: {s}")

    def _map_op(self, s: str) -> Operator:
        for op in Operator:
            if op.value == s:
                return op
        raise ValueError(f"Unknown operator: {s}")


def parse_and_build_ast(filename: str) -> List[Stmt]:
    input_stream = FileStream(filename, encoding='utf-8')
    lexer = MiniCLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = MiniCParser(tokens)
    tree = parser.program()
    builder = MiniCASTBuilder()
    ast = builder.visit(tree)
    return ast


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ast_builder.py <source.mc>")
        sys.exit(1)
    src = sys.argv[1]
    ast = parse_and_build_ast(src)
    from pprint import pprint
    pprint(ast)
