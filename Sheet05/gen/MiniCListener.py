# Generated from C:/Users/Kiera/Documents/Workspace/Compilerbau/Sheet05/MiniC.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MiniCParser import MiniCParser
else:
    from MiniCParser import MiniCParser

# This class defines a complete listener for a parse tree produced by MiniCParser.
class MiniCListener(ParseTreeListener):

    # Enter a parse tree produced by MiniCParser#program.
    def enterProgram(self, ctx:MiniCParser.ProgramContext):
        pass

    # Exit a parse tree produced by MiniCParser#program.
    def exitProgram(self, ctx:MiniCParser.ProgramContext):
        pass


    # Enter a parse tree produced by MiniCParser#stmt.
    def enterStmt(self, ctx:MiniCParser.StmtContext):
        pass

    # Exit a parse tree produced by MiniCParser#stmt.
    def exitStmt(self, ctx:MiniCParser.StmtContext):
        pass


    # Enter a parse tree produced by MiniCParser#vardecl.
    def enterVardecl(self, ctx:MiniCParser.VardeclContext):
        pass

    # Exit a parse tree produced by MiniCParser#vardecl.
    def exitVardecl(self, ctx:MiniCParser.VardeclContext):
        pass


    # Enter a parse tree produced by MiniCParser#assign.
    def enterAssign(self, ctx:MiniCParser.AssignContext):
        pass

    # Exit a parse tree produced by MiniCParser#assign.
    def exitAssign(self, ctx:MiniCParser.AssignContext):
        pass


    # Enter a parse tree produced by MiniCParser#fndecl.
    def enterFndecl(self, ctx:MiniCParser.FndeclContext):
        pass

    # Exit a parse tree produced by MiniCParser#fndecl.
    def exitFndecl(self, ctx:MiniCParser.FndeclContext):
        pass


    # Enter a parse tree produced by MiniCParser#params.
    def enterParams(self, ctx:MiniCParser.ParamsContext):
        pass

    # Exit a parse tree produced by MiniCParser#params.
    def exitParams(self, ctx:MiniCParser.ParamsContext):
        pass


    # Enter a parse tree produced by MiniCParser#return.
    def enterReturn(self, ctx:MiniCParser.ReturnContext):
        pass

    # Exit a parse tree produced by MiniCParser#return.
    def exitReturn(self, ctx:MiniCParser.ReturnContext):
        pass


    # Enter a parse tree produced by MiniCParser#fncall.
    def enterFncall(self, ctx:MiniCParser.FncallContext):
        pass

    # Exit a parse tree produced by MiniCParser#fncall.
    def exitFncall(self, ctx:MiniCParser.FncallContext):
        pass


    # Enter a parse tree produced by MiniCParser#args.
    def enterArgs(self, ctx:MiniCParser.ArgsContext):
        pass

    # Exit a parse tree produced by MiniCParser#args.
    def exitArgs(self, ctx:MiniCParser.ArgsContext):
        pass


    # Enter a parse tree produced by MiniCParser#block.
    def enterBlock(self, ctx:MiniCParser.BlockContext):
        pass

    # Exit a parse tree produced by MiniCParser#block.
    def exitBlock(self, ctx:MiniCParser.BlockContext):
        pass


    # Enter a parse tree produced by MiniCParser#while.
    def enterWhile(self, ctx:MiniCParser.WhileContext):
        pass

    # Exit a parse tree produced by MiniCParser#while.
    def exitWhile(self, ctx:MiniCParser.WhileContext):
        pass


    # Enter a parse tree produced by MiniCParser#cond.
    def enterCond(self, ctx:MiniCParser.CondContext):
        pass

    # Exit a parse tree produced by MiniCParser#cond.
    def exitCond(self, ctx:MiniCParser.CondContext):
        pass


    # Enter a parse tree produced by MiniCParser#expr.
    def enterExpr(self, ctx:MiniCParser.ExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#expr.
    def exitExpr(self, ctx:MiniCParser.ExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#type.
    def enterType(self, ctx:MiniCParser.TypeContext):
        pass

    # Exit a parse tree produced by MiniCParser#type.
    def exitType(self, ctx:MiniCParser.TypeContext):
        pass



del MiniCParser