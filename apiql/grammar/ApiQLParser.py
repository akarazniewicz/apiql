# Generated from C:/Users/karaznie/apiql/apiql/grammar\ApiQL.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3(")
        buf.write("m\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16\t")
        buf.write("\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\3\2\3\2\3")
        buf.write("\2\7\2(\n\2\f\2\16\2+\13\2\3\3\3\3\3\3\5\3\60\n\3\3\4")
        buf.write("\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\6\3\6\5\6>\n\6")
        buf.write("\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\t\3\t\3\n\3\n\3\13")
        buf.write("\3\13\3\f\3\f\3\f\3\f\7\fR\n\f\f\f\16\fU\13\f\3\f\3\f")
        buf.write("\3\r\3\r\3\r\3\r\3\r\5\r^\n\r\3\16\3\16\3\17\3\17\3\20")
        buf.write("\3\20\3\21\3\21\3\21\3\21\3\21\3\22\3\22\3\22\2\2\23\2")
        buf.write("\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \"\2\5\3\2\b\32")
        buf.write("\3\2\33\34\3\2\36\37\2d\2$\3\2\2\2\4/\3\2\2\2\6\61\3\2")
        buf.write("\2\2\b\66\3\2\2\2\n=\3\2\2\2\f?\3\2\2\2\16C\3\2\2\2\20")
        buf.write("G\3\2\2\2\22I\3\2\2\2\24K\3\2\2\2\26M\3\2\2\2\30]\3\2")
        buf.write("\2\2\32_\3\2\2\2\34a\3\2\2\2\36c\3\2\2\2 e\3\2\2\2\"j")
        buf.write("\3\2\2\2$)\5\4\3\2%&\7\3\2\2&(\5\4\3\2\'%\3\2\2\2(+\3")
        buf.write("\2\2\2)\'\3\2\2\2)*\3\2\2\2*\3\3\2\2\2+)\3\2\2\2,\60\5")
        buf.write("\6\4\2-\60\5\b\5\2.\60\5\n\6\2/,\3\2\2\2/-\3\2\2\2/.\3")
        buf.write("\2\2\2\60\5\3\2\2\2\61\62\7\4\2\2\62\63\7\5\2\2\63\64")
        buf.write("\5\2\2\2\64\65\7\6\2\2\65\7\3\2\2\2\66\67\7\7\2\2\678")
        buf.write("\7\5\2\289\5\2\2\29:\7\6\2\2:\t\3\2\2\2;>\5\f\7\2<>\5")
        buf.write("\16\b\2=;\3\2\2\2=<\3\2\2\2>\13\3\2\2\2?@\5\20\t\2@A\5")
        buf.write("\22\n\2AB\5\30\r\2B\r\3\2\2\2CD\5\20\t\2DE\5\24\13\2E")
        buf.write("F\5\26\f\2F\17\3\2\2\2GH\7$\2\2H\21\3\2\2\2IJ\t\2\2\2")
        buf.write("J\23\3\2\2\2KL\t\3\2\2L\25\3\2\2\2MN\7\5\2\2NS\5\30\r")
        buf.write("\2OP\7\35\2\2PR\5\30\r\2QO\3\2\2\2RU\3\2\2\2SQ\3\2\2\2")
        buf.write("ST\3\2\2\2TV\3\2\2\2US\3\2\2\2VW\7\6\2\2W\27\3\2\2\2X")
        buf.write("^\5\36\20\2Y^\5\32\16\2Z^\5\34\17\2[^\5 \21\2\\^\5\"\22")
        buf.write("\2]X\3\2\2\2]Y\3\2\2\2]Z\3\2\2\2][\3\2\2\2]\\\3\2\2\2")
        buf.write("^\31\3\2\2\2_`\t\4\2\2`\33\3\2\2\2ab\7 \2\2b\35\3\2\2")
        buf.write("\2cd\7#\2\2d\37\3\2\2\2ef\7!\2\2fg\7\5\2\2gh\5\"\22\2")
        buf.write("hi\7\6\2\2i!\3\2\2\2jk\7\"\2\2k#\3\2\2\2\7)/=S]")
        return buf.getvalue()


