from __future__ import annotations
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from antlr4 import FileStream, CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from gen.MiniCLexer import MiniCLexer
from gen.MiniCParser import MiniCParser
from gen.ASTBuilder import ASTBuilder
from gen import AST
from semantic import SemanticAnalyzer, SemanticError, ReferenceType, ClassSymbol, FunctionSymbol


"""
MiniC Interpreter

This interpreter executes MiniC programs by walking the Abstract Syntax Tree (AST).
It supports:
- Variable declarations and assignments (primitive types)
- Arithmetic, logical, and comparison expressions
- Control flow (if, while, return statements)
- Function definitions and calls with overloading
- Reference parameters (int& x)
- Class definitions with:
  - Field declarations
  - Constructors (default and custom)
  - Copy semantics
- Basic inheritance (static dispatch only, no virtual methods yet)
- Short-circuit evaluation for && and ||

Key limitations:
- Reference variables (outside function parameters) not fully supported
- Virtual methods not yet implemented (static dispatch only)
- Slicing and polymorphism not yet implemented
- Some edge cases in deep recursion (f95 function)
"""


class RuntimeError(Exception):
    pass


class ReturnException(Exception):
    """Used to implement return statements"""

    def __init__(self, value):
        self.value = value


class ObjectValue:
    """Represents an instance of a class"""

    def __init__(self, class_name: str, fields: Dict[str, Any]):
        self.class_name = class_name
        self.fields = fields
        self.vtable = {}  # Virtual method table: method_name -> actual implementation

    def __repr__(self):
        return f"<{self.class_name} object>"


class ReferenceValue:
    """Represents a reference to a variable"""

    def __init__(self, target_name: str, scope: Dict[str, Any]):
        self.target_name = target_name
        self.scope = scope

    def get(self) -> Any:
        # Follow the reference chain in case we have a reference to a reference
        value = self.scope[self.target_name]
        if isinstance(value, ReferenceValue):
            return value.get()
        return value

    def set(self, value: Any):
        # Follow the reference chain
        current = self.scope[self.target_name]
        if isinstance(current, ReferenceValue):
            current.set(value)
        else:
            self.scope[self.target_name] = value


class FieldReferenceValue:
    """Represents a reference to an object field"""

    def __init__(self, obj: ObjectValue, field_name: str):
        self.obj = obj
        self.field_name = field_name

    def get(self) -> Any:
        return self.obj.fields[self.field_name]

    def set(self, value: Any):
        self.obj.fields[self.field_name] = value


