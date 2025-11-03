# Generated from PrettyLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PrettyLangParser import PrettyLangParser
else:
    from PrettyLangParser import PrettyLangParser

# This class defines a complete listener for a parse tree produced by PrettyLangParser.
class PrettyLangListener(ParseTreeListener):

    # Enter a parse tree produced by PrettyLangParser#program.
    def enterProgram(self, ctx:PrettyLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#program.
    def exitProgram(self, ctx:PrettyLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#statement.
    def enterStatement(self, ctx:PrettyLangParser.StatementContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#statement.
    def exitStatement(self, ctx:PrettyLangParser.StatementContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#assignment.
    def enterAssignment(self, ctx:PrettyLangParser.AssignmentContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#assignment.
    def exitAssignment(self, ctx:PrettyLangParser.AssignmentContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#ifStatement.
    def enterIfStatement(self, ctx:PrettyLangParser.IfStatementContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#ifStatement.
    def exitIfStatement(self, ctx:PrettyLangParser.IfStatementContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#whileStatement.
    def enterWhileStatement(self, ctx:PrettyLangParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#whileStatement.
    def exitWhileStatement(self, ctx:PrettyLangParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#condition.
    def enterCondition(self, ctx:PrettyLangParser.ConditionContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#condition.
    def exitCondition(self, ctx:PrettyLangParser.ConditionContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#MulDivExpr.
    def enterMulDivExpr(self, ctx:PrettyLangParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:PrettyLangParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#CompareExpr.
    def enterCompareExpr(self, ctx:PrettyLangParser.CompareExprContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#CompareExpr.
    def exitCompareExpr(self, ctx:PrettyLangParser.CompareExprContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#LiteralExpr.
    def enterLiteralExpr(self, ctx:PrettyLangParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#LiteralExpr.
    def exitLiteralExpr(self, ctx:PrettyLangParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#VarExpr.
    def enterVarExpr(self, ctx:PrettyLangParser.VarExprContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#VarExpr.
    def exitVarExpr(self, ctx:PrettyLangParser.VarExprContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#ParenExpr.
    def enterParenExpr(self, ctx:PrettyLangParser.ParenExprContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#ParenExpr.
    def exitParenExpr(self, ctx:PrettyLangParser.ParenExprContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:PrettyLangParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:PrettyLangParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by PrettyLangParser#literal.
    def enterLiteral(self, ctx:PrettyLangParser.LiteralContext):
        pass

    # Exit a parse tree produced by PrettyLangParser#literal.
    def exitLiteral(self, ctx:PrettyLangParser.LiteralContext):
        pass



del PrettyLangParser