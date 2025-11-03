# Generated from PrettyLang.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,22,100,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,1,0,4,0,18,8,0,11,0,12,0,19,1,0,1,0,1,1,1,1,1,1,1,1,1,
        1,1,1,3,1,30,8,1,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,4,3,42,
        8,3,11,3,12,3,43,1,3,1,3,1,3,1,3,4,3,50,8,3,11,3,12,3,51,3,3,54,
        8,3,1,3,1,3,3,3,58,8,3,1,4,1,4,1,4,1,4,1,4,4,4,65,8,4,11,4,12,4,
        66,1,4,1,4,3,4,71,8,4,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,3,6,82,
        8,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,5,6,93,8,6,10,6,12,6,96,
        9,6,1,7,1,7,1,7,0,1,12,8,0,2,4,6,8,10,12,14,0,4,1,0,17,18,1,0,15,
        16,1,0,19,22,1,0,8,9,106,0,17,1,0,0,0,2,29,1,0,0,0,4,31,1,0,0,0,
        6,36,1,0,0,0,8,59,1,0,0,0,10,72,1,0,0,0,12,81,1,0,0,0,14,97,1,0,
        0,0,16,18,3,2,1,0,17,16,1,0,0,0,18,19,1,0,0,0,19,17,1,0,0,0,19,20,
        1,0,0,0,20,21,1,0,0,0,21,22,5,0,0,1,22,1,1,0,0,0,23,30,3,4,2,0,24,
        30,3,6,3,0,25,30,3,8,4,0,26,27,3,12,6,0,27,28,5,13,0,0,28,30,1,0,
        0,0,29,23,1,0,0,0,29,24,1,0,0,0,29,25,1,0,0,0,29,26,1,0,0,0,30,3,
        1,0,0,0,31,32,5,10,0,0,32,33,5,14,0,0,33,34,3,12,6,0,34,35,5,13,
        0,0,35,5,1,0,0,0,36,37,5,3,0,0,37,38,3,10,5,0,38,39,5,6,0,0,39,41,
        5,13,0,0,40,42,3,2,1,0,41,40,1,0,0,0,42,43,1,0,0,0,43,41,1,0,0,0,
        43,44,1,0,0,0,44,53,1,0,0,0,45,46,5,4,0,0,46,47,5,6,0,0,47,49,5,
        13,0,0,48,50,3,2,1,0,49,48,1,0,0,0,50,51,1,0,0,0,51,49,1,0,0,0,51,
        52,1,0,0,0,52,54,1,0,0,0,53,45,1,0,0,0,53,54,1,0,0,0,54,55,1,0,0,
        0,55,57,5,7,0,0,56,58,5,13,0,0,57,56,1,0,0,0,57,58,1,0,0,0,58,7,
        1,0,0,0,59,60,5,5,0,0,60,61,3,10,5,0,61,62,5,6,0,0,62,64,5,13,0,
        0,63,65,3,2,1,0,64,63,1,0,0,0,65,66,1,0,0,0,66,64,1,0,0,0,66,67,
        1,0,0,0,67,68,1,0,0,0,68,70,5,7,0,0,69,71,5,13,0,0,70,69,1,0,0,0,
        70,71,1,0,0,0,71,9,1,0,0,0,72,73,3,12,6,0,73,11,1,0,0,0,74,75,6,
        6,-1,0,75,76,5,1,0,0,76,77,3,12,6,0,77,78,5,2,0,0,78,82,1,0,0,0,
        79,82,3,14,7,0,80,82,5,10,0,0,81,74,1,0,0,0,81,79,1,0,0,0,81,80,
        1,0,0,0,82,94,1,0,0,0,83,84,10,6,0,0,84,85,7,0,0,0,85,93,3,12,6,
        7,86,87,10,5,0,0,87,88,7,1,0,0,88,93,3,12,6,6,89,90,10,4,0,0,90,
        91,7,2,0,0,91,93,3,12,6,5,92,83,1,0,0,0,92,86,1,0,0,0,92,89,1,0,
        0,0,93,96,1,0,0,0,94,92,1,0,0,0,94,95,1,0,0,0,95,13,1,0,0,0,96,94,
        1,0,0,0,97,98,7,3,0,0,98,15,1,0,0,0,11,19,29,43,51,53,57,66,70,81,
        92,94
    ]

