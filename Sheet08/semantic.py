from __future__ import annotations
import sys
from pathlib import Path
from typing import List, Dict, Optional, Union, Any, Tuple

from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from gen.MiniCLexer import MiniCLexer
from gen.MiniCParser import MiniCParser
from gen.ASTBuilder import ASTBuilder
from gen import AST


class SemanticError(Exception):
    pass


class TypeSymbol:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, TypeSymbol):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


class PrimitiveTypeSymbol(TypeSymbol):
    pass


class VariableSymbol:
    def __init__(self, name: str, type_sym: TypeSymbol):
        self.name = name
        self.type = type_sym


class FunctionSymbol:
    def __init__(self, name: str, return_type: TypeSymbol, parameters: List[VariableSymbol], is_method=False, is_virtual=False, class_name=None):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.is_method = is_method
        self.is_virtual = is_virtual
        self.class_name = class_name
        self.is_defined = False

    def __str__(self):
        params = ", ".join([str(p.type) for p in self.parameters])
        return f"{self.return_type} {self.name}({params})"

    @property
    def signature(self):
        param_types = tuple(str(p.type) for p in self.parameters)
        return (self.name, param_types)


class ClassSymbol(TypeSymbol):
    def __init__(self, name: str, parent: Optional[str]):
        super().__init__(name)
        self.parent_name = parent
        self.members: Dict[str,
                           Union[VariableSymbol, List[FunctionSymbol]]] = {}
        self.parent: Optional[ClassSymbol] = None
        self.is_defined = False


class SymbolTable:
    def __init__(self):
        self.scopes: List[Dict[str, Any]] = []
        self.classes: Dict[str, ClassSymbol] = {}
        self.functions: Dict[str, List[FunctionSymbol]] = {}

        self.void_type = PrimitiveTypeSymbol("void")
        self.int_type = PrimitiveTypeSymbol("int")
        self.bool_type = PrimitiveTypeSymbol("bool")
        self.char_type = PrimitiveTypeSymbol("char")
        self.string_type = PrimitiveTypeSymbol("string")

        self.push_scope()

        self.add_builtin_function(
            "print_bool", self.void_type, [self.bool_type])
        self.add_builtin_function("print_int", self.void_type, [self.int_type])
        self.add_builtin_function(
            "print_char", self.void_type, [self.char_type])
        self.add_builtin_function(
            "print_string", self.void_type, [self.string_type])

    def add_builtin_function(self, name, ret_type, param_types):
        params = [VariableSymbol(f"p{i}", t)
                  for i, t in enumerate(param_types)]
        fn = FunctionSymbol(name, ret_type, params)
        fn.is_defined = True
        if name not in self.functions:
            self.functions[name] = []
        self.functions[name].append(fn)

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def declare_variable(self, name: str, type_sym: TypeSymbol):
        if name in self.scopes[-1]:
            raise SemanticError(
                f"Redeclaration of variable '{name}' in the same scope.")
        self.scopes[-1][name] = VariableSymbol(name, type_sym)

    def resolve_variable(self, name: str) -> Optional[VariableSymbol]:
        for scope in reversed(self.scopes):
            if name in scope:
                sym = scope[name]
                if isinstance(sym, VariableSymbol):
                    return sym
        return None

    def declare_class(self, name: str, parent: Optional[str]) -> ClassSymbol:
        reserved = [t.name for t in [self.int_type, self.bool_type,
                                     self.char_type, self.string_type, self.void_type]]
        if name in self.classes or name in reserved:
            raise SemanticError(f"Redeclaration of type '{name}'.")
        cls = ClassSymbol(name, parent)
        self.classes[name] = cls
        return cls

    def resolve_type(self, name: str) -> TypeSymbol:
        if name == "int":
            return self.int_type
        if name == "bool":
            return self.bool_type
        if name == "char":
            return self.char_type
        if name == "string":
            return self.string_type
        if name == "void":
            return self.void_type
        if name in self.classes:
            return self.classes[name]
        raise SemanticError(f"Unknown type '{name}'.")

    def declare_function(self, func: FunctionSymbol):
        if func.name in self.classes:
            raise SemanticError(
                f"Function name '{func.name}' conflicts with class name.")

        candidates = self.functions.get(func.name, [])
        for f in candidates:
            if f.signature == func.signature:
                raise SemanticError(
                    f"Redeclaration of function '{func.name}' with same signature.")

        if func.name not in self.functions:
            self.functions[func.name] = []
        self.functions[func.name].append(func)


