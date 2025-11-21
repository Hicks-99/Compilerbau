# Generated from C:/Users/Kiera/Documents/Workspace/Compilerbau/Sheet05/MiniC.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MiniCParser import MiniCParser
else:
    from MiniCParser import MiniCParser

# This class defines a complete generic visitor for a parse tree produced by MiniCParser.

class MiniCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MiniCParser#program.
    def visitProgram(self, ctx:MiniCParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#stmt.
    def visitStmt(self, ctx:MiniCParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#vardecl.
    def visitVardecl(self, ctx:MiniCParser.VardeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#assign.
    def visitAssign(self, ctx:MiniCParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#fndecl.
    def visitFndecl(self, ctx:MiniCParser.FndeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#params.
    def visitParams(self, ctx:MiniCParser.ParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#return.
    def visitReturn(self, ctx:MiniCParser.ReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#fncall.
    def visitFncall(self, ctx:MiniCParser.FncallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#args.
    def visitArgs(self, ctx:MiniCParser.ArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#block.
    def visitBlock(self, ctx:MiniCParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#while.
    def visitWhile(self, ctx:MiniCParser.WhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#cond.
    def visitCond(self, ctx:MiniCParser.CondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#expr.
    def visitExpr(self, ctx:MiniCParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#type.
    def visitType(self, ctx:MiniCParser.TypeContext):
        return self.visitChildren(ctx)



del MiniCParser