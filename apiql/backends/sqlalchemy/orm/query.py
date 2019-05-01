from typing import Callable, Any

from funcy import monkey, flatten, lmap, select
from sqlalchemy import and_, or_
from sqlalchemy.orm import Query

from apiql import parser
from apiql.backends.sqlalchemy.orm.whitelist import Whitelist, merged, everything, just
from apiql.criteria import CriteriaVisitor, Predicate, Conjunction, Disjunction, Criteria
from apiql.grammar import default_deserializer
from apiql.grammar.transformer import ValueTypes


class SQLAlchemyCriteriaVisitor(CriteriaVisitor):
    filters = None

    def __init__(self, whitelist: Whitelist):
        self.whitelist = whitelist

    def visit_predicate(self, predicate: Predicate):
        attribute = self.whitelist.get_whitelisted_attribute(predicate.keyword)

        if attribute is None:
            raise ValueError('Invalid query attribute: \'{}\'.'.format(predicate.keyword))

        expression = self.whitelist.get_whitelisted_expression_builder(predicate.op)

        if predicate is None:
            raise ValueError('Invalid predicate: \'{}\'.'.format(predicate.op))

        return expression.build(attribute, predicate.value)

    def visit_conjunction(self, conjunction: Conjunction):
        return and_(*map(lambda c: c.accept(self), conjunction.criteria))

    def visit_disjunction(self, disjunction: Disjunction):
        return or_(*map(lambda c: c.accept(self), disjunction.criteria))

    def visit(self, criteria: Criteria):
        return lmap(lambda c: c.accept(self), criteria.criteria)


@monkey(Query)
def whitelisted(self, whitelist: Whitelist):
    self.whitelist = whitelist
    return self


def qualified_attribute(s):
    from sqlalchemy.orm.attributes import InstrumentedAttribute
    from sqlalchemy.sql.elements import Label
    return isinstance(s, InstrumentedAttribute) or isinstance(s, Label)


def discover_attributes(query):

    entities = []
    attributes = []

    from sqlalchemy.orm import Mapper
    from sqlalchemy.orm.query import _MapperEntity, _ColumnEntity
    from sqlalchemy.ext.declarative import DeclarativeMeta
    from sqlalchemy.orm.util import AliasedInsp

    def unwrap_entities(ents):

        def unwrap_mapper(e):

            if isinstance(e, Mapper):
                return e.entity
            elif isinstance(e, DeclarativeMeta):
                return e
            else:
                raise TypeError('Unsupported mapped entity type {}. Cannot automatically '
                                'map entity to query properties.'.format(type(e)))

        subjects = []
        for e in ents:

            if isinstance(e, _MapperEntity):
                subjects += lmap(unwrap_mapper, flatten(e.entities))
            elif isinstance(e, _ColumnEntity):
                subjects.append(e.expr)
            elif isinstance(e, AliasedInsp):
                subjects.append(e.entity)
            elif isinstance(e, Mapper):
                subjects.append(unwrap_mapper(e))
            else:
                raise TypeError("Unsupported entity Mapper type: {}. Cannot automatically map entities"
                                " to query properties.".format(type(e)))

        return subjects

    if query._entities is not None:
        subjects = unwrap_entities(query._entities)
        entities = select(lambda s: not qualified_attribute(s), subjects)
        attributes = select(qualified_attribute, subjects)

    if query._join_entities is not None:
        entities += unwrap_entities(query._join_entities)

    return merged(whitelists=[everything(*entities),
                              just(attributes=tuple(attributes))])


@monkey(Query)
def with_criteria(self, criteria: str, deserializer: Callable[[ValueTypes, Any], Any] = default_deserializer):

    # for empty criteria we just don't do any filtering.
    if criteria is None or not criteria:
        return self

    if not hasattr(self, 'whitelist') or not self.whitelist:
        self.whitelist = discover_attributes(self)

    c = parser.parse(criteria, deserializer=deserializer)
    sqlalchemy_builder = SQLAlchemyCriteriaVisitor(self.whitelist)

    return self.filter(*sqlalchemy_builder.visit(c))

