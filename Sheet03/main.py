from antlr4 import InputStream, CommonTokenStream
from PrettyLangLexer import PrettyLangLexer
from PrettyLangParser import PrettyLangParser


input_text = input("> ")
lexer = PrettyLangLexer(InputStream(input_text))
stream = CommonTokenStream(lexer)
parser = PrettyLangParser(stream)

tree = parser.program()

print(tree.toStringTree(recog=parser))
