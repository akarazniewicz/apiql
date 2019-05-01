import unittest

from apiql.criteria import Criteria, Predicate, Conjunction, Disjunction, DataDumpVisitor


class QueryTest(unittest.TestCase):

    def test_basic_predicate(self):

        d = [('a', '==', (True, False, 1))]

        q = Criteria.from_data(d)

        self.assertEqual(1, len(q.criteria))
        self.assertTrue(isinstance(q.criteria[0], Predicate))
        self.assertEqual(d[0], (q.criteria[0].keyword, q.criteria[0].op, q.criteria[0].value))

    def test_basic_predicates(self):

        d = [('a', 'in', (True, False, 1)), ('a', 'ilike', '"Foo" bar')]

        q = Criteria.from_data(d)

        self.assertEqual(2, len(q.criteria))
        self.assertTrue(isinstance(q.criteria[0], Predicate))
        self.assertTrue(isinstance(q.criteria[1], Predicate))
        self.assertEqual(d[0], (q.criteria[0].keyword, q.criteria[0].op, q.criteria[0].value))
        self.assertEqual(d[1], (q.criteria[1].keyword, q.criteria[1].op, q.criteria[1].value))

    def test_basic_conjunction(self):

        d = {'and': [('a', '==', '1')]}

        q = Criteria.from_data(d)

        self.assertEqual(1, len(q.criteria))
        self.assertTrue(isinstance(q.criteria[0], Conjunction))
        self.assertEqual(1, len(q.criteria[0].criteria))
        self.assertTrue(isinstance(q.criteria[0].criteria[0], Predicate))
        c = q.criteria[0].criteria[0]
        self.assertEqual(d['and'][0], (c.keyword, c.op, c.value))

    def test_basic_disjunction(self):

        d = {'or': [('a', '==', '1')]}

        q = Criteria.from_data(d)

        self.assertEqual(1, len(q.criteria))
        self.assertTrue(isinstance(q.criteria[0], Disjunction))
        self.assertEqual(1, len(q.criteria[0].criteria))
        self.assertTrue(isinstance(q.criteria[0].criteria[0], Predicate))
        c = q.criteria[0].criteria[0]
        self.assertEqual(d['or'][0], (c.keyword, c.op, c.value))

    def test_complex_criteria1(self):

        d = [{'and': [('a', 'in', (True, False, 1))]}, ('a', 'ilike', '"Foo" bar')]

        q = Criteria.from_data(d)

        self.assertEqual(2, len(q.criteria))
        self.assertTrue(isinstance(q.criteria[0], Conjunction))
        self.assertTrue(isinstance(q.criteria[1], Predicate))
        self.assertEqual(d[1], (q.criteria[1].keyword, q.criteria[1].op, q.criteria[1].value))
        c = q.criteria[0].criteria[0]
        self.assertEqual(d[0]['and'][0], (c.keyword, c.op, c.value))

    def test_complex_criteria2(self):

        d = [{'and': [('a', 'in', (True, False, 1)), {'or': [('c', '!=', "Bar"), ('d', 'ilike', 'Quux')]}]},
             ('a', 'ilike', '"Foo" bar')]

        q = Criteria.from_data(d)

        self.assertEqual(2, len(q.criteria))
        self.assertTrue(isinstance(q.criteria[0], Conjunction))
        self.assertTrue(isinstance(q.criteria[1], Predicate))
        self.assertEqual(d[1], (q.criteria[1].keyword, q.criteria[1].op, q.criteria[1].value))
        c = q.criteria[0].criteria[0]
        self.assertEqual(d[0]['and'][0], (c.keyword, c.op, c.value))
        self.assertTrue(isinstance(q.criteria[0].criteria[1], Disjunction))
        d = q.criteria[0].criteria[1].criteria[0]
        self.assertEqual(('c', '!=', "Bar"), (d.keyword, d.op, d.value))

    def test_data_dump(self):

        d = [('a', '==', 1)]

        dump = DataDumpVisitor()
        q = Criteria.from_data(d)

        dump.visit(q)

        self.assertEqual(d, dump.data)

    def test_data_dump2(self):

        d = [{'and': [('a', 'in', (True, False, 1)), {'or': [('c', '!=', "Bar"), ('d', 'ilike', 'Quux')]}]},
             ('a', 'ilike', '"Foo" bar')]

        dump = DataDumpVisitor()
        q = Criteria.from_data(d)

        dump.visit(q)

        self.assertEqual(d, dump.data)