class Interpreter:
    def __init__(self, node_symbols: Dict[Any, Any] = None):
        self.scopes: List[Dict[str, Any]] = []
        self.classes: Dict[str, AST.ClassDefinition] = {}
        self.functions: Dict[str,
                             List[Tuple[AST.FunctionDefinition, Dict[str, Any]]]] = {}
        self.builtin_functions = {
            'print_int': self._builtin_print_int,
            'print_bool': self._builtin_print_bool,
            'print_char': self._builtin_print_char,
            'print_string': self._builtin_print_string,
        }
        self.output = []
        self.repl_mode = False
        self.node_symbols = node_symbols or {}
        # The first scope is our persistent session scope
        self.push_scope()

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def declare_variable(self, name: str, value: Any):
        self.scopes[-1][name] = value

    def resolve_variable(self, name: str) -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
        """Returns (value, scope_dict) or (None, None) if not found"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name], scope
        return None, None

    def set_variable(self, name: str, value: Any):
        """Set variable in the scope where it's defined"""
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        raise RuntimeError(f"Variable '{name}' not found.")

    def _builtin_print_int(self, value: int):
        self.output.append(str(value))

    def _builtin_print_bool(self, value: bool):
        self.output.append('1' if value else '0')

    def _builtin_print_char(self, value: str):
        if isinstance(value, str) and len(value) > 0:
            self.output.append(value[0])
        else:
            self.output.append(str(value))

    def _builtin_print_string(self, value: str):
        self.output.append(str(value))

    def interpret(self, ast: AST.Program):
        """Interpret the program"""
        # First pass: collect classes and functions
        for decl in ast.declarations:
            if isinstance(decl, AST.ClassDefinition):
                self.classes[decl.name] = decl
            elif isinstance(decl, AST.FunctionDefinition):
                if decl.name not in self.functions:
                    self.functions[decl.name] = []
                self.functions[decl.name].append((decl, {}))

        # Second pass: execute functions (look for main)
        if 'main' in self.functions:
            try:
                main_func = self.functions['main'][0][0]
                # Execute main body in the session scope
                for stmt in main_func.body:
                    self.visit_statement(stmt)
            except ReturnException:
                pass

    def visit_repl_node(self, node: Union[AST.Declaration, AST.Statement]):
        """Execute a single node (declaration or statement) in REPL mode"""
        if isinstance(node, AST.ClassDefinition):
            self.classes[node.name] = node
        elif isinstance(node, AST.FunctionDefinition):
            if node.name not in self.functions:
                self.functions[node.name] = []
            self.functions[node.name].append((node, {}))
        elif isinstance(node, AST.Statement):
            self.visit_statement(node)

    def visit_program(self, node: AST.Program):
        self.interpret(node)

    def visit_function_definition(self, node: AST.FunctionDefinition, args: List[Any]) -> Any:
        """Execute a function with given arguments"""
        old_scopes = self.scopes
        self.scopes = [{}]

        # Bind parameters
        for i, param in enumerate(node.parameters):
            if i < len(args):
                self.declare_variable(param.name, args[i])

        # Execute body
        try:
            for stmt in node.body:
                self.visit_statement(stmt)
            # No explicit return, return None/void
            return None
        except ReturnException as e:
            return e.value
        finally:
            self.scopes = old_scopes

    def visit_class_definition(self, node: AST.ClassDefinition):
        pass  # Classes are handled during instantiation

    def visit_method_definition(self, node: AST.MethodDefinition, obj: ObjectValue, args: List[Any]) -> Any:
        """Execute a method with given object and arguments"""
        old_scopes = self.scopes
        self.scopes = [{}]

        # Make object fields available as variables
        for field_name, field_value in obj.fields.items():
            self.declare_variable(field_name, field_value)

        # Bind parameters
        for i, param in enumerate(node.parameters):
            if i < len(args):
                self.declare_variable(param.name, args[i])

        # Execute body
        try:
            for stmt in node.body:
                self.visit_statement(stmt)
            return None
        except ReturnException as e:
            return e.value
        finally:
            # Update object fields from scope
            param_names = {p.name for p in node.parameters}
            for field_name in obj.fields:
                if field_name in self.scopes[-1] and field_name not in param_names:
                    obj.fields[field_name] = self.scopes[-1][field_name]

            self.scopes = old_scopes

    def visit_constructor_definition(self, node: AST.ConstructorDefinition, obj: ObjectValue, args: List[Any]):
        """Execute a constructor"""
        # Call parent's default constructor first if exists
        sym = self.node_symbols.get(node)
        from semantic import FunctionSymbol
        if isinstance(sym, FunctionSymbol) and sym.class_name:
            class_def = self.classes.get(sym.class_name)
            if class_def and class_def.parent:
                parent_def = self.classes.get(class_def.parent)
                if parent_def:
                    parent_ctor = self.find_constructor(parent_def, 0)
                    if parent_ctor:
                        self.visit_constructor_definition(parent_ctor, obj, [])

        old_scopes = self.scopes
        self.scopes = [{}]

        # Make object fields available as variables
        for field_name, field_value in obj.fields.items():
            self.declare_variable(field_name, field_value)

        # Bind parameters
        for i, param in enumerate(node.parameters):
            if i < len(args):
                self.declare_variable(param.name, args[i])

        # Execute body
        try:
            for stmt in node.body:
                self.visit_statement(stmt)
        except ReturnException:
            pass
        finally:
            # Update object fields from scope
            # Ensure we don't overwrite fields with parameters that shaded them
            param_names = {p.name for p in node.parameters}
            for field_name in obj.fields:
                if field_name in self.scopes[-1] and field_name not in param_names:
                    obj.fields[field_name] = self.scopes[-1][field_name]

            self.scopes = old_scopes

    def visit_variable_declaration(self, node: AST.VariableDeclaration):
        """Declare a variable"""
        value = None

        # Check if this is a reference type
        if node.var_type.is_reference:
            # For reference types, we must have an initializer
            if not node.initializer:
                raise RuntimeError(
                    f"Reference '{node.name}' must be initialized.")

            # For reference variables, we need to extract the variable name from the initializer
            if isinstance(node.initializer, AST.IdentifierExpression):
                # Simple case: T& x = y;
                target_var_name = node.initializer.name
                target_val, target_scope = self.resolve_variable(
                    target_var_name)
                if target_scope is None:
                    raise RuntimeError(
                        f"Cannot initialize reference with undefined variable '{target_var_name}'.")
                value = ReferenceValue(target_var_name, target_scope)
            elif isinstance(node.initializer, AST.MemberAccessExpression):
                # Case: T& x = obj.field;
                # This is more complex - we'll evaluate it as a reference
                obj_val = self.visit_expression(node.initializer.object)
                if isinstance(obj_val, ObjectValue):
                    # Create a special reference to an object field
                    # For now, just store the object and field name
                    value = FieldReferenceValue(
                        obj_val, node.initializer.member)
                else:
                    raise RuntimeError(
                        "Cannot initialize reference with non-object member access.")
            else:
                raise RuntimeError(
                    f"Reference '{node.name}' must be initialized with an lvalue.")
        # Check if this is a class type
        elif node.var_type.base_type in self.classes:
            # Instantiate the class
            if node.initializer:
                # User provided an initializer (e.g., A x = A(5); or A x = b; where b is a subclass)
                value = self.visit_expression(node.initializer)

                # Check if we need to slice (assigning a derived object to a base variable)
                if isinstance(value, ObjectValue) and value.class_name != node.var_type.base_type:
                    # Check if value.class_name is a subclass of node.var_type.base_type
                    if self.is_subclass(value.class_name, node.var_type.base_type):
                        # Slice: create a new object of the base type and copy only base fields
                        sliced_obj = ObjectValue(node.var_type.base_type, {})
                        base_class_def = self.classes[node.var_type.base_type]
                        # Collect only the base class fields
                        self.collect_fields(base_class_def, sliced_obj)
                        # Copy the base class fields from the original object
                        for field_name in sliced_obj.fields:
                            if field_name in value.fields:
                                sliced_obj.fields[field_name] = value.fields[field_name]
                        value = sliced_obj
            else:
                # Use default constructor
                value = self.instantiate_class(node.var_type.base_type, [])
        else:
            # Primitive type
            if node.initializer:
                value = self.visit_expression(node.initializer)

        self.declare_variable(node.name, value)

    def visit_statement(self, stmt: AST.Statement):
        if isinstance(stmt, AST.VariableDeclaration):
            self.visit_variable_declaration(stmt)
        elif isinstance(stmt, AST.ExpressionStatement):
            return self.visit_expression_statement(stmt)
        elif isinstance(stmt, AST.BlockStatement):
            self.visit_block_statement(stmt)
        elif isinstance(stmt, AST.IfStatement):
            self.visit_if_statement(stmt)
        elif isinstance(stmt, AST.WhileStatement):
            self.visit_while_statement(stmt)
        elif isinstance(stmt, AST.ReturnStatement):
            self.visit_return_statement(stmt)

    def visit_expression_statement(self, stmt: AST.ExpressionStatement) -> Any:
        result = self.visit_expression(stmt.expression)
        if self.repl_mode:
            # We skip 'None' which is returned by void functions or expressions that don't produce a value
            # But the requirement says "only the result of expression-statements"
            # In C++, almost everything is an expression.
            if result is not None:
                print(result)
        return result

    def visit_block_statement(self, stmt: AST.BlockStatement):
        """Execute a block statement with new scope"""
        self.push_scope()
        try:
            for inner_stmt in stmt.statements:
                self.visit_statement(inner_stmt)
        finally:
            self.pop_scope()

    def visit_if_statement(self, stmt: AST.IfStatement):
        condition = self.visit_expression(stmt.condition)
        if self.is_truthy(condition):
            self.push_scope()
            for s in stmt.then_stmt:
                self.visit_statement(s)
            self.pop_scope()
        elif stmt.else_stmt:
            self.push_scope()
            for s in stmt.else_stmt:
                self.visit_statement(s)
            self.pop_scope()

    def visit_while_statement(self, stmt: AST.WhileStatement):
        while self.is_truthy(self.visit_expression(stmt.condition)):
            self.push_scope()
            for s in stmt.body:
                self.visit_statement(s)
            self.pop_scope()

    def visit_return_statement(self, stmt: AST.ReturnStatement):
        value = None
        if stmt.expression:
            value = self.visit_expression(stmt.expression)
        raise ReturnException(value)

    def visit_expression(self, expr: AST.Expression) -> Any:
        if isinstance(expr, AST.LiteralExpression):
            return self.visit_literal_expression(expr)
        elif isinstance(expr, AST.IdentifierExpression):
            return self.visit_identifier_expression(expr)
        elif isinstance(expr, AST.BinaryExpression):
            return self.visit_binary_expression(expr)
        elif isinstance(expr, AST.UnaryExpression):
            return self.visit_unary_expression(expr)
        elif isinstance(expr, AST.AssignmentExpression):
            return self.visit_assignment_expression(expr)
        elif isinstance(expr, AST.CallExpression):
            return self.visit_call_expression(expr)
        elif isinstance(expr, AST.MemberAccessExpression):
            return self.visit_member_access_expression(expr)
        elif isinstance(expr, AST.MethodCallExpression):
            return self.visit_method_call_expression(expr)
        else:
            raise RuntimeError(f"Unknown expression type: {type(expr)}")

    def visit_literal_expression(self, expr: AST.LiteralExpression) -> Any:
        if expr.literal_type == 'int':
            return int(expr.value)
        elif expr.literal_type == 'bool':
            if isinstance(expr.value, bool):
                return expr.value
            return str(expr.value).lower() == 'true'
        elif expr.literal_type == 'char':
            # Remove quotes
            s = str(expr.value)
            if s.startswith("'") and s.endswith("'"):
                s = s[1:-1]
            return s
        elif expr.literal_type == 'string':
            # Remove quotes
            s = str(expr.value)
            if s.startswith('"') and s.endswith('"'):
                s = s[1:-1]
            return s
        else:
            return expr.value

    def visit_identifier_expression(self, expr: AST.IdentifierExpression) -> Any:
        value, scope = self.resolve_variable(expr.name)
        if scope is None:
            raise RuntimeError(f"Undefined variable '{expr.name}'.")

        # If it's a reference, get the referenced value
        if isinstance(value, ReferenceValue):
            return value.get()
        return value

    def visit_binary_expression(self, expr: AST.BinaryExpression) -> Any:
        # Handle short-circuit evaluation for logical operators
        if expr.operator == '&&':
            left = self.visit_expression(expr.left)
            if not self.is_truthy(left):
                return False
            right = self.visit_expression(expr.right)
            return self.is_truthy(left) and self.is_truthy(right)
        elif expr.operator == '||':
            left = self.visit_expression(expr.left)
            if self.is_truthy(left):
                return True
            right = self.visit_expression(expr.right)
            return self.is_truthy(left) or self.is_truthy(right)

        # For other operators, evaluate both sides
        left = self.visit_expression(expr.left)
        right = self.visit_expression(expr.right)

        if expr.operator == '+':
            return left + right
        elif expr.operator == '-':
            return left - right
        elif expr.operator == '*':
            return left * right
        elif expr.operator == '/':
            if right == 0:
                raise RuntimeError("Division by zero")
            return left // right  # Integer division
        elif expr.operator == '%':
            return left % right
        elif expr.operator == '<':
            return left < right
        elif expr.operator == '<=':
            return left <= right
        elif expr.operator == '>':
            return left > right
        elif expr.operator == '>=':
            return left >= right
        elif expr.operator == '==':
            return left == right
        elif expr.operator == '!=':
            return left != right
        else:
            raise RuntimeError(f"Unknown operator: {expr.operator}")

    def visit_unary_expression(self, expr: AST.UnaryExpression) -> Any:
        operand = self.visit_expression(expr.operand)

        if expr.operator == '!':
            return not self.is_truthy(operand)
        elif expr.operator == '+':
            return +operand
        elif expr.operator == '-':
            return -operand
        else:
            raise RuntimeError(f"Unknown unary operator: {expr.operator}")

    def visit_assignment_expression(self, expr: AST.AssignmentExpression) -> Any:
        value = self.visit_expression(expr.value)

        # Handle different target types
        if isinstance(expr.target, AST.IdentifierExpression):
            target_value, scope = self.resolve_variable(expr.target.name)
            if scope is None:
                raise RuntimeError(f"Undefined variable '{expr.target.name}'.")

            if isinstance(target_value, ReferenceValue):
                target_value.set(value)
            else:
                # Check if we're assigning an object
                if isinstance(target_value, ObjectValue) and isinstance(value, ObjectValue):
                    # For object assignment, copy the fields
                    target_value.fields.clear()
                    target_value.fields.update(value.fields)
                else:
                    self.set_variable(expr.target.name, value)
        elif isinstance(expr.target, AST.MemberAccessExpression):
            obj = self.visit_expression(expr.target.object)
            if isinstance(obj, ObjectValue):
                obj.fields[expr.target.member] = value
            else:
                raise RuntimeError("Cannot access member of non-object")
        else:
            raise RuntimeError("Invalid assignment target")

        return value

    def visit_call_expression(self, expr: AST.CallExpression) -> Any:
        # Check if it's a builtin function
        if expr.callee in self.builtin_functions:
            args = [self.visit_expression(arg) for arg in expr.arguments]
            self.builtin_functions[expr.callee](*args)
            return None

        # Check if it's a constructor call
        if expr.callee in self.classes:
            return self.instantiate_class(expr.callee, expr.arguments)

        # Check if it's a user-defined function
        sym = self.node_symbols.get(expr)
        if isinstance(sym, (AST.FunctionDefinition, AST.MethodDefinition, AST.ConstructorDefinition)):
            # Fallback if node_symbols contains the node itself
            func_def = sym
            args = []
            for i, arg_expr in enumerate(expr.arguments):
                args.append(self.visit_expression(arg_expr))
            return self.visit_function_definition(func_def, args)

        if isinstance(sym, FunctionSymbol) and sym.ast_node:
            func_def = sym.ast_node
            args = []
            for i, arg_expr in enumerate(expr.arguments):
                if i < len(sym.parameters):
                    param_type = sym.parameters[i].type
                    if isinstance(param_type, ReferenceType):
                        if isinstance(arg_expr, AST.IdentifierExpression):
                            val, scope = self.resolve_variable(arg_expr.name)
                            args.append(ReferenceValue(arg_expr.name, scope))
                        elif isinstance(arg_expr, AST.MemberAccessExpression):
                            obj_val = self.visit_expression(arg_expr.object)
                            if isinstance(obj_val, ObjectValue):
                                args.append(FieldReferenceValue(
                                    obj_val, arg_expr.member))
                            else:
                                args.append(self.visit_expression(arg_expr))
                        else:
                            args.append(self.visit_expression(arg_expr))
                    else:
                        args.append(self.visit_expression(arg_expr))
                else:
                    args.append(self.visit_expression(arg_expr))
            return self.visit_function_definition(func_def, args)

        # Fallback to name search (less reliable for overloading)
        if expr.callee in self.functions:
            overloads = self.functions[expr.callee]
            for func_def, closure in overloads:
                if len(func_def.parameters) == len(expr.arguments):
                    args = [self.visit_expression(arg)
                            for arg in expr.arguments]
                    return self.visit_function_definition(func_def, args)

        raise RuntimeError(f"Unknown function '{expr.callee}'.")

    def visit_method_call_expression(self, expr: AST.MethodCallExpression) -> Any:
        obj = self.visit_expression(expr.object)

        if not isinstance(obj, ObjectValue):
            raise RuntimeError("Cannot call method on non-object")

        sym = self.node_symbols.get(expr)

        if isinstance(sym, FunctionSymbol):
            method_def = sym.ast_node

            # Virtual dispatch
            if sym.is_virtual:
                # Look for the method in the dynamic type
                dynamic_class_def = self.classes.get(obj.class_name)
                actual_method = self.find_method(
                    dynamic_class_def, expr.method)
                if actual_method:
                    method_def = actual_method

            if not method_def:
                raise RuntimeError(f"Method '{expr.method}' not found.")

            # Prepare arguments
            args = []
            for i, arg_expr in enumerate(expr.arguments):
                if i < len(sym.parameters):
                    param_type = sym.parameters[i].type
                    if isinstance(param_type, ReferenceType):
                        if isinstance(arg_expr, AST.IdentifierExpression):
                            val, scope = self.resolve_variable(arg_expr.name)
                            args.append(ReferenceValue(arg_expr.name, scope))
                        elif isinstance(arg_expr, AST.MemberAccessExpression):
                            obj_val = self.visit_expression(arg_expr.object)
                            if isinstance(obj_val, ObjectValue):
                                args.append(FieldReferenceValue(
                                    obj_val, arg_expr.member))
                            else:
                                args.append(self.visit_expression(arg_expr))
                        else:
                            args.append(self.visit_expression(arg_expr))
                    else:
                        args.append(self.visit_expression(arg_expr))
                else:
                    args.append(self.visit_expression(arg_expr))

            return self.visit_method_definition(method_def, obj, args)

        # Fallback
        class_def = self.classes.get(obj.class_name)
        if not class_def:
            raise RuntimeError(f"Class '{obj.class_name}' not found.")

        method = self.find_method(class_def, expr.method)
        if not method:
            raise RuntimeError(
                f"Method '{expr.method}' not found in class '{obj.class_name}'.")

        args = [self.visit_expression(arg) for arg in expr.arguments]
        return self.visit_method_definition(method, obj, args)

    def visit_member_access_expression(self, expr: AST.MemberAccessExpression) -> Any:
        obj = self.visit_expression(expr.object)

        if not isinstance(obj, ObjectValue):
            raise RuntimeError("Cannot access member of non-object")

        if expr.member not in obj.fields:
            raise RuntimeError(
                f"Field '{expr.member}' not found in class '{obj.class_name}'.")

        return obj.fields[expr.member]

    def instantiate_class(self, class_name: str, arguments: List[AST.Expression]) -> ObjectValue:
        """Create an instance of a class"""
        class_def = self.classes.get(class_name)
        if not class_def:
            raise RuntimeError(f"Class '{class_name}' not found.")

        # Initialize fields with default values
        obj = ObjectValue(class_name, {})

        # Collect fields from class hierarchy
        self.collect_fields(class_def, obj)

        # Evaluate arguments
        args = [self.visit_expression(arg) for arg in arguments]

        # Call parent's default constructor if this class has a parent
        if class_def.parent:
            parent_def = self.classes.get(class_def.parent)
            if parent_def:
                # Find parent's default constructor (no arguments)
                parent_default_constructor = self.find_constructor(
                    parent_def, 0, [])
                if parent_default_constructor:
                    self.visit_constructor_definition(
                        parent_default_constructor, obj, [])

        # Find and call the appropriate constructor
        constructor = self.find_constructor(class_def, len(args), args)
        if constructor:
            self.visit_constructor_definition(constructor, obj, args)
        elif len(args) == 1 and isinstance(args[0], ObjectValue) and args[0].class_name == class_name:
            # Implicit copy constructor
            for field_name, field_value in args[0].fields.items():
                obj.fields[field_name] = field_value

        return obj

    def collect_fields(self, class_def: AST.ClassDefinition, obj: ObjectValue):
        """Collect fields from class and parent classes"""
        # Collect from parent first (if any)
        if class_def.parent:
            parent_def = self.classes.get(class_def.parent)
            if parent_def:
                self.collect_fields(parent_def, obj)

        # Collect from this class
        for member in class_def.members:
            if isinstance(member, AST.VariableDeclaration):
                value = None
                if member.initializer:
                    value = self.visit_expression(member.initializer)
                obj.fields[member.name] = value

    def is_subclass(self, derived_name: str, base_name: str) -> bool:
        """Check if derived_name is a subclass of base_name"""
        if derived_name == base_name:
            return True

        class_def = self.classes.get(derived_name)
        if not class_def:
            return False

        if class_def.parent:
            return self.is_subclass(class_def.parent, base_name)

        return False

    def find_method(self, class_def: AST.ClassDefinition, method_name: str) -> Optional[AST.MethodDefinition]:
        """Find a method in class or parent classes"""
        for member in class_def.members:
            if isinstance(member, AST.MethodDefinition) and member.name == method_name:
                return member

        # Check parent
        if class_def.parent:
            parent_def = self.classes.get(class_def.parent)
            if parent_def:
                return self.find_method(parent_def, method_name)

        return None

    def find_constructor(self, class_def: AST.ClassDefinition, arg_count: int, arg_types: List[Any] = None) -> Optional[AST.ConstructorDefinition]:
        """Find a constructor with matching argument count and types"""
        # If arg_count is 1 and it's an object of the same class, prefer implicit copy constructor
        if arg_count == 1 and arg_types and len(arg_types) > 0:
            arg_type = arg_types[0]
            if isinstance(arg_type, ObjectValue) and arg_type.class_name == class_def.name:
                return None  # Use implicit copy constructor

        # Look for explicit constructors
        for member in class_def.members:
            if isinstance(member, AST.ConstructorDefinition) and len(member.parameters) == arg_count:
                return member

        # If no explicit constructor found and arg_count is 0, use implicit default constructor
        if arg_count == 0:
            return None  # Use implicit default constructor

        return None

    def is_truthy(self, value: Any) -> bool:
        """Convert value to boolean"""
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, ObjectValue):
            return True
        return bool(value)


