from abc import ABC, abstractmethod
from typing import List, Optional

# Base AST Node
class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

# Program
class Program(ASTNode):
    def __init__(self, declarations: List['Declaration']):
        self.declarations = declarations
    
    def accept(self, visitor):
        return visitor.visit_program(self)

# Declarations
class Declaration(ASTNode):
    pass

class ClassDefinition(Declaration):
    def __init__(self, name: str, parent: Optional[str], members: List['ClassMember']):
        self.name = name
        self.parent = parent
        self.members = members
    
    def accept(self, visitor):
        return visitor.visit_class_definition(self)

class FunctionDefinition(Declaration):
    def __init__(self, return_type: 'Type', name: str, parameters: List['Parameter'], body: 'Block'):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_function_definition(self)

# Class Members
class ClassMember(ASTNode):
    pass

class MethodDefinition(ClassMember):
    def __init__(self, is_virtual: bool, return_type: 'Type', name: str, parameters: List['Parameter'], body: 'Block'):
        self.is_virtual = is_virtual
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_method_definition(self)

class ConstructorDefinition(ClassMember):
    def __init__(self, name: str, parameters: List['Parameter'], body: 'Block'):
        self.name = name
        self.parameters = parameters
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_constructor_definition(self)

class VariableDeclaration(ClassMember):
    def __init__(self, var_type: 'Type', name: str, initializer: Optional['Expression']):
        self.var_type = var_type
        self.name = name
        self.initializer = initializer
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)

# Types
class Type(ASTNode):
    def __init__(self, base_type: str, is_reference: bool = False):
        self.base_type = base_type
        self.is_reference = is_reference
    
    def accept(self, visitor):
        return visitor.visit_type(self)

class Parameter(ASTNode):
    def __init__(self, param_type: Type, name: str):
        self.param_type = param_type
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_parameter(self)

# Statements
class Statement(ASTNode):
    pass

class Block(Statement):
    def __init__(self, statements: List[Statement]):
        self.statements = statements
    
    def accept(self, visitor):
        return visitor.visit_block(self)

class IfStatement(Statement):
    def __init__(self, condition: 'Expression', then_stmt: Statement, else_stmt: Optional[Statement]):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)

class WhileStatement(Statement):
    def __init__(self, condition: 'Expression', body: Statement):
        self.condition = condition
        self.body = body
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)

class ReturnStatement(Statement):
    def __init__(self, expression: Optional['Expression']):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)

class ExpressionStatement(Statement):
    def __init__(self, expression: 'Expression'):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)

# Expressions
class Expression(ASTNode):
    pass

class BinaryExpression(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)

class UnaryExpression(Expression):
    def __init__(self, operator: str, operand: Expression):
        self.operator = operator
        self.operand = operand
    
    def accept(self, visitor):
        return visitor.visit_unary_expression(self)

class AssignmentExpression(Expression):
    def __init__(self, target: Expression, value: Expression):
        self.target = target
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_assignment_expression(self)

class CallExpression(Expression):
    def __init__(self, callee: str, arguments: List[Expression]):
        self.callee = callee
        self.arguments = arguments
    
    def accept(self, visitor):
        return visitor.visit_call_expression(self)

class MemberAccessExpression(Expression):
    def __init__(self, object: Expression, member: str):
        self.object = object
        self.member = member
    
    def accept(self, visitor):
        return visitor.visit_member_access_expression(self)

class MethodCallExpression(Expression):
    def __init__(self, object: Expression, method: str, arguments: List[Expression]):
        self.object = object
        self.method = method
        self.arguments = arguments
    
    def accept(self, visitor):
        return visitor.visit_method_call_expression(self)

class IdentifierExpression(Expression):
    def __init__(self, name: str):
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_identifier_expression(self)

class LiteralExpression(Expression):
    def __init__(self, value, literal_type: str):
        self.value = value
        self.literal_type = literal_type
    
    def accept(self, visitor):
        return visitor.visit_literal_expression(self)