class ReferenceType(TypeSymbol):
    def __init__(self, inner: TypeSymbol):
        super().__init__(f"{inner.name}&")
        self.inner = inner


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.node_symbols: Dict[Any, Any] = {}
        self.current_class: Optional[ClassSymbol] = None
        self.current_function: Optional[FunctionSymbol] = None

    def visit_program(self, node: AST.Program):
        for decl in node.declarations:
            if isinstance(decl, AST.ClassDefinition):
                self.collect_class(decl)
            elif isinstance(decl, AST.FunctionDefinition):
                self.collect_function(decl)

        self.resolve_inheritance()

        for decl in node.declarations:
            if isinstance(decl, AST.ClassDefinition):
                self.analyze_class_body(decl)
            elif isinstance(decl, AST.FunctionDefinition):
                self.analyze_function_body(decl)

    def type_from_ast(self, type_node: AST.Type) -> TypeSymbol:
        base = self.symbol_table.resolve_type(type_node.base_type)
        if type_node.is_reference:
            if base == self.symbol_table.void_type:
                raise SemanticError("Cannot declare reference to void.")
            return ReferenceType(base)
        return base

    def collect_class(self, node: AST.ClassDefinition):
        self.symbol_table.declare_class(node.name, node.parent)

    def collect_function(self, node: AST.FunctionDefinition):
        ret_type = self.type_from_ast(node.return_type)
        params, _ = self._collect_parameters(node.parameters)

        func = FunctionSymbol(node.name, ret_type, params)
        self.symbol_table.declare_function(func)
        self.node_symbols[node] = func

    def _collect_parameters(self, param_nodes: List[AST.Parameter]) -> Tuple[List[VariableSymbol], set]:
        params = []
        param_names = set()
        for p in param_nodes:
            if p.name in param_names:
                raise SemanticError(f"Duplicate parameter name '{p.name}'.")
            param_names.add(p.name)
            p_type = self.type_from_ast(p.param_type)
            params.append(VariableSymbol(p.name, p_type))
        return params, param_names

    def resolve_inheritance(self):
        for name, cls in self.symbol_table.classes.items():
            if cls.parent_name:
                if cls.parent_name == name:
                    raise SemanticError(
                        f"Class '{name}' cannot inherit from itself.")
                if cls.parent_name not in self.symbol_table.classes:
                    raise SemanticError(
                        f"Base class '{cls.parent_name}' of '{name}' not found.")
                cls.parent = self.symbol_table.classes[cls.parent_name]

        for name, cls in self.symbol_table.classes.items():
            curr = cls
            chain = set()
            while curr:
                if curr.name in chain:
                    raise SemanticError(
                        f"Inheritance cycle detected involving '{curr.name}'.")
                chain.add(curr.name)
                curr = curr.parent

    # Combined analyzer for FunctionDefinition, MethodDefinition, ConstructorDefinition
    def analyze_function_body(self, node: Union[AST.FunctionDefinition, AST.MethodDefinition, AST.ConstructorDefinition]):
        func = self.node_symbols[node]
        self.current_function = func
        self.symbol_table.push_scope()

        for p in func.parameters:
            self.symbol_table.declare_variable(p.name, p.type)

        for stmt in node.body:
            self.visit_statement(stmt)

        self.symbol_table.pop_scope()
        self.current_function = None

    def analyze_class_body(self, node: AST.ClassDefinition):
        cls = self.symbol_table.classes[node.name]
        self.current_class = cls

        self._collect_members(node, cls)

        for member in node.members:
            if isinstance(member, (AST.MethodDefinition, AST.ConstructorDefinition)):
                self.analyze_function_body(member)

        self.current_class = None

    def _collect_members(self, node: AST.ClassDefinition, cls: ClassSymbol):
        for member in node.members:
            if isinstance(member, AST.VariableDeclaration):
                self._collect_field(member, cls)
            elif isinstance(member, AST.MethodDefinition):
                self._collect_method(member, cls)
            elif isinstance(member, AST.ConstructorDefinition):
                self._collect_constructor(member, cls)

    def _collect_field(self, member: AST.VariableDeclaration, cls: ClassSymbol):
        t = self.type_from_ast(member.var_type)
        if isinstance(t, ReferenceType):
            raise SemanticError("Fields cannot be references.")
        if member.name in cls.members:
            raise SemanticError(
                f"Duplicate member '{member.name}' in class '{cls.name}'.")
        cls.members[member.name] = VariableSymbol(member.name, t)

    def _collect_method(self, member: AST.MethodDefinition, cls: ClassSymbol):
        ret_type = self.type_from_ast(member.return_type)
        params, _ = self._collect_parameters(member.parameters)

        meth = FunctionSymbol(member.name, ret_type, params, is_method=True,
                              is_virtual=member.is_virtual, class_name=cls.name)

        if member.name not in cls.members:
            cls.members[member.name] = []
        elif not isinstance(cls.members[member.name], list):
            raise SemanticError(
                f"Method '{member.name}' conflicts with field.")

        method_list = cls.members[member.name]
        if isinstance(method_list, list):
            for m in method_list:
                if m.signature == meth.signature:
                    raise SemanticError(
                        f"Duplicate method '{member.name}' in class '{cls.name}'.")
            method_list.append(meth)

        self.node_symbols[member] = meth

    def _collect_constructor(self, member: AST.ConstructorDefinition, cls: ClassSymbol):
        if member.name != cls.name:
            raise SemanticError(
                f"Constructor name '{member.name}' must match class name '{cls.name}'.")
        params, _ = self._collect_parameters(member.parameters)

        ctor = FunctionSymbol(member.name, self.symbol_table.void_type,
                              params, is_method=True, class_name=cls.name)

        if "__ctor__" not in cls.members:
            cls.members["__ctor__"] = []

        ctor_list = cls.members["__ctor__"]
        if isinstance(ctor_list, list):
            for c in ctor_list:
                if c.signature == ctor.signature:
                    raise SemanticError(
                        f"Duplicate constructor for '{cls.name}'.")
            ctor_list.append(ctor)

        self.node_symbols[member] = ctor

    def visit_statement(self, stmt: AST.Statement):
        if isinstance(stmt, AST.VariableDeclaration):
            self._visit_var_decl(stmt)
        elif isinstance(stmt, AST.ReturnStatement):
            self._visit_return(stmt)
        elif isinstance(stmt, AST.IfStatement):
            self._visit_if(stmt)
        elif isinstance(stmt, AST.WhileStatement):
            self._visit_while(stmt)
        elif isinstance(stmt, AST.ExpressionStatement):
            self.visit_expression(stmt.expression)

    def _visit_var_decl(self, stmt: AST.VariableDeclaration):
        t = self.type_from_ast(stmt.var_type)
        if stmt.name in self.symbol_table.scopes[-1]:
            raise SemanticError(
                f"Redeclaration of '{stmt.name}' in current scope.")

        if isinstance(t, ReferenceType):
            self._check_reference_init(stmt, t)
        else:
            self._check_value_init(stmt, t)

        self.symbol_table.declare_variable(stmt.name, t)

    def _check_reference_init(self, stmt: AST.VariableDeclaration, t: ReferenceType):
        if not stmt.initializer:
            raise SemanticError(
                f"Reference '{stmt.name}' must be initialized.")

        init_type, is_lvalue = self.visit_expression(stmt.initializer)
        if not is_lvalue:
            raise SemanticError(
                f"Reference '{stmt.name}' must be initialized with an LValue.")

        if init_type != t.inner:
            is_sub = False
            if isinstance(t.inner, ClassSymbol) and isinstance(init_type, ClassSymbol):
                if self.is_subclass(init_type, t.inner):
                    is_sub = True
            if not is_sub:
                raise SemanticError(
                    f"Type mismatch: Expected {t.inner}, got {init_type}.")

    def _check_value_init(self, stmt: AST.VariableDeclaration, t: TypeSymbol):
        if stmt.initializer:
            init_type, _ = self.visit_expression(stmt.initializer)
            if init_type != t:
                is_compatible = False
                if isinstance(t, ClassSymbol) and isinstance(init_type, ClassSymbol):
                    if self.is_subclass(init_type, t):
                        is_compatible = True

                if not is_compatible:
                    raise SemanticError(
                        f"Type mismatch: cannot initialize {t} with {init_type}.")

    def _visit_return(self, stmt: AST.ReturnStatement):
        if not self.current_function:
            raise SemanticError("Return statement outside function.")

        expr_type = self.symbol_table.void_type
        if stmt.expression:
            expr_type, _ = self.visit_expression(stmt.expression)

        ret_type = self.current_function.return_type
        self._validate_return_type(ret_type, expr_type)

    def _validate_return_type(self, ret_type: TypeSymbol, expr_type: TypeSymbol):
        if ret_type == self.symbol_table.void_type:
            if expr_type != self.symbol_table.void_type:
                raise SemanticError("Void function cannot return a value.")
            return

        if expr_type == self.symbol_table.void_type:
            raise SemanticError(f"Expected return value of type {ret_type}.")

        if expr_type == ret_type:
            return

        if isinstance(ret_type, ClassSymbol) and isinstance(expr_type, ClassSymbol):
            if self.is_subclass(expr_type, ret_type):
                return

        raise SemanticError(
            f"Return type mismatch. Expected {ret_type}, got {expr_type}.")

    def _visit_if(self, stmt: AST.IfStatement):
        self._check_condition(stmt.condition)
        self._visit_block(stmt.then_stmt)
        if stmt.else_stmt:
            self._visit_block(stmt.else_stmt)

    def _visit_while(self, stmt: AST.WhileStatement):
        self._check_condition(stmt.condition)
        self._visit_block(stmt.body)

    def _check_condition(self, condition: AST.Expression):
        cond_type, _ = self.visit_expression(condition)
        if cond_type not in [self.symbol_table.bool_type, self.symbol_table.int_type, self.symbol_table.char_type, self.symbol_table.string_type]:
            raise SemanticError("Condition must be convertible to bool.")

    def _visit_block(self, stmts: List[AST.Statement]):
        self.symbol_table.push_scope()
        for s in stmts:
            self.visit_statement(s)
        self.symbol_table.pop_scope()

    def visit_expression(self, expr: AST.Expression) -> Tuple[TypeSymbol, bool]:
        if isinstance(expr, AST.IdentifierExpression):
            return self._visit_identifier(expr)
        elif isinstance(expr, AST.LiteralExpression):
            return self.symbol_table.resolve_type(expr.literal_type), False
        elif isinstance(expr, AST.AssignmentExpression):
            return self._visit_assignment(expr)
        elif isinstance(expr, AST.BinaryExpression):
            return self._visit_binary(expr)
        elif isinstance(expr, AST.UnaryExpression):
            return self._visit_unary(expr)
        elif isinstance(expr, AST.CallExpression):
            return self._visit_call(expr)
        elif isinstance(expr, AST.MethodCallExpression):
            return self._visit_method_call(expr)
        elif isinstance(expr, AST.MemberAccessExpression):
            return self._visit_member_access(expr)
        return self.symbol_table.void_type, False

    def _visit_identifier(self, expr: AST.IdentifierExpression) -> Tuple[TypeSymbol, bool]:
        sym = self.symbol_table.resolve_variable(expr.name)
        if sym:
            # Fix Pylance issue: Assign to variable for narrowing
            sym_type = sym.type
            if isinstance(sym_type, ReferenceType):
                return sym_type.inner, True
            return sym_type, True

        if self.current_class:
            member = self.lookup_member(self.current_class, expr.name)
            if member:
                if isinstance(member, VariableSymbol):
                    return member.type, True
                raise SemanticError(
                    f"Method '{expr.name}' cannot be used as a variable.")

        raise SemanticError(f"Undefined variable '{expr.name}'.")

    def _visit_assignment(self, expr: AST.AssignmentExpression) -> Tuple[TypeSymbol, bool]:
        target_type, is_lval = self.visit_expression(expr.target)
        if not is_lval:
            raise SemanticError("Assignment target must be an LValue.")

        val_type, _ = self.visit_expression(expr.value)

        if target_type != val_type:
            if isinstance(target_type, ClassSymbol) and isinstance(val_type, ClassSymbol):
                if not self.is_subclass(val_type, target_type):
                    raise SemanticError(
                        f"Cannot assign {val_type} to {target_type}.")
            else:
                raise SemanticError(
                    f"Assignment type mismatch: {target_type} = {val_type}.")
        return target_type, False

    def _visit_binary(self, expr: AST.BinaryExpression) -> Tuple[TypeSymbol, bool]:
        l_type, _ = self.visit_expression(expr.left)
        r_type, _ = self.visit_expression(expr.right)

        if expr.operator in ['+', '-', '*', '/', '%']:
            return self._check_arithmetic(l_type, r_type)
        if expr.operator in ['<', '<=', '>', '>=']:
            return self._check_comparison(l_type, r_type)
        if expr.operator in ['==', '!=']:
            return self._check_equality(l_type, r_type)
        if expr.operator in ['&&', '||']:
            return self._check_logic(l_type, r_type)
        return self.symbol_table.void_type, False

    def _check_arithmetic(self, l: TypeSymbol, r: TypeSymbol) -> Tuple[TypeSymbol, bool]:
        if l != self.symbol_table.int_type or r != self.symbol_table.int_type:
            raise SemanticError("Arithmetic operators require int.")
        return self.symbol_table.int_type, False

    def _check_comparison(self, l: TypeSymbol, r: TypeSymbol) -> Tuple[TypeSymbol, bool]:
        if l != r:
            raise SemanticError("Comparison operands must be same type.")
        if l not in [self.symbol_table.int_type, self.symbol_table.char_type]:
            raise SemanticError("Ordered comparison only for int and char.")
        return self.symbol_table.bool_type, False

    def _check_equality(self, l: TypeSymbol, r: TypeSymbol) -> Tuple[TypeSymbol, bool]:
        if l != r:
            raise SemanticError("Equality operands must be same type.")
        return self.symbol_table.bool_type, False

    def _check_logic(self, l: TypeSymbol, r: TypeSymbol) -> Tuple[TypeSymbol, bool]:
        if l != self.symbol_table.bool_type or r != self.symbol_table.bool_type:
            raise SemanticError("Logic operators require bool.")
        return self.symbol_table.bool_type, False

    def _visit_unary(self, expr: AST.UnaryExpression) -> Tuple[TypeSymbol, bool]:
        t, _ = self.visit_expression(expr.operand)
        if expr.operator == '!':
            if t != self.symbol_table.bool_type:
                raise SemanticError("! operator requires bool.")
            return self.symbol_table.bool_type, False
        if expr.operator in ['+', '-']:
            if t != self.symbol_table.int_type:
                raise SemanticError("Unary +/- requires int.")
            return self.symbol_table.int_type, False
        return self.symbol_table.void_type, False

    def _visit_call(self, expr: AST.CallExpression) -> Tuple[TypeSymbol, bool]:
        arg_infos = [(self.visit_expression(a)[0], self.visit_expression(a)[1])
                     for a in expr.arguments]

        # 1. Variables not callable
        if self.symbol_table.resolve_variable(expr.callee):
            raise SemanticError(
                f"'{expr.callee}' is a variable and cannot be called.")

        # 2. Constructor Call
        if expr.callee in self.symbol_table.classes:
            return self._resolve_constructor_call(expr.callee, arg_infos)

        # 3. Method Call (Implicit this)
        if self.current_class:
            res = self._check_method_call_implicit(expr.callee, arg_infos)
            if res:
                return res

        # 4. Global Function Call
        return self._resolve_global_call(expr.callee, arg_infos)

    def _check_method_call_implicit(self, callee: str, arg_infos: List[Tuple[TypeSymbol, bool]]) -> Optional[Tuple[TypeSymbol, bool]]:
        if not self.current_class:
            return None

        # Check method
        method_candidate = self.lookup_method_in_hierarchy(
            self.current_class, callee, arg_infos)
        if method_candidate:
            return method_candidate.return_type, False

        # Check field (error)
        if self.lookup_member(self.current_class, callee):
            raise SemanticError(f"'{callee}' is a field and cannot be called.")

        return None

    def _resolve_global_call(self, callee: str, arg_infos: List[Tuple[TypeSymbol, bool]]) -> Tuple[TypeSymbol, bool]:
        candidates = self.symbol_table.functions.get(callee, [])
        target = self._resolve_overload(candidates, arg_infos)
        if target:
            return target.return_type, False
        raise SemanticError(
            f"Function '{callee}' not found or parameters do not match.")

    def _resolve_constructor_call(self, class_name: str, arg_infos: List[Tuple[TypeSymbol, bool]]) -> Tuple[TypeSymbol, bool]:
        cls = self.symbol_table.classes[class_name]
        ctor_candidates = cls.members.get("__ctor__", [])

        # Explicit Constructors
        if isinstance(ctor_candidates, list) and ctor_candidates:
            target = self._resolve_overload(ctor_candidates, arg_infos)
            if target:
                return cls, False

        # Implicit Default Constructor (if no explicit constructors exist)
        if not ctor_candidates and not arg_infos:
            return cls, False

        # Implicit Copy Constructor
        if len(arg_infos) == 1:
            arg_type, _ = arg_infos[0]
            if isinstance(arg_type, ClassSymbol) and self.is_subclass(arg_type, cls):
                return cls, False

        raise SemanticError(f"No matching constructor for '{cls.name}'.")

    def _resolve_overload(self, candidates: List[FunctionSymbol], arg_infos: List[Tuple[TypeSymbol, bool]]) -> Optional[FunctionSymbol]:
        target = None
        for func in candidates:
            if len(func.parameters) == len(arg_infos):
                if self._check_parameters_match(func.parameters, arg_infos):
                    if target:
                        raise SemanticError("Ambiguous call.")
                    target = func
        return target

    def _check_parameters_match(self, parameters: List[VariableSymbol], arg_infos: List[Tuple[TypeSymbol, bool]]) -> bool:
        for i, p in enumerate(parameters):
            arg_type, is_lval = arg_infos[i]
            if p.type == arg_type:
                continue
            elif isinstance(p.type, ReferenceType) and p.type.inner == arg_type:
                if not is_lval:
                    return False
            else:
                return False
        return True

    def _visit_method_call(self, expr: AST.MethodCallExpression) -> Tuple[TypeSymbol, bool]:
        obj_type, _ = self.visit_expression(expr.object)

        target_class = self._resolve_target_class(obj_type)

        arg_infos = [(self.visit_expression(a)[0], self.visit_expression(a)[1])
                     for a in expr.arguments]

        method = self.lookup_method_in_hierarchy(
            target_class, expr.method, arg_infos)
        if not method:
            raise SemanticError(
                f"Method '{expr.method}' not found in class '{target_class.name}'.")

        return method.return_type, False

    def _visit_member_access(self, expr: AST.MemberAccessExpression) -> Tuple[TypeSymbol, bool]:
        obj_type, _ = self.visit_expression(expr.object)
        target_class = self._resolve_target_class(obj_type)

        member = self.lookup_member(target_class, expr.member)
        if not member:
            raise SemanticError(
                f"Member '{expr.member}' not found in class '{target_class.name}'.")

        if isinstance(member, VariableSymbol):
            return member.type, True
        else:
            raise SemanticError("Cannot access method as field.")

    def _resolve_target_class(self, obj_type: TypeSymbol) -> ClassSymbol:
        if isinstance(obj_type, ClassSymbol):
            return obj_type
        if isinstance(obj_type, ReferenceType) and isinstance(obj_type.inner, ClassSymbol):
            return obj_type.inner

        raise SemanticError("Member access/call on non-class type.")

    def lookup_member(self, cls: ClassSymbol, name: str):
        if name in cls.members:
            return cls.members[name]
        if cls.parent:
            return self.lookup_member(cls.parent, name)
        return None

    def lookup_method_in_hierarchy(self, cls: ClassSymbol, name: str, arg_infos: List[Tuple[TypeSymbol, bool]]):
        if name in cls.members:
            members = cls.members[name]
            if isinstance(members, list):
                target = self._resolve_overload(members, arg_infos)
                if target:
                    return target

        if cls.parent:
            return self.lookup_method_in_hierarchy(cls.parent, name, arg_infos)
        return None

    def is_subclass(self, child: TypeSymbol, parent: TypeSymbol):
        if child == parent:
            return True
        if isinstance(child, ClassSymbol) and isinstance(parent, ClassSymbol):
            curr = child.parent
            while curr:
                if curr == parent:
                    return True
                curr = curr.parent
        return False


