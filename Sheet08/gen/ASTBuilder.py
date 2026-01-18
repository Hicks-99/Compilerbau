from .MiniCVisitor import MiniCVisitor
from .MiniCParser import MiniCParser
from .AST import *


class ASTBuilder(MiniCVisitor):
    """Builds AST from ANTLR parse tree using the Visitor pattern"""

    def visitProgram(self, ctx: MiniCParser.ProgramContext) -> Program:
        declarations = []
        for decl_ctx in ctx.declaration():
            decl = self.visitDeclaration(decl_ctx)
            if decl:
                declarations.append(decl)
        return Program(declarations)

    def visitDeclaration(self, ctx: MiniCParser.DeclarationContext) -> Declaration:
        if ctx.classDefinition():
            return self.visitClassDefinition(ctx.classDefinition())
        elif ctx.functionDefinition():
            return self.visitFunctionDefinition(ctx.functionDefinition())
        return None

    def visitClassDefinition(self, ctx: MiniCParser.ClassDefinitionContext) -> ClassDefinition:
        name = ctx.Identifier(0).getText()
        parent = ctx.Identifier(1).getText() if len(
            ctx.Identifier()) > 1 else None
        members = []
        for member_ctx in ctx.classMember():
            member = self.visitClassMember(member_ctx)
            if member:
                members.append(member)
        return ClassDefinition(name, parent, members)

    def visitClassMember(self, ctx: MiniCParser.ClassMemberContext) -> ClassMember:
        if ctx.methodDefinition():
            return self.visitMethodDefinition(ctx.methodDefinition())
        elif ctx.constructorDefinition():
            return self.visitConstructorDefinition(ctx.constructorDefinition())
        elif ctx.variableDeclaration():
            return self.visitVariableDeclaration(ctx.variableDeclaration())
        return None

    def visitFunctionDefinition(self, ctx: MiniCParser.FunctionDefinitionContext) -> FunctionDefinition:
        return_type = self.visitType(ctx.type_())
        name = ctx.Identifier().getText()
        parameters = self.visitParameterList(
            ctx.parameterList()) if ctx.parameterList() else []
        # Gibt jetzt eine Liste zurück
        body = self.visitBlockStatements(ctx.block())
        return FunctionDefinition(return_type, name, parameters, body)

    def visitMethodDefinition(self, ctx: MiniCParser.MethodDefinitionContext) -> MethodDefinition:
        is_virtual = ctx.VIRTUAL() is not None
        return_type = self.visitType(ctx.type_())
        name = ctx.Identifier().getText()
        parameters = self.visitParameterList(
            ctx.parameterList()) if ctx.parameterList() else []
        # Gibt jetzt eine Liste zurück
        body = self.visitBlockStatements(ctx.block())
        return MethodDefinition(is_virtual, return_type, name, parameters, body)

    def visitConstructorDefinition(self, ctx: MiniCParser.ConstructorDefinitionContext) -> ConstructorDefinition:
        name = ctx.Identifier().getText()
        parameters = self.visitParameterList(
            ctx.parameterList()) if ctx.parameterList() else []
        # Gibt jetzt eine Liste zurück
        body = self.visitBlockStatements(ctx.block())
        return ConstructorDefinition(name, parameters, body)

    def visitVariableDeclaration(self, ctx: MiniCParser.VariableDeclarationContext) -> VariableDeclaration:
        var_type = self.visitType(ctx.type_())
        name = ctx.Identifier().getText()
        initializer = self.visitExpression(
            ctx.expression()) if ctx.expression() else None
        return VariableDeclaration(var_type, name, initializer)

    def visitParameterList(self, ctx: MiniCParser.ParameterListContext) -> List[Parameter]:
        return [self.visitParameter(param) for param in ctx.parameter()]

    def visitParameter(self, ctx: MiniCParser.ParameterContext) -> Parameter:
        param_type = self.visitType(ctx.type_())
        name = ctx.Identifier().getText()
        return Parameter(param_type, name)

    def visitType(self, ctx: MiniCParser.TypeContext) -> Type:
        base_type = self.visitPrimitiveType(ctx.primitiveType())
        is_reference = ctx.REF() is not None
        return Type(base_type, is_reference)

    def visitPrimitiveType(self, ctx: MiniCParser.PrimitiveTypeContext) -> str:
        if ctx.INT():
            return "int"
        elif ctx.BOOL():
            return "bool"
        elif ctx.CHAR():
            return "char"
        elif ctx.STRING():
            return "string"
        elif ctx.VOID():
            return "void"
        elif ctx.Identifier():
            return ctx.Identifier().getText()  # Custom class type
        return None

    def visitBlockStatements(self, ctx: MiniCParser.BlockContext) -> List[Statement]:
        """Returns a list of statements from a block (without creating a Block node)"""
        statements = []
        for stmt_ctx in ctx.statement():
            stmt = self.visitStatement(stmt_ctx)
            if stmt:
                statements.append(stmt)
        return statements

    def visitStatement(self, ctx: MiniCParser.StatementContext) -> Statement:
        if ctx.variableDeclaration():
            return self.visitVariableDeclaration(ctx.variableDeclaration())
        elif ctx.ifStatement():
            return self.visitIfStatement(ctx.ifStatement())
        elif ctx.whileStatement():
            return self.visitWhileStatement(ctx.whileStatement())
        elif ctx.returnStatement():
            return self.visitReturnStatement(ctx.returnStatement())
        elif ctx.block():
            return BlockStatement(self.visitBlockStatements(ctx.block()))
        elif ctx.expression():
            expr = self.visitExpression(ctx.expression())
            return ExpressionStatement(expr)
        return None

    def visitExpression(self, ctx):
        """Helper method to visit expressions by their type"""
        if isinstance(ctx, MiniCParser.IdExprContext):
            return self.visitIdExpr(ctx)
        elif isinstance(ctx, MiniCParser.LiteralExprContext):
            return self.visitLiteralExpr(ctx)
        elif isinstance(ctx, MiniCParser.ParenExprContext):
            return self.visitParenExpr(ctx)
        elif isinstance(ctx, MiniCParser.UnaryExprContext):
            return self.visitUnaryExpr(ctx)
        elif isinstance(ctx, MiniCParser.MultiplicativeExprContext):
            return self.visitMultiplicativeExpr(ctx)
        elif isinstance(ctx, MiniCParser.AdditiveExprContext):
            return self.visitAdditiveExpr(ctx)
        elif isinstance(ctx, MiniCParser.ComparisonExprContext):
            return self.visitComparisonExpr(ctx)
        elif isinstance(ctx, MiniCParser.EqualityExprContext):
            return self.visitEqualityExpr(ctx)
        elif isinstance(ctx, MiniCParser.LogicAndExprContext):
            return self.visitLogicAndExpr(ctx)
        elif isinstance(ctx, MiniCParser.LogicOrExprContext):
            return self.visitLogicOrExpr(ctx)
        elif isinstance(ctx, MiniCParser.AssignmentExprContext):
            return self.visitAssignmentExpr(ctx)
        elif isinstance(ctx, MiniCParser.CallExprContext):
            return self.visitCallExpr(ctx)
        elif isinstance(ctx, MiniCParser.MemberAccessExprContext):
            return self.visitMemberAccessExpr(ctx)
        elif isinstance(ctx, MiniCParser.MethodCallExprContext):
            return self.visitMethodCallExpr(ctx)
        return None

    def visitIfStatement(self, ctx: MiniCParser.IfStatementContext) -> IfStatement:
        condition = self.visitExpression(ctx.expression())

        # then_stmt can be a single statement or a block
        then_stmt_ctx = ctx.statement(0)
        if then_stmt_ctx.block():
            then_stmt = self.visitBlockStatements(then_stmt_ctx.block())
        else:
            stmt = self.visitStatement(then_stmt_ctx)
            then_stmt = [stmt] if stmt else []

        # else_stmt is optional
        else_stmt = None
        if ctx.ELSE():
            else_stmt_ctx = ctx.statement(1)
            if else_stmt_ctx.block():
                else_stmt = self.visitBlockStatements(else_stmt_ctx.block())
            else:
                stmt = self.visitStatement(else_stmt_ctx)
                else_stmt = [stmt] if stmt else []

        return IfStatement(condition, then_stmt, else_stmt)

    def visitWhileStatement(self, ctx: MiniCParser.WhileStatementContext) -> WhileStatement:
        condition = self.visitExpression(ctx.expression())

        # body can be a single statement or a block
        body_ctx = ctx.statement()
        if body_ctx.block():
            body = self.visitBlockStatements(body_ctx.block())
        else:
            stmt = self.visitStatement(body_ctx)
            body = [stmt] if stmt else []

        return WhileStatement(condition, body)

    def visitReturnStatement(self, ctx: MiniCParser.ReturnStatementContext) -> ReturnStatement:
        expression = self.visitExpression(
            ctx.expression()) if ctx.expression() else None
        return ReturnStatement(expression)

    # Expression visitors
    def visitIdExpr(self, ctx: MiniCParser.IdExprContext) -> IdentifierExpression:
        name = ctx.Identifier().getText()
        return IdentifierExpression(name)

    def visitLiteralExpr(self, ctx: MiniCParser.LiteralExprContext) -> LiteralExpression:
        return self.visitLiteral(ctx.literal())

    def visitParenExpr(self, ctx: MiniCParser.ParenExprContext) -> Expression:
        return self.visitExpression(ctx.expression())

    def visitUnaryExpr(self, ctx: MiniCParser.UnaryExprContext) -> UnaryExpression:
        operator = ctx.getChild(0).getText()
        operand = self.visitExpression(ctx.expression())
        return UnaryExpression(operator, operand)

    def visitMultiplicativeExpr(self, ctx: MiniCParser.MultiplicativeExprContext) -> BinaryExpression:
        left = self.visitExpression(ctx.expression(0))
        operator = ctx.getChild(1).getText()
        right = self.visitExpression(ctx.expression(1))
        return BinaryExpression(left, operator, right)

    def visitAdditiveExpr(self, ctx: MiniCParser.AdditiveExprContext) -> BinaryExpression:
        left = self.visitExpression(ctx.expression(0))
        operator = ctx.getChild(1).getText()
        right = self.visitExpression(ctx.expression(1))
        return BinaryExpression(left, operator, right)

    def visitComparisonExpr(self, ctx: MiniCParser.ComparisonExprContext) -> BinaryExpression:
        left = self.visitExpression(ctx.expression(0))
        operator = ctx.getChild(1).getText()
        right = self.visitExpression(ctx.expression(1))
        return BinaryExpression(left, operator, right)

    def visitEqualityExpr(self, ctx: MiniCParser.EqualityExprContext) -> BinaryExpression:
        left = self.visitExpression(ctx.expression(0))
        operator = ctx.getChild(1).getText()
        right = self.visitExpression(ctx.expression(1))
        return BinaryExpression(left, operator, right)

    def visitLogicAndExpr(self, ctx: MiniCParser.LogicAndExprContext) -> BinaryExpression:
        left = self.visitExpression(ctx.expression(0))
        operator = "&&"
        right = self.visitExpression(ctx.expression(1))
        return BinaryExpression(left, operator, right)

    def visitLogicOrExpr(self, ctx: MiniCParser.LogicOrExprContext) -> BinaryExpression:
        left = self.visitExpression(ctx.expression(0))
        operator = "||"
        right = self.visitExpression(ctx.expression(1))
        return BinaryExpression(left, operator, right)

    def visitAssignmentExpr(self, ctx: MiniCParser.AssignmentExprContext) -> AssignmentExpression:
        target = self.visitExpression(ctx.expression(0))
        value = self.visitExpression(ctx.expression(1))
        return AssignmentExpression(target, value)

    def visitCallExpr(self, ctx: MiniCParser.CallExprContext) -> CallExpression:
        callee = ctx.Identifier().getText()
        arguments = self.visitArgumentList(
            ctx.argumentList()) if ctx.argumentList() else []
        return CallExpression(callee, arguments)

    def visitMemberAccessExpr(self, ctx: MiniCParser.MemberAccessExprContext) -> MemberAccessExpression:
        obj = self.visitExpression(ctx.expression())
        member = ctx.Identifier().getText()
        return MemberAccessExpression(obj, member)

    def visitMethodCallExpr(self, ctx: MiniCParser.MethodCallExprContext) -> MethodCallExpression:
        obj = self.visitExpression(ctx.expression())
        method = ctx.Identifier().getText()
        arguments = self.visitArgumentList(
            ctx.argumentList()) if ctx.argumentList() else []
        return MethodCallExpression(obj, method, arguments)

    def visitArgumentList(self, ctx: MiniCParser.ArgumentListContext) -> List[Expression]:
        return [self.visitExpression(expr) for expr in ctx.expression()]

    def visitLiteral(self, ctx: MiniCParser.LiteralContext) -> LiteralExpression:
        text = ctx.getText()

        if ctx.BoolLiteral():
            return LiteralExpression(text == "true", "bool")
        elif ctx.IntLiteral():
            return LiteralExpression(int(text), "int")
        elif ctx.CharLiteral():
            # Remove quotes from char literal
            char_value = text[1:-1]  # Remove surrounding single quotes
            return LiteralExpression(char_value, "char")
        elif ctx.StringLiteral():
            # Remove quotes from string literal
            string_value = text[1:-1]  # Remove surrounding double quotes
            return LiteralExpression(string_value, "string")

        return None
