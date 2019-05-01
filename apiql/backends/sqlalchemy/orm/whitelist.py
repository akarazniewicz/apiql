import inspect
from typing import Union, List, Iterator, Callable, Any, Iterable

from funcy import none
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql.elements import Label
from whatever import _

from apiql.backends.sqlalchemy.orm.expression import All


class Prefixed:

    def __init__(self, key: str, entity):
        self.key = key
        self.entity = entity


prefixed = Prefixed


class Mapped:

    def __init__(self, key: str, attribute):
        self.key = key
        self.attribute = attribute


mapped = Mapped


class Whitelist:

    def get_whitelisted_expression_builder(self, predicate: str):
        return self.predicates.lookup(predicate)

    def get_whitelisted_attribute(self, attribute: str):
        w = self.whitelisted_attrs
        return next((a for (n, a) in w if n == attribute), None)


def map_alias(key, attrs):
    return map(lambda a: (key + '.' + a[0], a[1]), attrs)


def extract_attributes(e: Union[Prefixed, AliasedClass, DeclarativeMeta], qualify: Callable[[Any], bool]) \
        -> Iterator[tuple]:

    if isinstance(e, Prefixed):
        members = inspect.getmembers(e.entity, qualify)
        return map_alias(e.key, members)
    elif isinstance(e, AliasedClass):
        target_attrs = inspect.getmembers(e._aliased_insp._target, qualify)
        return map(lambda s: (e._aliased_insp.name + '.' + s[0], getattr(e, s[0])), target_attrs)
    elif isinstance(e, DeclarativeMeta):
        return inspect.getmembers(e, qualify)
    else:
        raise TypeError('Unsupported entity type: \'{}\''.format(type(e)))


class WhitelistAll(Whitelist):

    def __init__(self, *entities):
        self.whitelisted_attrs = []

        def qualified(m):
            return isinstance(m, InstrumentedAttribute)

        for e in entities:
                self.whitelisted_attrs += extract_attributes(e, qualified)

    def get_whitelisted_expression_builder(self, predicate: str) -> bool:
        return All.lookup(predicate)


class WhitelistAllBut(Whitelist):

    def __init__(self, entities: Iterable[Union[Prefixed, AliasedClass, DeclarativeMeta]],
                 but: Iterable[InstrumentedAttribute], predicates=All):
        self.whitelisted_attrs = []
        self.predicates = predicates

        if not isinstance(entities, tuple):
            entities = (entities,)

        if not isinstance(but, tuple):
            but = (but,)

        def qualified(a) -> bool:
            return isinstance(a, InstrumentedAttribute) and none(a.key == _.key, but)

        for e in entities:
                self.whitelisted_attrs += extract_attributes(e, qualified)


class WhitelistJust(Whitelist):

    def __init__(self, attributes: Union[tuple, Union[InstrumentedAttribute, Mapped]], predicates=All):

        if not isinstance(attributes, tuple):
            attributes = (attributes,)

        self.whitelisted_attrs = []
        self.predicates = predicates

        for a in attributes:
            if isinstance(a, Mapped):
                self.whitelisted_attrs.append((a.key, a.attribute))
            elif isinstance(a, InstrumentedAttribute):
                if a.parent.is_aliased_class:
                    self.whitelisted_attrs.append((a.parent.name + '.' + a.key, a))
                else:
                    self.whitelisted_attrs.append((a.key, a))
            elif isinstance(a, Label):
                self.whitelisted_attrs.append((a.key, a))
            else:
                raise TypeError('Unsupported attribute type \'{}\''.format(type(a)))


class WhitelistMerged(Whitelist):

    def __init__(self, whitelists: List[Whitelist], predicates=All):

        self.whitelisted_attrs = []

        for w in whitelists:
            self.whitelisted_attrs += w.whitelisted_attrs

        self.predicates = predicates


everything_but = WhitelistAllBut
everything = WhitelistAll
just = WhitelistJust
merged = WhitelistMerged

Whitelist.All = WhitelistAll
Whitelist.AllBut = WhitelistAllBut
Whitelist.Just = WhitelistJust
Whitelist.Merged = WhitelistMerged