def run_interpreter(path: Path) -> Tuple[bool, str]:
    """Run interpreter on a file and return (success, output)"""
    try:
        # Parse
        input_stream = FileStream(str(path), encoding="utf-8")
        lexer = MiniCLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = MiniCParser(token_stream)

        class BailErrorListener(ErrorListener):
            def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
                raise SemanticError(f"Syntax Error at {line}:{column}: {msg}")

        parser.removeErrorListeners()
        parser.addErrorListener(BailErrorListener())

        tree = parser.program()

        # Build AST
        ast_builder = ASTBuilder()
        ast = ast_builder.visitProgram(tree)

        # Semantic analysis
        analyzer = SemanticAnalyzer()
        analyzer.visit_program(ast)

        # Interpret
        interpreter = Interpreter(analyzer.node_symbols)
        interpreter.interpret(ast)

        output = '\n'.join(interpreter.output)
        return True, output

    except (SemanticError, RuntimeError) as e:
        return False, str(e)
    except Exception as e:
        return False, f"Internal error: {str(e)}"


class CollectErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Syntax Error at {line}:{column}: {msg}")


def is_complete_input(text: str) -> bool:
    text = text.strip()
    if not text:
        return True

    # Check brace/paren balance
    if text.count('{') > text.count('}'):
        return False
    if text.count('(') > text.count(')'):
        return False

    # Heuristic for complete statement/declaration:
    # Must end in ; or }
    if not (text.endswith(';') or text.endswith('}')):
        return False

    return True


