import datetime
import unittest

from funcy import some, none
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker, aliased
from whatever import _

from apiql.backends.sqlalchemy.orm import with_criteria, whitelisted
from apiql.backends.sqlalchemy.orm.whitelist import Whitelist, prefixed, everything, just, mapped
from tests.backends.sqlalchemy_fixtures import Movie, Genre, Base


class TestSQLAlchemyCriteriaFiltering(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///')
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        drama = Genre(name="Drama", genre_id=1)
        scifi = Genre(name="Sci-Fi", genre_id=2)
        war = Genre(name="War", genre_id=3)
        adventure = Genre(name="Adventure", genre_id=4)
        comedy = Genre(name="Comedy", genre_id=5)

        self.monty_python = Movie(title="Monty Python and the Holy Grail", release_year=1975, source="IMDB", rating="8",
                                  genres=[comedy, adventure])

        self.jurassic_park = Movie(title="Jurassic Park", release_year=1993, source='IMDB', rating="9",
                                   genres=[adventure, scifi])

        self.apocalypse_now = Movie(title="Apocalypse Now", release_year=1979, source="TMDB", rating="9",
                                    original_title="Apocalypse Now, The", genres=[drama, war])

        self.gosford_park = Movie(title="Gosford Park", release_year=2001, source='IMDB', rating="7", genres=[drama])

        # we are adding entities separately to make sure we have different timestamps for testing dates.
        self.session.add(self.monty_python)
        self.session.commit()
        self.session.add(self.jurassic_park)
        self.session.commit()
        self.session.add(self.apocalypse_now)
        self.session.commit()
        self.session.add(self.gosford_park)
        self.session.commit()

    def test_simple_disjunction(self):
        session = self.session
        actual = session.query(Movie).with_criteria('or(rating=="8";release_year==1993)')

        expected = session.query(Movie).filter(
            or_(
                Movie.rating == 8,
                Movie.release_year == 1993,
            )
        )

        results = actual.all()

        self.assertEqual(str(expected), str(actual))
        self.assertEqual(2, len(results))
        self.assertEqual(2, len(expected.all()))
        self.assertTrue(some(_.title == 'Monty Python and the Holy Grail', results))
        self.assertTrue(some(_.title == 'Jurassic Park', results))

    def test_simple_multi_param_disjunction(self):
        session = self.session
        actual = session.query(Movie).with_criteria('or(rating=="8";release_year==1993;source=="TMDB")')

        expected = session.query(Movie).filter(
            or_(
                Movie.rating == 8,
                Movie.release_year == 1993,
                Movie.source == 'TMDB'
            )
        )

        results = actual.all()
        self.assertEqual(str(expected), str(actual))
        self.assertEqual(3, len(results))
        self.assertEqual(3, len(expected.all()))
        self.assertTrue(none(_.title == 'Gosford Park', results))

    def test_simple_conjunction(self):
        session = self.session
        actual = session.query(Movie).with_criteria('and(rating=="8";release_year==1975)')

        expected = session.query(Movie).filter(
            and_(
                Movie.rating == 8,
                Movie.release_year == 1975
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(results))
        self.assertEqual(1, len(expected.all()))
        self.assertTrue('Monty Python and the Holy Grail', results[0])

    def test_top_level_criteria_list(self):
        session = self.session
        actual = session.query(Movie).with_criteria('release_year==1975')

        expected = session.query(Movie).filter(Movie.release_year == 1975)

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(results))
        self.assertEqual(1, len(expected.all()))
        self.assertTrue('Monty Python and the Holy Grail', results[0])

    def test_top_level_multi_criteria_list(self):
        session = self.session
        actual = session.query(Movie).join(Genre) \
            .whitelisted(everything(Movie, prefixed('genre', Genre))) \
            .with_criteria('rating=="9";genre.name=="War"')

        expected = session.query(Movie).filter(Movie.rating == "9") \
            .join(Genre).filter(Genre.name == 'War')

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(results))
        self.assertEqual(1, len(expected.all()))
        self.assertTrue('Apocalypse Now', results[0])

    def test_simple_multi_param_conjunction(self):
        session = self.session
        actual = session.query(Movie).with_criteria('and(rating=="8";release_year==1975;source=="IMDB")')

        expected = session.query(Movie).filter(
            and_(
                Movie.rating == 8,
                Movie.release_year == 1975,
                Movie.source == "IMDB"
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(results))
        self.assertEqual(1, len(expected.all()))
        self.assertTrue('Monty Python and the Holy Grail', results[0])

    def test_conjunction_with_nested_disjunction(self):
        session = self.session
        actual = session.query(Movie).join(Genre) \
            .whitelisted(just((Movie.source, Movie.rating, mapped('genre.name', Genre.name)))) \
            .with_criteria('and(source=="IMDB";or(rating=="9";genre.name=="Drama"))')

        expected = session.query(Movie).join(Genre).filter(
            and_(
                Movie.source == "IMDB",
                or_(
                    Movie.rating == "9",
                    Genre.name == "Drama"
                )
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(2, len(results))
        self.assertEqual(2, len(expected.all()))
        self.assertTrue(some(_.title == 'Gosford Park', results))
        self.assertTrue(some(_.title == 'Jurassic Park', results))

    def test_multiple_nested_criteria(self):
        session = self.session
        actual = session.query(Movie).join(Genre) \
            .whitelisted(Whitelist.All(Movie, prefixed('genre', Genre))) \
            .with_criteria('and(and(source=="IMDB";or(rating=="9";genre.name=="Drama"));genre.name=="Sci-Fi")')

        expected = session.query(Movie).join(Genre).filter(
            and_(
                and_(
                    Movie.source == "IMDB",
                    or_(
                        Movie.rating == "9",
                        Genre.name == "Drama"
                    )
                ),
                Genre.name == "Sci-Fi"
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(results))
        self.assertEqual(1, len(expected.all()))
        self.assertTrue(some(_.title == 'Jurassic Park', results))

    def test_neq(self):
        session = self.session
        actual = session.query(Movie).join(Genre) \
            .whitelisted(Whitelist.All(Movie, prefixed('genre', Genre))) \
            .with_criteria(
            'and( genre.name != "Drama"; genre.name != "Sci-Fi"; genre.name != "War"; genre.name != "Adventure" )')

        expected = session.query(Movie).join(Genre).filter(
            and_(
                Genre.name != "Drama",
                Genre.name != "Sci-Fi",
                Genre.name != "War",
                Genre.name != "Adventure"
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(results))
        self.assertEqual(1, len(expected.all()))
        self.assertTrue('Monty Python and the Holy Grail', results[0].title)

    def test_gt_lt(self):
        session = self.session
        actual = session.query(Movie).with_criteria('and(release_year > 1975; release_year < 2001)')

        expected = session.query(Movie).filter(
            and_(
                Movie.release_year > 1975,
                Movie.release_year < 2001
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(2, len(results))
        self.assertEqual(2, len(expected.all()))
        self.assertTrue(some(_.title == 'Jurassic Park', results))
        self.assertTrue(some(_.title == 'Apocalypse Now', results))

    def test_gte_lte(self):
        session = self.session
        actual = session.query(Movie).with_criteria(
            'and(release_year >= 1979; release_year <= 2010)')

        expected = session.query(Movie).filter(
            and_(
                Movie.release_year >= 1979,
                Movie.release_year <= 2010
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(3, len(results))
        self.assertEqual(3, len(expected.all()))
        self.assertTrue(some(_.title == 'Apocalypse Now', results))
        self.assertTrue(some(_.title == 'Jurassic Park', results))
        self.assertTrue(some(_.title == 'Gosford Park', results))

    def test_like(self):
        session = self.session
        actual = session.query(Movie).with_criteria('or(title like "Park"; original_title like "The")')

        expected = session.query(Movie).filter(
            or_(
                Movie.title.like('%Park%'),
                Movie.original_title.like("%The%")
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(3, len(results))
        self.assertEqual(3, len(expected.all()))
        self.assertTrue(some(_.title == 'Apocalypse Now', results))
        self.assertTrue(some(_.title == 'Jurassic Park', results))
        self.assertTrue(some(_.title == 'Gosford Park', results))

    def test_ilike(self):
        session = self.session
        actual = session.query(Movie).with_criteria('or(title ilike "THE"; original_title ilike "THE")')

        expected = session.query(Movie).filter(
            or_(
                Movie.title.ilike('%THE%'),
                Movie.original_title.ilike("%THE%")
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(2, len(actual.all()))
        self.assertEqual(2, len(results))
        self.assertTrue(some(_.title == 'Apocalypse Now', results))
        self.assertTrue(some(_.title == 'Monty Python and the Holy Grail', results))

    def test_notlike(self):
        session = self.session
        actual = session.query(Movie).with_criteria('and(title notlike "the"; release_year > 1990)')

        expected = session.query(Movie).filter(
            and_(
                Movie.title.notlike('%the%'),
                Movie.release_year > 1990
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(2, len(expected.all()))
        self.assertEqual(2, len(results))
        self.assertTrue(some(_.title == 'Jurassic Park', results))
        self.assertTrue(some(_.title == 'Gosford Park', results))

    def test_in1(self):
        session = self.session
        actual = session.query(Movie).join(Genre).with_criteria(
            'and(name in ("Sci-Fi", "War"); release_year > 1990)')

        expected = session.query(Movie).join(Genre).filter(
            and_(
                Genre.name.in_(('Sci-Fi', 'War')),
                Movie.release_year > 1990
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(expected.all()))
        self.assertEqual(1, len(results))
        self.assertTrue('Jurassic Park', results[0].title)

    def test_in2(self):
        session = self.session
        actual = session.query(Movie).with_criteria(
            'and(original_title in ("Apocalypse Now, The", null); release_year > 1970)')

        expected = session.query(Movie).filter(
            and_(
                Movie.original_title.in_(('Apocalypse Now, The', None)),
                Movie.release_year > 1970
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(expected.all()))
        self.assertEqual(1, len(results))
        self.assertEqual('Apocalypse Now', results[0].title)

    def test_in3(self):
        session = self.session
        actual = session.query(Movie).with_criteria('release_year in (1979, 2001))')

        expected = session.query(Movie).filter(
            Movie.release_year.in_((1979, 2001))
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(2, len(expected.all()))
        self.assertEqual(2, len(results))
        self.assertTrue(some(_.title == 'Gosford Park', results))
        self.assertTrue(some(_.title == 'Apocalypse Now', results))

    def test_isnull(self):
        session = self.session
        actual = session.query(Movie).with_criteria('original_title == null)')

        expected = session.query(Movie).filter(
            Movie.original_title.is_(None)
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(3, len(expected.all()))
        self.assertEqual(3, len(results))
        self.assertTrue(none(_.title == 'Apocalypse Now', results))

    def test_isnotnull(self):
        session = self.session
        actual = session.query(Movie).with_criteria('original_title != null)')

        expected = session.query(Movie).filter(
            Movie.original_title.isnot(None)
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(expected.all()))
        self.assertEqual(1, len(results))
        self.assertEqual('Apocalypse Now', results[0].title)

    def test_in4(self):
        session = self.session
        actual = session.query(Movie).with_criteria('release_year in (null, true, "2001"))')

        expected = session.query(Movie).filter(
            Movie.release_year.in_((None, True, '2001'))
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(expected.all()))
        self.assertEqual(1, len(results))
        self.assertEqual('Gosford Park', results[0].title)

    def test_notin(self):
        session = self.session
        actual = session.query(Movie).with_criteria('release_year notin (1979, 2001))')

        expected = session.query(Movie).filter(
            Movie.release_year.notin_((1979, 2001))
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(2, len(expected.all()))
        self.assertEqual(2, len(results))
        self.assertTrue(some(_.title == 'Monty Python and the Holy Grail', results))
        self.assertTrue(some(_.title == 'Jurassic Park', results))

    def test_startswith2(self):
        session = self.session
        actual = session.query(Movie).with_criteria('title startswith "The")')

        expected = session.query(Movie).filter(
            Movie.title.startswith("The")
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(0, len(expected.all()))
        self.assertEqual(0, len(results))

    def test_endswidth(self):
        session = self.session
        actual = session.query(Movie).with_criteria('title endswith "Park")')

        expected = session.query(Movie).filter(
            Movie.title.endswith("Park")
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(2, len(expected.all()))
        self.assertEqual(2, len(results))
        self.assertTrue(some(_.title == 'Jurassic Park', results))
        self.assertTrue(some(_.title == 'Gosford Park', results))

    def test_contains(self):
        session = self.session
        actual = session.query(Movie).with_criteria('or(original_title contains "The";title contains "the")')

        expected = session.query(Movie).filter(
            or_(
                Movie.original_title.contains('The'),
                Movie.title.contains('the')
            )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(2, len(expected.all()))
        self.assertEqual(2, len(results))
        self.assertTrue(some(_.title == 'Apocalypse Now', results))
        self.assertTrue(some(_.title == 'Monty Python and the Holy Grail', results))

    def test_datetime1(self):
        now = datetime.datetime.now().isoformat()

        session = self.session
        actual = session.query(Movie).with_criteria('created_datetime<datetime("{}")'.format(now))

        expected = session.query(Movie).filter(
            Movie.created_datetime < datetime.datetime.fromisoformat(now)
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(4, len(expected.all()))
        self.assertEqual(4, len(results))

    def test_datetime2(self):
        session = self.session

        monty_python_datetime = session.query(Movie).filter(Movie.title == 'Monty Python and the Holy Grail') \
            .first().created_datetime.isoformat()
        apocalypse_now_datetime = session.query(Movie).filter(Movie.title == 'Apocalypse Now') \
            .first().created_datetime.isoformat()

        actual = session.query(Movie).with_criteria('created_datetime notin (datetime("{}"), datetime("{}"))'
                                                    .format(monty_python_datetime, apocalypse_now_datetime))

        expected = session.query(Movie).filter(
            Movie.created_datetime.notin_((datetime.datetime.fromisoformat(monty_python_datetime),
                                           datetime.datetime.fromisoformat(apocalypse_now_datetime))
                                          )
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(2, len(expected.all()))
        self.assertEqual(2, len(results))
        self.assertTrue(some(_.title == 'Jurassic Park', results))
        self.assertTrue(some(_.title == 'Gosford Park', results))

    def test_empty_criteria(self):
        session = self.session
        actual = session.query(Movie).with_criteria('')

        expected = session.query(Movie)

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(4, len(expected.all()))
        self.assertEqual(4, len(results))

    def test_simple_join(self):
        session = self.session
        actual = session.query(Movie).join(Genre).with_criteria('name=="War"')

        expected = session.query(Movie).join(Genre).filter(
            Genre.name == 'War'
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(expected.all()))
        self.assertEqual(1, len(results))
        self.assertTrue(some(_.title == 'Apocalypse Now', results))

    def test_aliased1(self):
        session = self.session
        kind = aliased(Genre, name='kind')
        actual = session.query(Movie).join(kind).with_criteria('kind.name=="War"')

        expected = session.query(Movie).join(kind).filter(
            kind.name == 'War'
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(expected.all()))
        self.assertEqual(1, len(results))
        self.assertTrue(some(_.title == 'Apocalypse Now', results))

    def test_aliased2(self):
        session = self.session
        kind = aliased(Genre, name='kind')
        actual = session.query(Movie).join(kind) \
            .whitelisted(just(kind.name)).with_criteria('kind.name=="War"')

        expected = session.query(Movie).join(kind).filter(
            kind.name == 'War'
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(expected.all()))
        self.assertEqual(1, len(results))
        self.assertTrue(some(_.title == 'Apocalypse Now', results))

    def test_aliased3(self):
        session = self.session
        kind = aliased(Genre, name='kind')
        actual = session.query(Movie).join(kind) \
            .whitelisted(everything(kind)).with_criteria('kind.name=="War"')

        expected = session.query(Movie).join(kind).filter(
            kind.name == 'War'
        )

        results = actual.all()
        self.assertEqual(str(actual), str(expected))
        self.assertEqual(1, len(expected.all()))
        self.assertEqual(1, len(results))
        self.assertTrue(some(_.title == 'Apocalypse Now', results))
