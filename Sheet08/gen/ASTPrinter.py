from .AST import *

class ASTPrinter:
    """Pretty prints the AST structure with indentation"""
    
    def __init__(self, indent_size=2):
        self.indent_size = indent_size
        self.indent = 0
    
    def _print(self, text):
        print(" " * self.indent + text)
    
    def print_ast(self, node: ASTNode):
        """Main entry point to print an AST node"""
        node.accept(self)
    
    def _print_statement_list(self, statements: List[Statement]):
        """Helper to print a list of statements"""
        for stmt in statements:
            stmt.accept(self)
    
    # Program
    def visit_program(self, node: Program):
        self._print("Program")
        self.indent += self.indent_size
        for decl in node.declarations:
            decl.accept(self)
        self.indent -= self.indent_size
    
    # Declarations
    def visit_class_definition(self, node: ClassDefinition):
        parent_str = f" : {node.parent}" if node.parent else ""
        self._print(f"Class {node.name}{parent_str}")
        self.indent += self.indent_size
        for member in node.members:
            member.accept(self)
        self.indent -= self.indent_size
    
    def visit_function_definition(self, node: FunctionDefinition):
        self._print(f"Function {node.name}")
        self.indent += self.indent_size
        self._print("Return Type:")
        self.indent += self.indent_size
        node.return_type.accept(self)
        self.indent -= self.indent_size
        
        if node.parameters:
            self._print("Parameters:")
            self.indent += self.indent_size
            for param in node.parameters:
                param.accept(self)
            self.indent -= self.indent_size
        
        self._print("Body:")
        self.indent += self.indent_size
        self._print_statement_list(node.body)
        self.indent -= self.indent_size
        self.indent -= self.indent_size
    
    # Class Members
    def visit_method_definition(self, node: MethodDefinition):
        virtual_str = "virtual " if node.is_virtual else ""
        self._print(f"{virtual_str}Method {node.name}")
        self.indent += self.indent_size
        self._print("Return Type:")
        self.indent += self.indent_size
        node.return_type.accept(self)
        self.indent -= self.indent_size
        
        if node.parameters:
            self._print("Parameters:")
            self.indent += self.indent_size
            for param in node.parameters:
                param.accept(self)
            self.indent -= self.indent_size
        
        self._print("Body:")
        self.indent += self.indent_size
        self._print_statement_list(node.body)
        self.indent -= self.indent_size
        self.indent -= self.indent_size
    
    def visit_constructor_definition(self, node: ConstructorDefinition):
        self._print(f"Constructor {node.name}")
        self.indent += self.indent_size
        
        if node.parameters:
            self._print("Parameters:")
            self.indent += self.indent_size
            for param in node.parameters:
                param.accept(self)
            self.indent -= self.indent_size
        
        self._print("Body:")
        self.indent += self.indent_size
        self._print_statement_list(node.body)
        self.indent -= self.indent_size
        self.indent -= self.indent_size
    
    def visit_variable_declaration(self, node: VariableDeclaration):
        self._print(f"Variable {node.name}")
        self.indent += self.indent_size
        self._print("Type:")
        self.indent += self.indent_size
        node.var_type.accept(self)
        self.indent -= self.indent_size
        
        if node.initializer:
            self._print("Initializer:")
            self.indent += self.indent_size
            node.initializer.accept(self)
            self.indent -= self.indent_size
        self.indent -= self.indent_size
    
    # Types
    def visit_type(self, node: Type):
        ref_str = "&" if node.is_reference else ""
        self._print(f"{node.base_type}{ref_str}")
    
    def visit_parameter(self, node: Parameter):
        self._print(f"Parameter {node.name}")
        self.indent += self.indent_size
        node.param_type.accept(self)
        self.indent -= self.indent_size
    
    # Statements
    def visit_if_statement(self, node: IfStatement):
        self._print("If Statement")
        self.indent += self.indent_size
        self._print("Condition:")
        self.indent += self.indent_size
        node.condition.accept(self)
        self.indent -= self.indent_size
        
        self._print("Then:")
        self.indent += self.indent_size
        self._print_statement_list(node.then_stmt)
        self.indent -= self.indent_size
        
        if node.else_stmt:
            self._print("Else:")
            self.indent += self.indent_size
            self._print_statement_list(node.else_stmt)
            self.indent -= self.indent_size
        self.indent -= self.indent_size
    
    def visit_while_statement(self, node: WhileStatement):
        self._print("While Statement")
        self.indent += self.indent_size
        self._print("Condition:")
        self.indent += self.indent_size
        node.condition.accept(self)
        self.indent -= self.indent_size
        
        self._print("Body:")
        self.indent += self.indent_size
        self._print_statement_list(node.body)
        self.indent -= self.indent_size
        self.indent -= self.indent_size
    
    def visit_return_statement(self, node: ReturnStatement):
        self._print("Return Statement")
        if node.expression:
            self.indent += self.indent_size
            node.expression.accept(self)
            self.indent -= self.indent_size
    
    def visit_expression_statement(self, node: ExpressionStatement):
        self._print("Expression Statement")
        self.indent += self.indent_size
        node.expression.accept(self)
        self.indent -= self.indent_size
    
    # Expressions
    def visit_binary_expression(self, node: BinaryExpression):
        self._print(f"Binary Expression ({node.operator})")
        self.indent += self.indent_size
        self._print("Left:")
        self.indent += self.indent_size
        node.left.accept(self)
        self.indent -= self.indent_size
        
        self._print("Right:")
        self.indent += self.indent_size
        node.right.accept(self)
        self.indent -= self.indent_size
        self.indent -= self.indent_size
    
    def visit_unary_expression(self, node: UnaryExpression):
        self._print(f"Unary Expression ({node.operator})")
        self.indent += self.indent_size
        node.operand.accept(self)
        self.indent -= self.indent_size
    
    def visit_assignment_expression(self, node: AssignmentExpression):
        self._print("Assignment Expression")
        self.indent += self.indent_size
        self._print("Target:")
        self.indent += self.indent_size
        node.target.accept(self)
        self.indent -= self.indent_size
        
        self._print("Value:")
        self.indent += self.indent_size
        node.value.accept(self)
        self.indent -= self.indent_size
        self.indent -= self.indent_size
    
    def visit_call_expression(self, node: CallExpression):
        self._print(f"Call Expression: {node.callee}")
        if node.arguments:
            self.indent += self.indent_size
            self._print("Arguments:")
            self.indent += self.indent_size
            for arg in node.arguments:
                arg.accept(self)
            self.indent -= self.indent_size
            self.indent -= self.indent_size
    
    def visit_member_access_expression(self, node: MemberAccessExpression):
        self._print(f"Member Access: .{node.member}")
        self.indent += self.indent_size
        self._print("Object:")
        self.indent += self.indent_size
        node.object.accept(self)
        self.indent -= self.indent_size
        self.indent -= self.indent_size
    
    def visit_method_call_expression(self, node: MethodCallExpression):
        self._print(f"Method Call: .{node.method}")
        self.indent += self.indent_size
        self._print("Object:")
        self.indent += self.indent_size
        node.object.accept(self)
        self.indent -= self.indent_size
        
        if node.arguments:
            self._print("Arguments:")
            self.indent += self.indent_size
            for arg in node.arguments:
                arg.accept(self)
            self.indent -= self.indent_size
        self.indent -= self.indent_size
    
    def visit_identifier_expression(self, node: IdentifierExpression):
        self._print(f"Identifier: {node.name}")
    
    def visit_literal_expression(self, node: LiteralExpression):
        self._print(f"Literal ({node.literal_type}): {node.value}")
