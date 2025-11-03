from antlr4 import *
from PrettyLangLexer import PrettyLangLexer
from PrettyLangParser import PrettyLangParser

file_name = input("Enter the file name: ")
with open(file_name, 'r') as file:
    input_text =  file.read()
lexer = PrettyLangLexer(InputStream(input_text))
stream = CommonTokenStream(lexer)
parser = PrettyLangParser(stream)

tree = parser.program()

print(tree.toStringTree(recog=parser))