class PrettyLangParser ( Parser ):

    grammarFileName = "PrettyLang.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'if'", "'else'", "'while'", 
                     "'do'", "'end'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "':='", "'+'", 
                     "'-'", "'*'", "'/'", "'=='", "'!='", "'<'", "'>'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "IF", "ELSE", 
                      "WHILE", "DO", "END", "INT", "STRING", "IDENT", "COMMENT", 
                      "WS", "NEWLINE", "ASSIGN", "PLUS", "MINUS", "STAR", 
                      "SLASH", "EQ", "NEQ", "LT", "GT" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_assignment = 2
    RULE_ifStatement = 3
    RULE_whileStatement = 4
    RULE_condition = 5
    RULE_expression = 6
    RULE_literal = 7

    ruleNames =  [ "program", "statement", "assignment", "ifStatement", 
                   "whileStatement", "condition", "expression", "literal" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    IF=3
    ELSE=4
    WHILE=5
    DO=6
    END=7
    INT=8
    STRING=9
    IDENT=10
    COMMENT=11
    WS=12
    NEWLINE=13
    ASSIGN=14
    PLUS=15
    MINUS=16
    STAR=17
    SLASH=18
    EQ=19
    NEQ=20
    LT=21
    GT=22

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(PrettyLangParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PrettyLangParser.StatementContext)
            else:
                return self.getTypedRuleContext(PrettyLangParser.StatementContext,i)


        def getRuleIndex(self):
            return PrettyLangParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = PrettyLangParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 16
                self.statement()
                self.state = 19 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 1834) != 0)):
                    break

            self.state = 21
            self.match(PrettyLangParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self):
            return self.getTypedRuleContext(PrettyLangParser.AssignmentContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(PrettyLangParser.IfStatementContext,0)


        def whileStatement(self):
            return self.getTypedRuleContext(PrettyLangParser.WhileStatementContext,0)


        def expression(self):
            return self.getTypedRuleContext(PrettyLangParser.ExpressionContext,0)


        def NEWLINE(self):
            return self.getToken(PrettyLangParser.NEWLINE, 0)

        def getRuleIndex(self):
            return PrettyLangParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)




    def statement(self):

        localctx = PrettyLangParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 29
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 23
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 24
                self.ifStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 25
                self.whileStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 26
                self.expression(0)
                self.state = 27
                self.match(PrettyLangParser.NEWLINE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(PrettyLangParser.IDENT, 0)

        def ASSIGN(self):
            return self.getToken(PrettyLangParser.ASSIGN, 0)

        def expression(self):
            return self.getTypedRuleContext(PrettyLangParser.ExpressionContext,0)


        def NEWLINE(self):
            return self.getToken(PrettyLangParser.NEWLINE, 0)

        def getRuleIndex(self):
            return PrettyLangParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)




    def assignment(self):

        localctx = PrettyLangParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self.match(PrettyLangParser.IDENT)
            self.state = 32
            self.match(PrettyLangParser.ASSIGN)
            self.state = 33
            self.expression(0)
            self.state = 34
            self.match(PrettyLangParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(PrettyLangParser.IF, 0)

        def condition(self):
            return self.getTypedRuleContext(PrettyLangParser.ConditionContext,0)


        def DO(self, i:int=None):
            if i is None:
                return self.getTokens(PrettyLangParser.DO)
            else:
                return self.getToken(PrettyLangParser.DO, i)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(PrettyLangParser.NEWLINE)
            else:
                return self.getToken(PrettyLangParser.NEWLINE, i)

        def END(self):
            return self.getToken(PrettyLangParser.END, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PrettyLangParser.StatementContext)
            else:
                return self.getTypedRuleContext(PrettyLangParser.StatementContext,i)


        def ELSE(self):
            return self.getToken(PrettyLangParser.ELSE, 0)

        def getRuleIndex(self):
            return PrettyLangParser.RULE_ifStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)




    def ifStatement(self):

        localctx = PrettyLangParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_ifStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(PrettyLangParser.IF)
            self.state = 37
            self.condition()
            self.state = 38
            self.match(PrettyLangParser.DO)
            self.state = 39
            self.match(PrettyLangParser.NEWLINE)
            self.state = 41 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 40
                self.statement()
                self.state = 43 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 1834) != 0)):
                    break

            self.state = 53
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 45
                self.match(PrettyLangParser.ELSE)
                self.state = 46
                self.match(PrettyLangParser.DO)
                self.state = 47
                self.match(PrettyLangParser.NEWLINE)
                self.state = 49 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 48
                    self.statement()
                    self.state = 51 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 1834) != 0)):
                        break



            self.state = 55
            self.match(PrettyLangParser.END)
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 56
                self.match(PrettyLangParser.NEWLINE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(PrettyLangParser.WHILE, 0)

        def condition(self):
            return self.getTypedRuleContext(PrettyLangParser.ConditionContext,0)


        def DO(self):
            return self.getToken(PrettyLangParser.DO, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(PrettyLangParser.NEWLINE)
            else:
                return self.getToken(PrettyLangParser.NEWLINE, i)

        def END(self):
            return self.getToken(PrettyLangParser.END, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PrettyLangParser.StatementContext)
            else:
                return self.getTypedRuleContext(PrettyLangParser.StatementContext,i)


        def getRuleIndex(self):
            return PrettyLangParser.RULE_whileStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStatement" ):
                listener.enterWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStatement" ):
                listener.exitWhileStatement(self)




    def whileStatement(self):

        localctx = PrettyLangParser.WhileStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_whileStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(PrettyLangParser.WHILE)
            self.state = 60
            self.condition()
            self.state = 61
            self.match(PrettyLangParser.DO)
            self.state = 62
            self.match(PrettyLangParser.NEWLINE)
            self.state = 64 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 63
                self.statement()
                self.state = 66 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 1834) != 0)):
                    break

            self.state = 68
            self.match(PrettyLangParser.END)
            self.state = 70
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 69
                self.match(PrettyLangParser.NEWLINE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(PrettyLangParser.ExpressionContext,0)


        def getRuleIndex(self):
            return PrettyLangParser.RULE_condition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondition" ):
                listener.enterCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondition" ):
                listener.exitCondition(self)




    def condition(self):

        localctx = PrettyLangParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PrettyLangParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class MulDivExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PrettyLangParser.ExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PrettyLangParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PrettyLangParser.ExpressionContext,i)

        def STAR(self):
            return self.getToken(PrettyLangParser.STAR, 0)
        def SLASH(self):
            return self.getToken(PrettyLangParser.SLASH, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMulDivExpr" ):
                listener.enterMulDivExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMulDivExpr" ):
                listener.exitMulDivExpr(self)


    class CompareExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PrettyLangParser.ExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PrettyLangParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PrettyLangParser.ExpressionContext,i)

        def LT(self):
            return self.getToken(PrettyLangParser.LT, 0)
        def GT(self):
            return self.getToken(PrettyLangParser.GT, 0)
        def EQ(self):
            return self.getToken(PrettyLangParser.EQ, 0)
        def NEQ(self):
            return self.getToken(PrettyLangParser.NEQ, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompareExpr" ):
                listener.enterCompareExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompareExpr" ):
                listener.exitCompareExpr(self)


    class LiteralExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PrettyLangParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(PrettyLangParser.LiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteralExpr" ):
                listener.enterLiteralExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteralExpr" ):
                listener.exitLiteralExpr(self)


    class VarExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PrettyLangParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENT(self):
            return self.getToken(PrettyLangParser.IDENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarExpr" ):
                listener.enterVarExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarExpr" ):
                listener.exitVarExpr(self)


    class ParenExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PrettyLangParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(PrettyLangParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)


    class AddSubExprContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PrettyLangParser.ExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PrettyLangParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(PrettyLangParser.ExpressionContext,i)

        def PLUS(self):
            return self.getToken(PrettyLangParser.PLUS, 0)
        def MINUS(self):
            return self.getToken(PrettyLangParser.MINUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddSubExpr" ):
                listener.enterAddSubExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddSubExpr" ):
                listener.exitAddSubExpr(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = PrettyLangParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 12
        self.enterRecursionRule(localctx, 12, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                localctx = PrettyLangParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 75
                self.match(PrettyLangParser.T__0)
                self.state = 76
                self.expression(0)
                self.state = 77
                self.match(PrettyLangParser.T__1)
                pass
            elif token in [8, 9]:
                localctx = PrettyLangParser.LiteralExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 79
                self.literal()
                pass
            elif token in [10]:
                localctx = PrettyLangParser.VarExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 80
                self.match(PrettyLangParser.IDENT)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 94
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 92
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
                    if la_ == 1:
                        localctx = PrettyLangParser.MulDivExprContext(self, PrettyLangParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 83
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 84
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==17 or _la==18):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 85
                        self.expression(7)
                        pass

                    elif la_ == 2:
                        localctx = PrettyLangParser.AddSubExprContext(self, PrettyLangParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 86
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 87
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==15 or _la==16):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 88
                        self.expression(6)
                        pass

                    elif la_ == 3:
                        localctx = PrettyLangParser.CompareExprContext(self, PrettyLangParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 89
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 90
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 7864320) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 91
                        self.expression(5)
                        pass

             
                self.state = 96
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(PrettyLangParser.INT, 0)

        def STRING(self):
            return self.getToken(PrettyLangParser.STRING, 0)

        def getRuleIndex(self):
            return PrettyLangParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)




    def literal(self):

        localctx = PrettyLangParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_literal)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            _la = self._input.LA(1)
            if not(_la==8 or _la==9):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[6] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 4)
         




