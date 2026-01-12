# Generated from MiniC.g4 by ANTLR 4.13.2
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


    # Visit a parse tree produced by MiniCParser#declaration.
    def visitDeclaration(self, ctx:MiniCParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#classDefinition.
    def visitClassDefinition(self, ctx:MiniCParser.ClassDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#classMember.
    def visitClassMember(self, ctx:MiniCParser.ClassMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:MiniCParser.VariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:MiniCParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#methodDefinition.
    def visitMethodDefinition(self, ctx:MiniCParser.MethodDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#constructorDefinition.
    def visitConstructorDefinition(self, ctx:MiniCParser.ConstructorDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#parameterList.
    def visitParameterList(self, ctx:MiniCParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#parameter.
    def visitParameter(self, ctx:MiniCParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#type.
    def visitType(self, ctx:MiniCParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#primitiveType.
    def visitPrimitiveType(self, ctx:MiniCParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#block.
    def visitBlock(self, ctx:MiniCParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#statement.
    def visitStatement(self, ctx:MiniCParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#ifStatement.
    def visitIfStatement(self, ctx:MiniCParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#whileStatement.
    def visitWhileStatement(self, ctx:MiniCParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#returnStatement.
    def visitReturnStatement(self, ctx:MiniCParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#IdExpr.
    def visitIdExpr(self, ctx:MiniCParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#ComparisonExpr.
    def visitComparisonExpr(self, ctx:MiniCParser.ComparisonExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#LogicAndExpr.
    def visitLogicAndExpr(self, ctx:MiniCParser.LogicAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#AssignmentExpr.
    def visitAssignmentExpr(self, ctx:MiniCParser.AssignmentExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#UnaryExpr.
    def visitUnaryExpr(self, ctx:MiniCParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#MultiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:MiniCParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#EqualityExpr.
    def visitEqualityExpr(self, ctx:MiniCParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#AdditiveExpr.
    def visitAdditiveExpr(self, ctx:MiniCParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#LogicOrExpr.
    def visitLogicOrExpr(self, ctx:MiniCParser.LogicOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#LiteralExpr.
    def visitLiteralExpr(self, ctx:MiniCParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#CallExpr.
    def visitCallExpr(self, ctx:MiniCParser.CallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#ParenExpr.
    def visitParenExpr(self, ctx:MiniCParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#MemberAccessExpr.
    def visitMemberAccessExpr(self, ctx:MiniCParser.MemberAccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#MethodCallExpr.
    def visitMethodCallExpr(self, ctx:MiniCParser.MethodCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#argumentList.
    def visitArgumentList(self, ctx:MiniCParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniCParser#literal.
    def visitLiteral(self, ctx:MiniCParser.LiteralContext):
        return self.visitChildren(ctx)



del MiniCParser