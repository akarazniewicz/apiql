import datetime

from apiql.criteria import Criteria, Conjunction, Predicate

import apiql.parser as parser

import unittest


class ApiQueryDSLTest(unittest.TestCase):

    def test_none_criteria_should_fail(self):
        self.assertRaises(ValueError, parser.parse, None)

    def test_empty_criteria_should_fail(self):
        self.assertRaises(ValueError, parser.parse, "")

    def test_invalid_property_name_should_fail1(self):
        self.assertRaises(parser.ParseError, parser.parse, "2foo==1")

    def test_invalid_empty_conjunction(self):
        self.assertRaises(parser.ParseError, parser.parse, "and()")

    def test_invalid_empty_disjunction(self):
        self.assertRaises(parser.ParseError, parser.parse, "or()")

    def test_invalid_empty_nested_criteria1(self):
        self.assertRaises(parser.ParseError, parser.parse, "or(and())")

    def test_invalid_empty_nested_criteria2(self):
        self.assertRaises(parser.ParseError, parser.parse, "or();or()")

    def test_invalid_empty_nested_criteria3(self):
        self.assertRaises(parser.ParseError, parser.parse, "and(or();or())")

    def test_nested_conjunctions(self):
        self.assertEqual({'and': [{'and': [('foo', '==', True)]}]}, parser.parse("and(and(foo==true))").to_data())

    def test_no_effect_disjunction_with_additional_elems(self):
        self.assertEqual({'and': [{'and': [('foo', '==', True)]}, ('bar', '==', True)]},
                         parser.parse("and(and(foo==true);bar==true)").to_data())

    def test_test_datetime(self):
        date_time = datetime.datetime.now().isoformat()
        self.assertEqual([('foo', '==', datetime.datetime.fromisoformat(date_time))],
                         parser.parse('foo==datetime("{}")'.format(date_time)).to_data())

    def test_eq(self):
        self.assertEqual({'and': [('a', '==', 7), ('b', '==', 8)]}, parser.parse('and(a == 7;b == 8)').to_data())

    def test_neq(self):
        self.assertEqual({'and': [('a', '!=', None), ('b', '!=', True)]}, parser.parse('and(a != null; b != true)').to_data())

    def test_gt(self):
        self.assertEqual({'and': [('a', '>', 9), ('b', '>', 22.2)]}, parser.parse('and(a > 9; b > 22.2)').to_data())

    def test_gte(self):
        self.assertEqual({'and': [('a', '>=', 9), ('b', '>=', 22.2)]}, parser.parse('and(a >= 9; b >= 22.2)').to_data())

    def test_lt(self):
        self.assertEqual({'and': [('a', '<', 9), ('b', '<', 22.2)]}, parser.parse('and(a < 9; b < 22.2)').to_data())

    def test_lte(self):
        self.assertEqual({'and': [('a', '<=', 9), ('b', '<=', 22.2)]}, parser.parse('and(a <= 9; b <= 22.2)').to_data())

    def test_like(self):
        self.assertEqual({'and': [('a', 'like', 'Foo "Bar"'), ('b', 'like', '"Baz" Quux')]},
                         parser.parse('and(a like "Foo \\"Bar\\""; b like "\\"Baz\\" Quux")').to_data())

    def test_notlike(self):
        self.assertEqual({'and': [('a', 'notlike', 'Foo "Bar"'), ('b', 'like', '"Baz" Quux')]},
                         parser.parse('and(a notlike "Foo \\"Bar\\""; b like "\\"Baz\\" Quux")').to_data())

    def test_ilike(self):
        self.assertEqual({'and': [('a', 'ilike', 'Foo "Bar"'), ('b', 'like', '"Baz" Quux')]},
                         parser.parse('and(a ilike "Foo \\"Bar\\""; b like "\\"Baz\\" Quux")').to_data())

    def test_notilike(self):
        self.assertEqual({'and': [('a', 'notilike', 'Foo')]},
                         parser.parse('and(a notilike "Foo")').to_data())

    def test_in(self):
        self.assertEqual({'and': [('a', 'in', (True, False, None, 'Foo "Bar"')), ('b', '==', 42)]},
                         parser.parse('and(a in (true, false, null, "Foo \\"Bar\\""); b == 42)').to_data())

    def test_in_numerics(self):
        self.assertEqual({'and': [('a', 'in', (1, 2, 3, 4.2)), ('b', '==', 42)]},
                         parser.parse('and(a in (1,2,3,4.2); b == 42)').to_data())

    def test_notin(self):
        self.assertEqual({'and': [('a', 'notin', (True, False, None, 'Foo "Bar"')), ('b', '==', 42)]},
                         parser.parse('and(a notin (true, false, null, "Foo \\"Bar\\""); b == 42)').to_data())

    def test_startswith(self):
        self.assertEqual({'and': [('a', 'startswith', 'Foo "Bar"'), ('b', '==', 42)]},
                         parser.parse('and(a startswith "Foo \\"Bar\\""; b == 42)').to_data())

    def test_istartswith(self):
        self.assertEqual({'and': [('a', 'startswith', 'Foo "Bar"'), ('b', 'istartswith', 'Bar Baz')]},
                         parser.parse('and(a startswith "Foo \\"Bar\\""; b istartswith "Bar Baz")').to_data())

    def test_endswith(self):
        self.assertEqual({'and': [('a', 'endswith', 'Foo "Bar"'), ('b', 'istartswith', 'Bar Baz')]},
                         parser.parse('and(a endswith "Foo \\"Bar\\""; b istartswith "Bar Baz")').to_data())

    def test_iendswith(self):
        self.assertEqual({'and': [('a', 'iendswith', 'Foo "Bar"'), ('b', 'istartswith', 'Bar Baz')]},
                         parser.parse('and(a iendswith "Foo \\"Bar\\""; b istartswith "Bar Baz")').to_data())

    def test_contains(self):
        self.assertEqual({'and': [('a', 'contains', 'Foo "Bar"'), ('b', 'contains', 'Bar Baz')]},
                         parser.parse('and(a contains "Foo \\"Bar\\""; b contains "Bar Baz")').to_data())

    def test_icontains(self):
        self.assertEqual({'and': [('a', 'icontains', 'Foo "Bar"'), ('b', 'icontains', 'Bar Baz')]},
                         parser.parse('and(a icontains "Foo \\"Bar\\""; b icontains "Bar Baz")').to_data())

    def test_match(self):
        self.assertEqual({'and': [('a', 'match', 'Foo "Bar"'), ('b', '!=', None)]},
                         parser.parse('and(a match "Foo \\"Bar\\""; b != null)').to_data())

    def test_basic_sting_atrribute(self):
        self.assertEqual(parser.parse('foo like "Remington & Shaw: \\"Who? Me!\\""').to_data(),
                         [('foo', 'like', 'Remington & Shaw: "Who? Me!"')])

    def test_key_underscore_name(self):
        self.assertEqual(parser.parse('__foo__.bar.baz.__2quux!=true').to_data(), [('__foo__.bar.baz.__2quux', '!=', True)])

    def test_basic_boolean_attribute(self):
        self.assertEqual(parser.parse('foo==false').to_data(), [('foo', '==', False)])

    def test_basic_null_attribute(self):
        self.assertEqual(parser.parse('foo==null').to_data(), [('foo', '==', None)])

    def test_basic_float_attribute(self):
        self.assertEqual(parser.parse('foo >= -7.3').to_data(), [('foo', '>=', -7.3)])

    def test_basic_integer_attribute(self):
        self.assertEqual(parser.parse('foo == -42').to_data(), [('foo', '==', -42)])

    def test_basic_range_attribute(self):
        self.assertEqual(parser.parse('foo in (-42, null)').to_data(), [('foo', 'in', (-42, None))])

    def test_basic_single_range_attribute(self):
        self.assertEqual(parser.parse('foo in (1)').to_data(), [('foo', 'in', (1,))])

    def test_basic_empty_range_should_fail(self):
        self.assertRaises(parser.ParseError, parser.parse, 'foo in ()')

    def test_basic_range_for_simple_operator_should_fail(self):
        self.assertRaises(parser.ParseError, parser.parse, 'foo == (1,2)')

    def test_multiple_top_level_elements(self):
        self.assertEqual(parser.parse('foo like "Foo";bar in (1,2)').to_data(), [('foo', 'like', 'Foo'), ('bar', 'in', (1, 2))])

    def test_basic_conjunction(self):
        self.assertEqual(parser.parse('and(foo==7)').to_data(), {'and': [('foo', '==', 7)]})

    def test_basic_conjunction_with_top_level_attribute(self):
        self.assertEqual(parser.parse('bar==7;and(foo like "Foo Bar")').to_data(),
                         [
                             ('bar', '==', 7),
                             {'and': [
                                 ('foo', 'like', "Foo Bar")
                             ]}]
                         )

    def test_basic_conjunction_with_top_level_suffixed_attribute(self):
        self.assertEqual(parser.parse('and(foo=="Foo Bar");bar==7').to_data(),
                         [
                             {'and': [
                                 ('foo', '==', "Foo Bar")
                             ]},
                             ('bar', '==', 7)
                         ]
                         )

    def test_basic_nested_conjunction(self):
        self.assertEqual(parser.parse('and(or(foo==true))').to_data(),
                         {'and': [
                             {
                                 'or': [('foo', '==', True)]
                             }
                         ]
                         }
                         )

    def test_conjunction_with_whitespaces(self):
        self.assertEqual(parser.parse('and ( foo like "Foo Bar"; baz == null; quux !=false;ber <=  42)').to_data(),
                         {'and': [
                             ('foo', 'like', "Foo Bar"),
                             ('baz', '==', None),
                             ('quux', '!=', False),
                             ('ber', '<=', 42)
                         ]}
                         )

    def test_crieria_eq(self):

        parsed_criteria = parser.parse('and(title like "Monty";genres == null;ignored!=false;release_year<=1975)')
        syntax_tree = Criteria(
            [Conjunction([
                Predicate('title', 'like', 'Monty'),
                Predicate('genres', '==', None),
                Predicate('ignored', '!=', False),
                Predicate('release_year', '<=', 1975)

            ])]
        )

        self.assertEqual(syntax_tree, parsed_criteria)

    def test_complex_nested_conjunction(self):
        self.assertEqual(parser.parse(
            'and(foo like "Foo \\"Bar\\"";or(baz in (null, true, false, "Foo \\"Bar\\"");quux==false);ber>=-42)')
                         .to_data(),
            {'and': [
                ('foo', 'like', 'Foo "Bar"'),
                {'or': [
                    ('baz', 'in', (None, True, False, 'Foo "Bar"')),
                    ('quux', '==', False)
                ]},
                ('ber', '>=', -42)
            ]}
        )

    def test_complex_nested_disjunction(self):
        self.assertEqual(parser.parse(
            'or(foo like "Foo \\"Bar\\"";and(baz in (null, true, false, "Foo \\"Bar\\"");or(quux!=false));and(zazz<=-42))')
                         .to_data(),
            {'or': [
                ('foo', 'like', 'Foo "Bar"'),
                {'and': [
                    ('baz', 'in', (None, True, False, 'Foo "Bar"')),
                    {'or': [('quux', '!=', False)]}
                ]},
                {'and': [('zazz', '<=', -42)]}
            ]}
        )
