import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, aliased

from apiql.backends.sqlalchemy.orm.whitelist import everything, everything_but, just, mapped, prefixed
from tests.backends.sqlalchemy_fixtures import Genre, Movie, Base


class WhitelistTest(unittest.TestCase):

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

        monty_python = Movie(title="Monty Python and the Holy Grail", release_year=1975, source="IMDB", rating="8",
                             genres=[comedy, adventure])

        jurassic_park = Movie(title="Jurassic Park", release_year=1993, source='IMDB', rating="9",
                              genres=[adventure, scifi])

        apocalypse_now = Movie(title="Apocalypse Now", release_year=1979, source="TMDB", rating="9",
                               original_title="Apocalypse Now, The", genres=[drama, war])

        gosford_park = Movie(title="Gosford Park", release_year=2001, source='IMDB', rating="7", genres=[drama])

        self.session.add_all([monty_python, jurassic_park, apocalypse_now, gosford_park])

    def test_whitelist_all(self):

        all_whitelisted = everything(Genre)

        self.assertEqual(5, len(all_whitelisted.whitelisted_attrs))
        self.assertEqual(Genre.id, all_whitelisted.get_whitelisted_attribute('id'))
        self.assertEqual(Genre.name, all_whitelisted.get_whitelisted_attribute('name'))
        self.assertEqual(Genre.genre_id, all_whitelisted.get_whitelisted_attribute('genre_id'))
        self.assertEqual(Genre.movie_id, all_whitelisted.get_whitelisted_attribute('movie_id'))
        self.assertIsNotNone(all_whitelisted.get_whitelisted_attribute('movie'))

    def test_whitelist_all_prefixed(self):

        all_whitelisted = everything(prefixed('test', Genre))

        self.assertEqual(5, len(all_whitelisted.whitelisted_attrs))
        self.assertEqual(Genre.id, all_whitelisted.get_whitelisted_attribute('test.id'))
        self.assertEqual(Genre.name, all_whitelisted.get_whitelisted_attribute('test.name'))
        self.assertEqual(Genre.genre_id, all_whitelisted.get_whitelisted_attribute('test.genre_id'))
        self.assertEqual(Genre.movie_id, all_whitelisted.get_whitelisted_attribute('test.movie_id'))
        self.assertIsNotNone(all_whitelisted.get_whitelisted_attribute('test.movie'))

    def test_whitelist_all_but(self):

        wl = everything_but(Genre, but=(Genre.name, Genre.id))

        self.assertEqual(3, len(wl.whitelisted_attrs))
        self.assertIsNone(wl.get_whitelisted_attribute('id'))
        self.assertIsNone(wl.get_whitelisted_attribute('name'))
        self.assertEqual(Genre.genre_id, wl.get_whitelisted_attribute('genre_id'))
        self.assertEqual(Genre.movie_id, wl.get_whitelisted_attribute('movie_id'))
        self.assertIsNotNone(wl.get_whitelisted_attribute('movie'))

    def test_whitelist_all_but_prefixed(self):

        wl = everything_but(prefixed('test', Genre), but=(Genre.name, Genre.id))

        self.assertEqual(3, len(wl.whitelisted_attrs))
        self.assertIsNone(wl.get_whitelisted_attribute('test.id'))
        self.assertIsNone(wl.get_whitelisted_attribute('test.name'))
        self.assertEqual(Genre.genre_id, wl.get_whitelisted_attribute('test.genre_id'))
        self.assertEqual(Genre.movie_id, wl.get_whitelisted_attribute('test.movie_id'))

    def test_just(self):

        whitelisted1 = just(Genre.name)
        whitelisted2 = just((Genre.name, Genre.id))

        self.assertEqual(1, len(whitelisted1.whitelisted_attrs))
        self.assertEqual(Genre.name, whitelisted1.get_whitelisted_attribute('name'))

        self.assertEqual(2, len(whitelisted2.whitelisted_attrs))
        self.assertEqual(Genre.name, whitelisted2.get_whitelisted_attribute('name'))
        self.assertEqual(Genre.id, whitelisted2.get_whitelisted_attribute('id'))

    def test_mapped(self):

        whitelisted1 = just(mapped('foo', Genre.name))
        whitelisted2 = just((mapped('bar', Genre.name), Genre.id))

        self.assertEqual(2, len(whitelisted2.whitelisted_attrs))
        self.assertEqual(Genre.name, whitelisted2.get_whitelisted_attribute('bar'))
        self.assertEqual(Genre.id, whitelisted2.get_whitelisted_attribute('id'))
        self.assertEqual(1, len(whitelisted1.whitelisted_attrs))
        self.assertEqual(Genre.name, whitelisted1.get_whitelisted_attribute('foo'))

    def test_automatic_whitelisting(self):
        session = self.session

        actual = session.query(Movie).with_criteria('title=="Foo"')

        self.assertEqual(8, len(actual.whitelist.whitelisted_attrs))

    def test_automatic_whitelisting_multiple_entities(self):
        session = self.session

        actual = session.query(Movie, Genre).with_criteria('title=="Foo"')

        self.assertEqual(13, len(actual.whitelist.whitelisted_attrs))

    def test_automatic_whitelisting_joins(self):
        session = self.session

        actual = session.query(Movie).join(Genre).with_criteria('title=="Foo"')

        self.assertEqual(13, len(actual.whitelist.whitelisted_attrs))

    def test_automatic_aliased_whitelist(self):
        session = self.session
        kind = aliased(Genre, name='kind')
        actual = session.query(Movie).join(kind).with_criteria('kind.name=="Foo"')

        expected = session.query(Movie).join(kind).filter(
            kind.name == "Foo"
        )

        self.assertEqual(13, len(actual.whitelist.whitelisted_attrs))
        self.assertEqual(str(expected), str(actual))

    def test_automatic_labelled_attribute_whitelist(self):
        session = self.session
        actual = session.query(Movie.original_title.label('aka')).with_criteria('aka=="Foo"')

        self.assertEqual(1, len(actual.whitelist.whitelisted_attrs))
        self.assertEqual(Movie.original_title.label('aka').name,
                         actual.whitelist.get_whitelisted_attribute('aka').name)

    def test_mapped_specific_columns(self):

        session = self.session
        actual = session.query(Movie.release_year, Movie.title).with_criteria('release_year==1979')

        expected = session.query(Movie.release_year, Movie.title).filter(
            Movie.release_year == 1979
        )

        self.assertEqual(str(expected), str(actual))

    def test_aliased_all_but(self):

        flix = aliased(Movie, name='flix')

        wl = everything_but(entities=flix, but=flix.source)
        self.assertEqual(7, len(wl.whitelisted_attrs))
        self.assertIsNone(wl.get_whitelisted_attribute('flix.source'))

