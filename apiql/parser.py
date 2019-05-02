from typing import Callable, Any

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from apiql.criteria import Criteria
from apiql.grammar.transformer import ValueTypes
from .grammar import ApiQLLexer, ApiQLParser, ApiQLASTTransformerVisitor, default_deserializer


class ParseError(Exception):
    pass


class ParseErrorListener(ErrorListener):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ParseError('Syntax error in column {}: {}'.format(column, msg))


def parse(query: str, deserializer: Callable[[ValueTypes, Any], Any] = default_deserializer) -> Criteria:
    if not query:
        raise ValueError("Query string cannot be null.")

    lexer = ApiQLLexer(InputStream(query))
    parser = ApiQLParser(CommonTokenStream(lexer))
    parser.addErrorListener(ParseErrorListener())
    transformer = ApiQLASTTransformerVisitor(deserializer=deserializer)

    return transformer.visit(parser.criteria())
