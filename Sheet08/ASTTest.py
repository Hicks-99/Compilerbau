from gen.ASTBuilder import ASTBuilder
from gen.ASTPrinter import ASTPrinter
from gen.MiniCParser import MiniCParser
from gen.MiniCLexer import MiniCLexer
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from pathlib import Path


class MyErrorListener(ErrorListener):
    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Line {line}:{column} - {msg}")


# Parse code - use Path to construct the correct path
script_dir = Path(__file__).parent
test_file = script_dir / "tests" / "positive" / "GOLD01_basics.cpp"

print(f"Reading file: {test_file}")
print(f"File exists: {test_file.exists()}")

# Create lexer and parser
lexer = MiniCLexer(FileStream(str(test_file), encoding="utf-8"))
token_stream = CommonTokenStream(lexer)
parser = MiniCParser(token_stream)

# Add error listener
error_listener = MyErrorListener()
parser.removeErrorListeners()
parser.addErrorListener(error_listener)

# Parse
parse_tree = parser.program()

# Check for parsing errors
if error_listener.errors:
    print("Parsing errors:")
    for error in error_listener.errors:
        print(f"  {error}")
else:
    print("Parsing successful!")

# Build AST
print("\nBuilding AST...")
builder = ASTBuilder()
ast = builder.visitProgram(parse_tree)

# Check result
if ast is None:
    print("ERROR: AST is None!")
    print(f"Parse tree type: {type(parse_tree)}")
    print(f"Parse tree: {parse_tree.toStringTree(recog=parser)[:200]}...")
else:
    print(f"✓ Program has {len(ast.declarations)} declarations")
    for i, decl in enumerate(ast.declarations):
        print(f"  Declaration {i+1}: {type(decl).__name__}")
    
    # Pretty print the AST
    print("\n" + "="*60)
    print("AST Structure:")
    print("="*60)
    printer = ASTPrinter()
    printer.print_ast(ast)