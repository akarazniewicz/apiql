from abc import ABC, abstractmethod
from typing import Union


class CriteriaVisitor(ABC):
    """
    Criteria visitor interface.
    """

    @abstractmethod
    def visit_predicate(self, predicate: 'Predicate'):
        pass

    @abstractmethod
    def visit_conjunction(self, conjunction: 'Conjunction'):
        pass

    @abstractmethod
    def visit_disjunction(self, disjunction: 'Disjunction'):
        pass

    @abstractmethod
    def visit(self, criteria: 'Criteria'):
        pass


class Criterion(ABC):

    @abstractmethod
    def accept(self, visitor: CriteriaVisitor):
        pass


class Predicate(Criterion):

    def __init__(self, keyword: str, op: str, value: Union[list, dict]):
        self.keyword = keyword
        self.op = op
        self.value = value

    def accept(self, visitor: CriteriaVisitor):
        return visitor.visit_predicate(self)

    def __repr__(self):
        return 'Predicate({}, {}, {})'.format(self.keyword, self.op, self.value)

    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return False
        else:
            return self.keyword == other.keyword and \
                   self.op == other.op and \
                   self.value == other.value


class Conjunction(Criterion):

    def __init__(self, criteria=None):
        if criteria is None:
            criteria = []
        self.criteria = criteria

    def accept(self, visitor: CriteriaVisitor):
        return visitor.visit_conjunction(self)

    def __repr__(self):
        return 'Conjunction([{}])'.format(', '.join(map(str, self.criteria)))

    def __eq__(self, other):
        if not isinstance(other, Conjunction):
            return False
        else:
            return self.criteria == other.criteria


class Disjunction(Criterion):

    def __init__(self, criteria=None):
        if criteria is None:
            criteria = []
        self.criteria = criteria

    def accept(self, visitor: CriteriaVisitor):
        return visitor.visit_disjunction(self)

    def __repr__(self):
        return 'Disjunction([{}])'.format(', '.join(map(str, self.criteria)))

    def __eq__(self, other):
        if not isinstance(other, Disjunction):
            return False
        else:
            return self.criteria == other.criteria


class DataDumpVisitor(CriteriaVisitor):

    def __init__(self):
        self.data = None

    def visit_predicate(self, predicate: Predicate):
        return predicate.keyword, predicate.op, predicate.value

    def visit_disjunction(self, conjunction: Disjunction):
        return {'or': [criterion.accept(self) for criterion in conjunction.criteria]}

    def visit_conjunction(self, conjunction: Conjunction):
        return {'and': [criterion.accept(self) for criterion in conjunction.criteria]}

    def visit(self, query: 'Criteria'):
        criteria = [criterion.accept(self) for criterion in query.criteria]

        if len(criteria) == 1 and isinstance(criteria[0], dict):
            self.data = criteria.pop()
        else:
            self.data = criteria

        return self.data


class Criteria:

    def __init__(self, criteria=None):
        if criteria is None:
            criteria = []
        self.criteria = criteria

    def __repr__(self):
        return 'Criteria([{}])'.format(', '.join(map(str, self.criteria)))

    def __eq__(self, other):
        if not isinstance(other, Criteria):
            return False
        else:
            return self.criteria == other.criteria

    @classmethod
    def from_data(cls, query_spec: Union[dict, list]) -> 'Criteria':

        def _query_builder(query_spec):
            if isinstance(query_spec, list):
                return [_query_builder(k) for k in query_spec]
            if isinstance(query_spec, tuple):
                kw, op, val = query_spec
                return Predicate(kw, op, val)
            else:
                for k, v in query_spec.items():
                    if k == 'and':
                        return Conjunction(_query_builder(v))
                    elif k == 'or':
                        return Disjunction(_query_builder(v))

        value = _query_builder(query_spec)

        return Criteria(value if isinstance(value, list) else [value])

    def to_data(self) -> Union[dict, list]:
        return DataDumpVisitor().visit(self)
