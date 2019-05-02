import dateutil.parser
from enum import Enum
from typing import Any, Callable

from funcy import lmap

from . import ApiQLVisitor, ApiQLParser

from ..criteria import Conjunction, Disjunction, Predicate, Criteria



class ValueTypes(Enum):
    DATETIME = 1
    NUMBER = 2
    BOOLEAN = 3


def default_deserializer(value_type: ValueTypes, value: Any) -> Any:
    if value_type == ValueTypes.DATETIME:
        return dateutil.parser.parse(value)

    if value_type == ValueTypes.NUMBER:
        try:
            return int(value)
        except:
            return float(value)

    if value_type == ValueTypes.BOOLEAN:
        if value == 'true':
            return True
        else:
            return False


# noinspection PyBroadException
class ApiQLASTTransformerVisitor(ApiQLVisitor):
    """
    Transformer transforming antlr AST into parser independent query data structure.
    """

    def __init__(self, deserializer: Callable[[ValueTypes, Any], Any] = default_deserializer):
        self.deserializer = deserializer

    # symbols to ignore
    ignored_terms = ('and', 'or', 'datetime', ',', '(', ')', ';')

    def filter_ignored(self, node):
        """
        Predicate to filter AST terms we are not interested in.
        :return: True, if given node should be excluded from building tree.
        """
        return node.getText() not in self.ignored_terms

    def visit(self, tree):
        return Criteria(ApiQLVisitor.visit(self, tree))

    def visitConjunction(self, ctx: ApiQLParser.ConjunctionContext):
        return Conjunction(ctx.criteria().accept(self))

    def visitDisjunction(self, ctx: ApiQLParser.DisjunctionContext):
        return Disjunction(ctx.criteria().accept(self))

    def visitCriteria(self, ctx: ApiQLParser.CriteriaContext):
        """
        Builds complete query criteria from parser antlr tree.
        """
        return lmap(lambda c: c.accept(self), ctx.getChildren(self.filter_ignored))

    def visitCriterion(self, ctx: ApiQLParser.CriterionContext):
        return self.visitChildren(ctx)

    def visitBasic_predicate(self, ctx: ApiQLParser.Basic_predicateContext):
        return Predicate(ctx.keyword().getText(), ctx.basic_operator().getText(), ctx.value().accept(self))

    def visitCompound_predicate(self, ctx: ApiQLParser.Compound_predicateContext):
        return Predicate(ctx.keyword().getText(), ctx.compound_operator().getText(), ctx.values().accept(self))

    def visitValues(self, ctx: ApiQLParser.ValuesContext):
        values = tuple(map(lambda c: c.accept(self), ctx.getChildren(self.filter_ignored)))
        return values

    def visitNumber(self, ctx: ApiQLParser.NumberContext):
        return self.deserializer(ValueTypes.NUMBER, ctx.getText())

    def visitBoolean(self, ctx: ApiQLParser.BooleanContext):
        value = ctx.getText()
        if value == 'true':
            return True
        else:
            return False

    def visitNil(self, ctx: ApiQLParser.NilContext):
        return None

    def visitString(self, ctx: ApiQLParser.StringContext):
        """
        Antlr  keeps string in wrapped (meaning keeping leading and trailing '"'s). We unwrap, and unescape it.
        :return: unescaped string.
        """
        return bytes(ctx.getText(), "utf-8").decode('unicode_escape')[1:-1]

    def visitDatetime(self, ctx: ApiQLParser.DatetimeContext):
        return self.deserializer(ValueTypes.DATETIME, next(ctx.getChildren(self.filter_ignored)).getText()[1:-1])