def run_repl(initial_file: Optional[Path] = None):
    analyzer = SemanticAnalyzer()
    interpreter = Interpreter(analyzer.node_symbols)
    ast_builder = ASTBuilder()

    # Initial file processing
    if initial_file:
        try:
            input_stream = FileStream(str(initial_file), encoding="utf-8")
            lexer = MiniCLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = MiniCParser(token_stream)

            error_listener = CollectErrorListener()
            parser.removeErrorListeners()
            parser.addErrorListener(error_listener)

            tree = parser.program()
            if error_listener.errors:
                for err in error_listener.errors:
                    print(err, file=sys.stderr)
                return

            ast = ast_builder.visitProgram(tree)
            analyzer.visit_program(ast)
            interpreter.interpret(ast)

            if interpreter.output:
                print("\n".join(interpreter.output))
                interpreter.output = []

        except (SemanticError, RuntimeError) as e:
            print(f"Error during initialization: {e}", file=sys.stderr)
        except Exception as e:
            print(
                f"Internal error during initialization: {e}", file=sys.stderr)

    interpreter.repl_mode = True
    print("\nMiniC REPL")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            code_lines = []
            while True:
                prompt = ">>> " if not code_lines else "... "
                line = input(prompt)

                if line.strip().lower() == "exit":
                    return

                code_lines.append(line)
                code = "\n".join(code_lines)

                if is_complete_input(code):
                    break

            if not code.strip():
                continue

            # Parse input
            input_stream = InputStream(code)
            lexer = MiniCLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = MiniCParser(token_stream)

            error_listener = CollectErrorListener()
            parser.removeErrorListeners()
            parser.addErrorListener(error_listener)

            # Try parsing as program (declarations) first
            tree = parser.program()

            nodes = []
            # We check if it matched at least one declaration and reached EOF
            if not error_listener.errors and tree.children and token_stream.LA(1) == -1:
                program_ast = ast_builder.visitProgram(tree)
                nodes = program_ast.declarations
            else:
                # Try parsing as statement
                token_stream.seek(0)
                parser.reset()
                error_listener.errors = []
                tree = parser.statement()
                # LA(1) == -1 is EOF
                if not error_listener.errors and (token_stream.LA(1) == -1):
                    nodes = [ast_builder.visitStatement(tree)]
                else:
                    if not error_listener.errors:
                        print(
                            "Syntax Error: Incomplete input or trailing characters.", file=sys.stderr)
                    else:
                        for err in error_listener.errors:
                            print(err, file=sys.stderr)
                    continue

            # Execute nodes
            for node in nodes:
                try:
                    analyzer.analyze_repl_node(node)
                    interpreter.visit_repl_node(node)

                    if interpreter.output:
                        print("\n".join(interpreter.output))
                        interpreter.output = []
                except (SemanticError, RuntimeError) as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Internal error: {e}")

        except EOFError:
            print("\nExiting...")
            break
        except KeyboardInterrupt:
            print("\nInterrupt")
            continue


