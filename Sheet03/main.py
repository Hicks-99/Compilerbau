from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from PrettyLangLexer import PrettyLangLexer
from PrettyLangParser import PrettyLangParser

file_name = 'Sheet03/test.txt'
with open(file_name, 'r') as file:
    input_text =  file.read()
lexer = PrettyLangLexer(InputStream(input_text))
stream = CommonTokenStream(lexer)
parser = PrettyLangParser(stream)

mytree = parser.program()

#print(mytree.toStringTree(recog=parser))

def pretty_printer(parsetree: PrettyLangParser.ProgramContext, indent: int = 0) -> str:
    output = ""
    if type(parsetree) == TerminalNodeImpl: 
        if parsetree.getText() != '<EOF>':
            output += more_formatting(parsetree, indent)

        return output
    
    for child in parsetree.getChildren():
        if type(child) == PrettyLangParser.StatementContext:
            output += indent*'    '
        if type(child) == PrettyLangParser.IfStatementContext or type(child) == PrettyLangParser.WhileStatementContext:
            indent += 1
        output += pretty_printer(child, indent) # type: ignore

    return output

def more_formatting(node: TerminalNodeImpl, indent:int) -> str:
    parent = node.parentCtx
    #print(type(parent))
    index = parent.children.index(node)
    match type(parent):
        case PrettyLangParser.CompareExprContext | PrettyLangParser.MulDivExprContext | PrettyLangParser.AddSubExprContext : 
            return " " + node.getText() + " "
        case PrettyLangParser.AssignmentContext:
            if index == 1: 
                return " " + node.getText() + " "
            return node.getText()
        
        case PrettyLangParser.IfStatementContext | PrettyLangParser.WhileStatementContext:
            if len(parent.children) > index+1 and type(parent.children[index+1]) == PrettyLangParser.ConditionContext: 
                return  node.getText()+ " "
            
            if index >= 0 and type(parent.children[index-1]) == PrettyLangParser.ConditionContext: 
                return " " + node.getText()
            
            if index >= 0 and type(parent.children[index-1]) == PrettyLangParser.StatementContext:
                return (indent-1)*'    ' + node.getText() + " "

            return node.getText()
    
        case _: 
            return node.getText()

    return ""


print(pretty_printer(mytree))