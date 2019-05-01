
class Aggregate:

    def __init__(self, operator):
        self.aggregate = [operator]

    def __or__(self, other):
        self.aggregate += [other]
        return self

    def lookup(self, op: str):
        return next((o for o in self.aggregate if o.op == op), None)


class ExpressionMeta(type):

    def __or__(self, other):
        return Aggregate(self) | other


class Expression(metaclass=ExpressionMeta):
    pass


class Eq(Expression):
    op = '=='

    @classmethod
    def build(cls, attr, val):
        return attr == val


class Neq(Exception):
    op = '!='

    @classmethod
    def build(cls, attr, value):
            return attr != value


class Gt(Expression):
    op = '>'

    @classmethod
    def build(cls, attr, value):
        return attr > value


class Gte(Expression):
    op = '>='

    @classmethod
    def build(cls, attr, value):
        return attr >= value


class Lt(Expression):
    op = '<'

    @classmethod
    def build(cls, attr, value):
        return attr < value


class Lte(Expression):
    op = '<='

    @classmethod
    def build(cls, attr, value):
        return attr <= value


class Like(Expression):
    op = 'like'

    @classmethod
    def build(cls, attr, value):
        return attr.like("%{}%".format(value))


class NotLike(Expression):
    op = 'notlike'

    @classmethod
    def build(cls, attr, value):
        return attr.notlike('%{}%'.format(value))


class Ilike(Expression):
    op = 'ilike'

    @classmethod
    def build(cls, attr, value):
        return attr.ilike('%{}%'.format(value))


class NotIlike(Expression):
    op = 'notilike'

    @classmethod
    def build(cls, attr, value):
        return attr.notilike('%{}%'.format(value))


class In(Expression):
    op = 'in'

    @classmethod
    def build(cls, attr, value):
        return attr.in_(value)


class NotIn(Expression):
    op = 'notin'

    @classmethod
    def build(cls, attr, value):
        return attr.notin_(value)


class StartsWith(Expression):
    op = 'startswith'

    @classmethod
    def build(cls, attr, value):
        return attr.startswith(value)


class EndsWith(Expression):
    op = 'endswith'

    @classmethod
    def build(cls, attr, value):
        return attr.endswith(value)


class Contains(Expression):
    op = 'contains'

    @classmethod
    def build(cls, attr, value):
        return attr.contains(value)


class NotContains(Expression):
    op = 'notcontains'

    @classmethod
    def build(cls, attr, value):
        return attr.notcontians(value)


All = Eq | Neq | Gt | Gte | Lt | Lte | Like | NotLike | Ilike | NotIlike | In | NotIn \
      | StartsWith | EndsWith | Contains | NotContains

Core = Eq | Neq | Gt | Gte | Lt | Lte

Compare = Like | NotIlike | Ilike | NotIlike | In | NotIn | StartsWith | EndsWith | Contains | NotContains