def analyze_file(path):
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
    ast_builder = ASTBuilder()
    ast = ast_builder.visitProgram(tree)

    analyzer = SemanticAnalyzer()
    analyzer.visit_program(ast)

# Test runner
def test_single_file(f: Path, expect_success: bool) -> tuple[str, str]:
    status = "FAIL"
    error_msg = ""
    try:
        analyze_file(str(f))
        if expect_success:
            status = "PASS"
        else:
            status = "FAIL (Unexpected success)"
    except SemanticError as e:
        error_msg = str(e)
        if not expect_success:
            status = "PASS"
        else:
            status = "FAIL"
    except Exception as e:
        status = "CRASH"
        error_msg = str(e)
    return status, error_msg


def run_suite(path: Path, expect_success=True):
    print(f"\nTesting {path.name}:")
    valid = 0
    files = sorted(path.glob("*.cpp"))
    total = len(files)
    for f in files:
        status, error_msg = test_single_file(f, expect_success)
        print(f"  [{status}] {f.name}")
        if error_msg:
            print(f"    {error_msg}")

        if status == "PASS":
            valid += 1
    return valid, total


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            analyze_file(sys.argv[1])
            print("Analysis successful.")
            sys.exit(0)
        except SemanticError as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Internal Error: {e}")
            sys.exit(1)
    else:
        base = Path(__file__).parent / "tests"
        if not base.exists():
            print(f"Tests folder not found at {base}")
            sys.exit(1)

        p_v, p_t = run_suite(base / "positive", expect_success=True)
        n_v, n_t = run_suite(base / "negative", expect_success=False)
        print(f"\nSummary: Positive {p_v}/{p_t}, Negative {n_v}/{n_t}")
