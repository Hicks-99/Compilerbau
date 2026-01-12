# Generated from MiniC.g4 by ANTLR 4.13.2
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


    # Enter a parse tree produced by MiniCParser#declaration.
    def enterDeclaration(self, ctx:MiniCParser.DeclarationContext):
        pass

    # Exit a parse tree produced by MiniCParser#declaration.
    def exitDeclaration(self, ctx:MiniCParser.DeclarationContext):
        pass


    # Enter a parse tree produced by MiniCParser#classDefinition.
    def enterClassDefinition(self, ctx:MiniCParser.ClassDefinitionContext):
        pass

    # Exit a parse tree produced by MiniCParser#classDefinition.
    def exitClassDefinition(self, ctx:MiniCParser.ClassDefinitionContext):
        pass


    # Enter a parse tree produced by MiniCParser#classMember.
    def enterClassMember(self, ctx:MiniCParser.ClassMemberContext):
        pass

    # Exit a parse tree produced by MiniCParser#classMember.
    def exitClassMember(self, ctx:MiniCParser.ClassMemberContext):
        pass


    # Enter a parse tree produced by MiniCParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:MiniCParser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by MiniCParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx:MiniCParser.VariableDeclarationContext):
        pass


    # Enter a parse tree produced by MiniCParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:MiniCParser.FunctionDefinitionContext):
        pass

    # Exit a parse tree produced by MiniCParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:MiniCParser.FunctionDefinitionContext):
        pass


    # Enter a parse tree produced by MiniCParser#methodDefinition.
    def enterMethodDefinition(self, ctx:MiniCParser.MethodDefinitionContext):
        pass

    # Exit a parse tree produced by MiniCParser#methodDefinition.
    def exitMethodDefinition(self, ctx:MiniCParser.MethodDefinitionContext):
        pass


    # Enter a parse tree produced by MiniCParser#constructorDefinition.
    def enterConstructorDefinition(self, ctx:MiniCParser.ConstructorDefinitionContext):
        pass

    # Exit a parse tree produced by MiniCParser#constructorDefinition.
    def exitConstructorDefinition(self, ctx:MiniCParser.ConstructorDefinitionContext):
        pass


    # Enter a parse tree produced by MiniCParser#parameterList.
    def enterParameterList(self, ctx:MiniCParser.ParameterListContext):
        pass

    # Exit a parse tree produced by MiniCParser#parameterList.
    def exitParameterList(self, ctx:MiniCParser.ParameterListContext):
        pass


    # Enter a parse tree produced by MiniCParser#parameter.
    def enterParameter(self, ctx:MiniCParser.ParameterContext):
        pass

    # Exit a parse tree produced by MiniCParser#parameter.
    def exitParameter(self, ctx:MiniCParser.ParameterContext):
        pass


    # Enter a parse tree produced by MiniCParser#type.
    def enterType(self, ctx:MiniCParser.TypeContext):
        pass

    # Exit a parse tree produced by MiniCParser#type.
    def exitType(self, ctx:MiniCParser.TypeContext):
        pass


    # Enter a parse tree produced by MiniCParser#primitiveType.
    def enterPrimitiveType(self, ctx:MiniCParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by MiniCParser#primitiveType.
    def exitPrimitiveType(self, ctx:MiniCParser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by MiniCParser#block.
    def enterBlock(self, ctx:MiniCParser.BlockContext):
        pass

    # Exit a parse tree produced by MiniCParser#block.
    def exitBlock(self, ctx:MiniCParser.BlockContext):
        pass


    # Enter a parse tree produced by MiniCParser#statement.
    def enterStatement(self, ctx:MiniCParser.StatementContext):
        pass

    # Exit a parse tree produced by MiniCParser#statement.
    def exitStatement(self, ctx:MiniCParser.StatementContext):
        pass


    # Enter a parse tree produced by MiniCParser#ifStatement.
    def enterIfStatement(self, ctx:MiniCParser.IfStatementContext):
        pass

    # Exit a parse tree produced by MiniCParser#ifStatement.
    def exitIfStatement(self, ctx:MiniCParser.IfStatementContext):
        pass


    # Enter a parse tree produced by MiniCParser#whileStatement.
    def enterWhileStatement(self, ctx:MiniCParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by MiniCParser#whileStatement.
    def exitWhileStatement(self, ctx:MiniCParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by MiniCParser#returnStatement.
    def enterReturnStatement(self, ctx:MiniCParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by MiniCParser#returnStatement.
    def exitReturnStatement(self, ctx:MiniCParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by MiniCParser#IdExpr.
    def enterIdExpr(self, ctx:MiniCParser.IdExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#IdExpr.
    def exitIdExpr(self, ctx:MiniCParser.IdExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#ComparisonExpr.
    def enterComparisonExpr(self, ctx:MiniCParser.ComparisonExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#ComparisonExpr.
    def exitComparisonExpr(self, ctx:MiniCParser.ComparisonExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#LogicAndExpr.
    def enterLogicAndExpr(self, ctx:MiniCParser.LogicAndExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#LogicAndExpr.
    def exitLogicAndExpr(self, ctx:MiniCParser.LogicAndExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#AssignmentExpr.
    def enterAssignmentExpr(self, ctx:MiniCParser.AssignmentExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#AssignmentExpr.
    def exitAssignmentExpr(self, ctx:MiniCParser.AssignmentExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#UnaryExpr.
    def enterUnaryExpr(self, ctx:MiniCParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#UnaryExpr.
    def exitUnaryExpr(self, ctx:MiniCParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#MultiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:MiniCParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#MultiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:MiniCParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#EqualityExpr.
    def enterEqualityExpr(self, ctx:MiniCParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#EqualityExpr.
    def exitEqualityExpr(self, ctx:MiniCParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#AdditiveExpr.
    def enterAdditiveExpr(self, ctx:MiniCParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#AdditiveExpr.
    def exitAdditiveExpr(self, ctx:MiniCParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#LogicOrExpr.
    def enterLogicOrExpr(self, ctx:MiniCParser.LogicOrExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#LogicOrExpr.
    def exitLogicOrExpr(self, ctx:MiniCParser.LogicOrExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#LiteralExpr.
    def enterLiteralExpr(self, ctx:MiniCParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#LiteralExpr.
    def exitLiteralExpr(self, ctx:MiniCParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#CallExpr.
    def enterCallExpr(self, ctx:MiniCParser.CallExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#CallExpr.
    def exitCallExpr(self, ctx:MiniCParser.CallExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#ParenExpr.
    def enterParenExpr(self, ctx:MiniCParser.ParenExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#ParenExpr.
    def exitParenExpr(self, ctx:MiniCParser.ParenExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#MemberAccessExpr.
    def enterMemberAccessExpr(self, ctx:MiniCParser.MemberAccessExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#MemberAccessExpr.
    def exitMemberAccessExpr(self, ctx:MiniCParser.MemberAccessExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#MethodCallExpr.
    def enterMethodCallExpr(self, ctx:MiniCParser.MethodCallExprContext):
        pass

    # Exit a parse tree produced by MiniCParser#MethodCallExpr.
    def exitMethodCallExpr(self, ctx:MiniCParser.MethodCallExprContext):
        pass


    # Enter a parse tree produced by MiniCParser#argumentList.
    def enterArgumentList(self, ctx:MiniCParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by MiniCParser#argumentList.
    def exitArgumentList(self, ctx:MiniCParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by MiniCParser#literal.
    def enterLiteral(self, ctx:MiniCParser.LiteralContext):
        pass

    # Exit a parse tree produced by MiniCParser#literal.
    def exitLiteral(self, ctx:MiniCParser.LiteralContext):
        pass



del MiniCParser