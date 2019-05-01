# Generated from C:/Users/karaznie/apiql/apiql/grammar\ApiQL.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ApiQLParser import ApiQLParser
else:
    from ApiQLParser import ApiQLParser

# This class defines a complete generic visitor for a parse tree produced by ApiQLParser.

class ApiQLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ApiQLParser#criteria.
    def visitCriteria(self, ctx:ApiQLParser.CriteriaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#criterion.
    def visitCriterion(self, ctx:ApiQLParser.CriterionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#conjunction.
    def visitConjunction(self, ctx:ApiQLParser.ConjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#disjunction.
    def visitDisjunction(self, ctx:ApiQLParser.DisjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#predicate.
    def visitPredicate(self, ctx:ApiQLParser.PredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#basic_predicate.
    def visitBasic_predicate(self, ctx:ApiQLParser.Basic_predicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#compound_predicate.
    def visitCompound_predicate(self, ctx:ApiQLParser.Compound_predicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#keyword.
    def visitKeyword(self, ctx:ApiQLParser.KeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#basic_operator.
    def visitBasic_operator(self, ctx:ApiQLParser.Basic_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#compound_operator.
    def visitCompound_operator(self, ctx:ApiQLParser.Compound_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#values.
    def visitValues(self, ctx:ApiQLParser.ValuesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#value.
    def visitValue(self, ctx:ApiQLParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#boolean.
    def visitBoolean(self, ctx:ApiQLParser.BooleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#nil.
    def visitNil(self, ctx:ApiQLParser.NilContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#number.
    def visitNumber(self, ctx:ApiQLParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#datetime.
    def visitDatetime(self, ctx:ApiQLParser.DatetimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiQLParser#string.
    def visitString(self, ctx:ApiQLParser.StringContext):
        return self.visitChildren(ctx)



del ApiQLParser