def extract_expected_output(file_path: Path) -> Optional[str]:
    """Extract expected output from /* EXPECT: ... */ comment"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Look for /* EXPECT: ... */ or /* EXPECT (.*?): ... */
    import re
    match = re.search(
        r'/\*\s*EXPECT\s*(?:\([^)]*\))?\s*:\s*(.*?)\*/', content, re.DOTALL)
    if match:
        lines = match.group(1).strip().split('\n')
        # Clean up each line (remove leading/trailing whitespace and comments)
        lines = [line.strip() for line in lines if line.strip()]
        return '\n'.join(lines)
    return None


def run_suite(path: Path):
    """Run a test suite"""
    print(f"\nTesting {path.name}:")
    passed = 0
    total = 0
    files = sorted(path.glob("*.cpp"))

    for f in files:
        total += 1
        success, output = run_interpreter(f)

        if success:
            expected = extract_expected_output(f)
            if expected is None:
                print(f"  [SKIP] {f.name} (no EXPECT comment)")
                total -= 1
                continue

            if output == expected:
                print(f"  [PASS] {f.name}")
                passed += 1
            else:
                print(f"  [FAIL] {f.name}")
                print(f"    Expected:\n{expected}")
                print(f"    Got:\n{output}")
        else:
            print(f"  [FAIL] {f.name}")
            print(f"    {output}")

    return passed, total


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            base = Path(__file__).parent / "tests"
            p_passed, p_total = run_suite(base / "positive")
            print(f"\nSummary: {p_passed}/{p_total} tests passed")
            sys.exit(0 if p_passed == p_total else 1)
        path = Path(sys.argv[1])
        if path.exists() and path.is_file():
            run_repl(path)
        else:
            print(f"Error: File {path} not found.")
            sys.exit(1)
    else:
        run_repl()