class ApiQLParser ( Parser ):

    grammarFileName = "ApiQL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'and'", "'('", "')'", "'or'", 
                     "'=='", "'!='", "'>'", "'>='", "'<'", "'<='", "'like'", 
                     "'ilike'", "'notlike'", "'notilike'", "'startswith'", 
                     "'istartswith'", "'endswith'", "'iendswith'", "'contains'", 
                     "'notcontains'", "'icontains'", "'inotcontains'", "'match'", 
                     "'in'", "'notin'", "','", "'true'", "'false'", "'null'", 
                     "'datetime'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "STRING", "NUMBER", "KEYWORD", "ESCAPED_STRING", "FLOAT", 
                      "INT", "WS" ]

    RULE_criteria = 0
    RULE_criterion = 1
    RULE_conjunction = 2
    RULE_disjunction = 3
    RULE_predicate = 4
    RULE_basic_predicate = 5
    RULE_compound_predicate = 6
    RULE_keyword = 7
    RULE_basic_operator = 8
    RULE_compound_operator = 9
    RULE_values = 10
    RULE_value = 11
    RULE_boolean = 12
    RULE_nil = 13
    RULE_number = 14
    RULE_datetime = 15
    RULE_string = 16

    ruleNames =  [ "criteria", "criterion", "conjunction", "disjunction", 
                   "predicate", "basic_predicate", "compound_predicate", 
                   "keyword", "basic_operator", "compound_operator", "values", 
                   "value", "boolean", "nil", "number", "datetime", "string" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    STRING=32
    NUMBER=33
    KEYWORD=34
    ESCAPED_STRING=35
    FLOAT=36
    INT=37
    WS=38

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class CriteriaContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def criterion(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ApiQLParser.CriterionContext)
            else:
                return self.getTypedRuleContext(ApiQLParser.CriterionContext,i)


        def getRuleIndex(self):
            return ApiQLParser.RULE_criteria

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCriteria" ):
                return visitor.visitCriteria(self)
            else:
                return visitor.visitChildren(self)




    def criteria(self):

        localctx = ApiQLParser.CriteriaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_criteria)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            self.criterion()
            self.state = 39
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ApiQLParser.T__0:
                self.state = 35
                self.match(ApiQLParser.T__0)
                self.state = 36
                self.criterion()
                self.state = 41
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CriterionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def conjunction(self):
            return self.getTypedRuleContext(ApiQLParser.ConjunctionContext,0)


        def disjunction(self):
            return self.getTypedRuleContext(ApiQLParser.DisjunctionContext,0)


        def predicate(self):
            return self.getTypedRuleContext(ApiQLParser.PredicateContext,0)


        def getRuleIndex(self):
            return ApiQLParser.RULE_criterion

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCriterion" ):
                return visitor.visitCriterion(self)
            else:
                return visitor.visitChildren(self)




    def criterion(self):

        localctx = ApiQLParser.CriterionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_criterion)
        try:
            self.state = 45
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ApiQLParser.T__1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 42
                self.conjunction()
                pass
            elif token in [ApiQLParser.T__4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 43
                self.disjunction()
                pass
            elif token in [ApiQLParser.KEYWORD]:
                self.enterOuterAlt(localctx, 3)
                self.state = 44
                self.predicate()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConjunctionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def criteria(self):
            return self.getTypedRuleContext(ApiQLParser.CriteriaContext,0)


        def getRuleIndex(self):
            return ApiQLParser.RULE_conjunction

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConjunction" ):
                return visitor.visitConjunction(self)
            else:
                return visitor.visitChildren(self)




    def conjunction(self):

        localctx = ApiQLParser.ConjunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_conjunction)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self.match(ApiQLParser.T__1)
            self.state = 48
            self.match(ApiQLParser.T__2)
            self.state = 49
            self.criteria()
            self.state = 50
            self.match(ApiQLParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DisjunctionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def criteria(self):
            return self.getTypedRuleContext(ApiQLParser.CriteriaContext,0)


        def getRuleIndex(self):
            return ApiQLParser.RULE_disjunction

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDisjunction" ):
                return visitor.visitDisjunction(self)
            else:
                return visitor.visitChildren(self)




    def disjunction(self):

        localctx = ApiQLParser.DisjunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_disjunction)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.match(ApiQLParser.T__4)
            self.state = 53
            self.match(ApiQLParser.T__2)
            self.state = 54
            self.criteria()
            self.state = 55
            self.match(ApiQLParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PredicateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def basic_predicate(self):
            return self.getTypedRuleContext(ApiQLParser.Basic_predicateContext,0)


        def compound_predicate(self):
            return self.getTypedRuleContext(ApiQLParser.Compound_predicateContext,0)


        def getRuleIndex(self):
            return ApiQLParser.RULE_predicate

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPredicate" ):
                return visitor.visitPredicate(self)
            else:
                return visitor.visitChildren(self)




    def predicate(self):

        localctx = ApiQLParser.PredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_predicate)
        try:
            self.state = 59
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.basic_predicate()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 58
                self.compound_predicate()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Basic_predicateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def keyword(self):
            return self.getTypedRuleContext(ApiQLParser.KeywordContext,0)


        def basic_operator(self):
            return self.getTypedRuleContext(ApiQLParser.Basic_operatorContext,0)


        def value(self):
            return self.getTypedRuleContext(ApiQLParser.ValueContext,0)


        def getRuleIndex(self):
            return ApiQLParser.RULE_basic_predicate

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBasic_predicate" ):
                return visitor.visitBasic_predicate(self)
            else:
                return visitor.visitChildren(self)




    def basic_predicate(self):

        localctx = ApiQLParser.Basic_predicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_basic_predicate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.keyword()
            self.state = 62
            self.basic_operator()
            self.state = 63
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Compound_predicateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def keyword(self):
            return self.getTypedRuleContext(ApiQLParser.KeywordContext,0)


        def compound_operator(self):
            return self.getTypedRuleContext(ApiQLParser.Compound_operatorContext,0)


        def values(self):
            return self.getTypedRuleContext(ApiQLParser.ValuesContext,0)


        def getRuleIndex(self):
            return ApiQLParser.RULE_compound_predicate

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompound_predicate" ):
                return visitor.visitCompound_predicate(self)
            else:
                return visitor.visitChildren(self)




    def compound_predicate(self):

        localctx = ApiQLParser.Compound_predicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_compound_predicate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self.keyword()
            self.state = 66
            self.compound_operator()
            self.state = 67
            self.values()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeywordContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def KEYWORD(self):
            return self.getToken(ApiQLParser.KEYWORD, 0)

        def getRuleIndex(self):
            return ApiQLParser.RULE_keyword

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKeyword" ):
                return visitor.visitKeyword(self)
            else:
                return visitor.visitChildren(self)




    def keyword(self):

        localctx = ApiQLParser.KeywordContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_keyword)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(ApiQLParser.KEYWORD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Basic_operatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ApiQLParser.RULE_basic_operator

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBasic_operator" ):
                return visitor.visitBasic_operator(self)
            else:
                return visitor.visitChildren(self)




    def basic_operator(self):

        localctx = ApiQLParser.Basic_operatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_basic_operator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << ApiQLParser.T__5) | (1 << ApiQLParser.T__6) | (1 << ApiQLParser.T__7) | (1 << ApiQLParser.T__8) | (1 << ApiQLParser.T__9) | (1 << ApiQLParser.T__10) | (1 << ApiQLParser.T__11) | (1 << ApiQLParser.T__12) | (1 << ApiQLParser.T__13) | (1 << ApiQLParser.T__14) | (1 << ApiQLParser.T__15) | (1 << ApiQLParser.T__16) | (1 << ApiQLParser.T__17) | (1 << ApiQLParser.T__18) | (1 << ApiQLParser.T__19) | (1 << ApiQLParser.T__20) | (1 << ApiQLParser.T__21) | (1 << ApiQLParser.T__22) | (1 << ApiQLParser.T__23))) != 0)):
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


    class Compound_operatorContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ApiQLParser.RULE_compound_operator

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompound_operator" ):
                return visitor.visitCompound_operator(self)
            else:
                return visitor.visitChildren(self)




    def compound_operator(self):

        localctx = ApiQLParser.Compound_operatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_compound_operator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            _la = self._input.LA(1)
            if not(_la==ApiQLParser.T__24 or _la==ApiQLParser.T__25):
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


    class ValuesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ApiQLParser.ValueContext)
            else:
                return self.getTypedRuleContext(ApiQLParser.ValueContext,i)


        def getRuleIndex(self):
            return ApiQLParser.RULE_values

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValues" ):
                return visitor.visitValues(self)
            else:
                return visitor.visitChildren(self)




    def values(self):

        localctx = ApiQLParser.ValuesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_values)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(ApiQLParser.T__2)
            self.state = 76
            self.value()
            self.state = 81
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ApiQLParser.T__26:
                self.state = 77
                self.match(ApiQLParser.T__26)
                self.state = 78
                self.value()
                self.state = 83
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 84
            self.match(ApiQLParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number(self):
            return self.getTypedRuleContext(ApiQLParser.NumberContext,0)


        def boolean(self):
            return self.getTypedRuleContext(ApiQLParser.BooleanContext,0)


        def nil(self):
            return self.getTypedRuleContext(ApiQLParser.NilContext,0)


        def datetime(self):
            return self.getTypedRuleContext(ApiQLParser.DatetimeContext,0)


        def string(self):
            return self.getTypedRuleContext(ApiQLParser.StringContext,0)


        def getRuleIndex(self):
            return ApiQLParser.RULE_value

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = ApiQLParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_value)
        try:
            self.state = 91
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ApiQLParser.NUMBER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 86
                self.number()
                pass
            elif token in [ApiQLParser.T__27, ApiQLParser.T__28]:
                self.enterOuterAlt(localctx, 2)
                self.state = 87
                self.boolean()
                pass
            elif token in [ApiQLParser.T__29]:
                self.enterOuterAlt(localctx, 3)
                self.state = 88
                self.nil()
                pass
            elif token in [ApiQLParser.T__30]:
                self.enterOuterAlt(localctx, 4)
                self.state = 89
                self.datetime()
                pass
            elif token in [ApiQLParser.STRING]:
                self.enterOuterAlt(localctx, 5)
                self.state = 90
                self.string()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ApiQLParser.RULE_boolean

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolean" ):
                return visitor.visitBoolean(self)
            else:
                return visitor.visitChildren(self)




    def boolean(self):

        localctx = ApiQLParser.BooleanContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_boolean)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            _la = self._input.LA(1)
            if not(_la==ApiQLParser.T__27 or _la==ApiQLParser.T__28):
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


    class NilContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ApiQLParser.RULE_nil

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNil" ):
                return visitor.visitNil(self)
            else:
                return visitor.visitChildren(self)




    def nil(self):

        localctx = ApiQLParser.NilContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_nil)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            self.match(ApiQLParser.T__29)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(ApiQLParser.NUMBER, 0)

        def getRuleIndex(self):
            return ApiQLParser.RULE_number

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber" ):
                return visitor.visitNumber(self)
            else:
                return visitor.visitChildren(self)




    def number(self):

        localctx = ApiQLParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            self.match(ApiQLParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DatetimeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def string(self):
            return self.getTypedRuleContext(ApiQLParser.StringContext,0)


        def getRuleIndex(self):
            return ApiQLParser.RULE_datetime

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDatetime" ):
                return visitor.visitDatetime(self)
            else:
                return visitor.visitChildren(self)




    def datetime(self):

        localctx = ApiQLParser.DatetimeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_datetime)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self.match(ApiQLParser.T__30)
            self.state = 100
            self.match(ApiQLParser.T__2)
            self.state = 101
            self.string()
            self.state = 102
            self.match(ApiQLParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(ApiQLParser.STRING, 0)

        def getRuleIndex(self):
            return ApiQLParser.RULE_string

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)




    def string(self):

        localctx = ApiQLParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.match(ApiQLParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





