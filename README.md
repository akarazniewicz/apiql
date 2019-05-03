## ApiQL - a Simple API query language for RESTful services

ApiQL is a simple domain language for API consumers to express REST resource filtering criteria in a concise, powerful, URL friendly way.

# Installing

ApiQL can be installed and updated with pip:


``pip install apiql``

### API query language

Api query language provides set of predicates and expressions allowing API providers and consumers to build complex resource queries. While ApiQL syntax is in largely SQL inspired, it is designed to be technology agnostic. ApiQL is translated into abstract criteria tree and can be transformed into backend specific functionality. 

#### ApiQL query syntax

ApiQL query is set of basic predicates which may be then composed using conjunctions (`and`) or disjunctions (`or`) into expressions.

For example, let's assume we have REST API exposing movie information:

`wget -q -O - 'http://awso.me/api/movies'`

```javascript
[{
    "title": "Monty Python and the Holy Grail",
    "release_year": 1975,
    "original_title": "Monty Python and the Holy Grail"
    "created_datetime": "2019-05-01T09:17:06.527181+00:00",
    "external_id": "762",
    "genres": [{"id" : 1, "name": "Comedy"}, {"id" : 2, "name": "Adventure"}, {"id" : 2, "name": "Fantasy"}],
    "id": 1,
    "plot": "King Arthur, accompanied by his squire, recruits his Knights of the Round Table [...]",
    "rating": 6.0,  
    "source": "tmdb",
    "ignored": false
},

...

]
```

#### ApiQL query basics

In its most basic form, ApiQL query is just single predicate:

``wget -q -O - 'http://awso.me/api/movies?filter=title=="Monty Python and the Holy Grail"'``

which will filter only "Monty Python and the Holy Grails" resources. (whole ApiQL query is contained within single URL query param; note that ApiQL uses `==` operator for equality, not ``=``).

*Note: ApiQL was designed to be as much URL friendly as possible, however all ApiQL queries, should be URL-encoded. In this document we use ``wget`` as it URL-encodes all URLs by default; ``curl``  has little bit more arcane syntax in this case: ``curl -G   --data-urlencode "filter=[my ApiQL query]" http://awso.me/api/movies``*

##### ApiQL predicates

In reality API consumers require much more than simple ``==`` predicate. ApiQL supports following set of predicates:
* `==`, 
* `!=`, 
* `>`, 
* `>=`, 
* `<`, 
* `<=`, 
* `like` - equivalent SQL LIKE operator, however You don't need explicitly add `%`, 
* `ilike`- case insensitive version of `like`, 
* `notlike` - equivalent SQL NOT LIKE operator,
* `notilike` - case insensitive version on `notlike`, 
* `startswith` - equivalent to SQL STARTS WITH operator, 
* `istartswith` - case insensitive version of `startswith`, 
* `endswith` - equivalent to SQL ENDS WITH, 
* `iendswith` - case insensitive version of `iendswith`, 
* `contains` - alias to `like`, 
* `notcontains` - alias to `notlike`, 
* `icontains` - case insensitive version of `contains`,
* `inotcontains` - case insensitive version of `notcontains`,
* `in` - equivalent to SQL IN operator,
* `notin` equivalent to SQL NOT IN operator. 

For example, query:

``wget -q -O - 'http://awso.me/api/movies?filter=title ilike "Holy"'``

will return all movies matching "Holy": "Monty Python and the Holy Grails", "Holy Money" and possibly bunch of other filcks matching "Holy".

and query:

``wget -q -O - 'http://awso.me/api/movies?filter=release_year>=1975'``

will return all movies released in 1975 or later.

##### Query literals

Literals are the values, things that can be on the right hand side of predicate. So far we have seen strings ("Holy") and numeric literals (1975). ApiQL support bunch of other literals too:

* Strings - all string literals are unicode and are following the same rules like JSON string literals. ApiQL strings are always double-quoted (for example, this is a string: "This is a string", this however: 'not a string' *is not*), and escaped ("The movie: \\"The Movie\\"").
* Numbers - are basically integers and floats: `release_year != 2003` or `rating > 3.3` or even `rating > -1.6E-35`.
* Boolean - `true` and `false` are translated into platform specific booleans. Example usage: `ingored != false`
* Nil - special `null` literal is translated into platform specific literal, for example: `genres != null`
* Datetime - literal representing datetime: `created_datetime >= datetime("2019-05-01T08:00:00.527181+00:00")`. Out of the box ApiQL supports ISO-8601 datetime formats (however, this behavior can be customized). 
* Tuples - represents series of values in `in` and `notin` clauses: `release_year notin (1975, 2011)`. Tuples can contain coma separated list of other literals: `release_date in (flase, null, datetime("datetime("1975-01-01T00:00:00.000000+00:00"))`

#### Combining queries

Queries can be combined into more complicated expressions by grouping atomic predicates (separated by `;`).

For example:

``wget -q -O - 'http://awso.me/api/movies?filter=title ilike "Holy";release_year>1975;ignored!=null'``

predicates in this query are interpreted as `conjunction` (`and`), returning all movies with `title` matching "Holy" *and* released after 1975 which are not marked as `ignored`.

#### Logical expressions

ApiQL supports logical `conjunctions` (`and`) and `disjunctions` (`or`); both of them can nest predicates: `and(criteria(;criteria)*)`and`or(criteria(;criteria)*)`

Query below, is equivalent to the previous one:

``wget -q -O - 'http://awso.me/api/movies?filter=and(title ilike "Holy";release_year > 1975;ignored != true)'``

This one, however:

``wget -q -O -'http://awso.me/api/movies?filter=or(title ilike "Holy";release_year>1975;ignored!=true)'``

will return all movies with titles matching "Holy" *or* released after 1975 *or* not ignored.

Conjunctions and Disjunctions can be nested. Let's say we want to filter movies with rating greater than 7 or source is "IMDB", however we would like to filter only not-ignored resources:

``wget -q -O - 'http://awso.me/api/movies?filter=and(or(rating>7;source="IMDB");ignored!=flase)'``

### Parsing ApiQL queries

So far, so good. Now, how ApiQL Queries can actually be interpreted by API data store? ApiQL queries are internally translated into python data structure (syntax tree) represented by`Crtieria` class. 

``Criteria`` along with `Predicate`, `Conjunction` and `Disjunction` fully represents parsed query tree.

`Criteria` class aggregates list of `Criterion`. 

`Criterion` just abstract atomic criteria element; it's either:
*  simple `Predicate` an atomic logical expression (for example 
`Predicate('title', '==', 'Apocalypse Now')` for query `title=="Apocalypse Now"`)
* `Conjunction` which again is just logical ``and`` operator with group of predicates `Conjunction([Predicate('title','==', 'Apocalypse Now'),Predicate('release_year','>', 1975)])` for query `and(title=="Apocalypse Now";release_year>1975)`
* `Disjunction` - logical ``or`` operator

Parsing ApiQL query with python:

```python
import apiql.parser as parser
from apiql.criteria import Criteria, Conjunction, Disjunction, Predicate

# ...

parsed_criteria = parser.parse('and(title like "Monty";genres == null;ignored!=false;release_year<=1975)')
syntax_tree = Criteria(
    [Conjunction([
        Predicate('title', 'like', 'Monty'),
        Predicate('genres', '==', None),
        Predicate('ignored', '!=', False),
        Predicate('release_year', '<=', 1975)
    ])]
)

# parsed_criteria is equal to syntax_tree

assertEqual(syntax_tree, parsed_criteria)

```   
### A Tour of queries

Now we can actually use ApiQL to filter resources. Out of the box ApiQL provides SQLAlchemy ORM integration (it can be, however integrated with other backends). This section showcases all basic query examples. Complete list of query capabilities can be found in the test suite.

All examples will use this sample data model:

```python
Base = declarative_base()

class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    genre_id = Column(Integer)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=True)

class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    original_title = Column(String)
    release_year = Column(Integer)
    source = Column(String)
    rating = Column(String)
    created_datetime = Column(DateTime, default=datetime.utcnow)
	genres = relationship('Genre', cascade="all", backref="movie", lazy=True)

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

session.add(monty_python)
session.add(jurassic_park)
session.add(apocalypse_now)
session.add(gosford_park)
```

A main entry point to SQLAlchemy integration is ``with_criteria`` extension method, which extends plain SQLAlchemy ``Query`` object with ApiQL capabilities. ``with_criteria`` is following basic SQLAlchemy conventions, so it can be freely used with native ``filter_by`` or ``filter`` functions. 

Following examples show ApiQL queries and their native SQLAlchemy representations.
 
#### Simple conjunction criteria

```python
from apiql.backends.sqlalchemy.orm import with_criteria

actual = session.query(Movie).with_criteria('and(rating=="8";release_year==1975)')

# is equivalent to

expected = session.query(Movie).filter(
    and_(
        Movie.rating == 8,
        Movie.release_year == 1975
    )
)
```

#### Simple disjunction criteria

```python
from apiql.backends.sqlalchemy.orm import with_criteria

actual = session.query(Movie).with_criteria('or(rating=="8";release_year==1993;source=="TMDB")')

# is equivalent to

expected = session.query(Movie).filter(
    or_(
        Movie.rating == 8,
        Movie.release_year == 1993,
        Movie.source == 'TMDB'
    )
)

```

#### `<` and `>` predicates

```python

actual = session.query(Movie).with_criteria('and(release_year > 1975; release_year < 2001)')

# is equivalent to

expected = session.query(Movie).filter(
    and_(
        Movie.release_year > 1975,
        Movie.release_year < 2001
    )
)
```

#### `like` and `ilike` predicates

```python
actual = session.query(Movie).with_criteria('or(title like "THE"; original_title ilike "THE")')

# is equivalent to

expected = session.query(Movie).filter(
    or_(
        Movie.title.like('%THE%'),
        Movie.original_title.ilike("%THE%")
    )
)
```

#### `notlike` predicate

```python
actual = session.query(Movie).with_criteria('and(title notlike "the"; release_year > 1990)')

# is equivalent to

expected = session.query(Movie).filter(
    and_(
        Movie.title.notlike('%the%'),
        Movie.release_year > 1990
    )
)
```

#### `in` and `notin` predicate

```python
actual = session.query(Movie).with_criteria('release_year in (1979, 2001))')

# is equivalent to

expected = session.query(Movie).filter(
    Movie.release_year.in_((1979, 2001))
)
```
and 
```python
actual = session.query(Movie).with_criteria('release_year notin (1979, 2001))')

# is equivalent to

expected = session.query(Movie).filter(
    Movie.release_year.notin_((1979, 2001))
)
```

#### ``IS NULL`` and ``IS NOT NULL`` predicates

```python
actual = session.query(Movie).with_criteria('original_title == null)')

# is equivalent to

expected = session.query(Movie).filter(
    Movie.original_title.is_(None)
)
```
and
```python
actual = session.query(Movie).with_criteria('original_title != null)')

# is equivalent to

expected = session.query(Movie).filter(
    Movie.original_title.isnot(None)
)
```

#### `startswith` and `endswith` predicates

Following queries are equivalents

```python
actual = session.query(Movie).with_criteria('title startswith "The")')

# is equivalent to

expected = session.query(Movie).filter(
    Movie.title.startswith("The")
)
```
and
```python
actual = session.query(Movie).with_criteria('title endswith "Park")')

# is equivalent to

expected = session.query(Movie).filter(
    Movie.title.endswith("Park")
)
```

#### `contains` predicate

```python
actual = session.query(Movie).with_criteria('or(original_title contains "The";title contains "the")')

# is equivalent to

expected = session.query(Movie).filter(
    or_(
        Movie.original_title.contains('The'),
        Movie.title.contains('the')
    )
)
```

#### `datetime` literals

Following queries are equivalents
```python
now = datetime.datetime.now().isoformat()

actual = session.query(Movie).with_criteria('created_datetime<datetime("{}")'.format(now))

# is equivalent to

expected = session.query(Movie).filter(
    Movie.created_datetime < datetime.datetime.fromisoformat(now)
)
```

#### Joins and aliased entities

Joins are supported as well. Following queries are equivalents:

```python
actual = session.query(Movie).join(Genre).with_criteria('name=="War"')

# is equivalent to

expected = session.query(Movie).join(Genre).filter(
    Genre.name == 'War'
)
```
ApiQL supports `aliased` entities:

```python
kind = aliased(Genre, name='kind')
actual = session.query(Movie).join(kind).with_criteria('kind.name=="War"')

# is equivalent to

expected = session.query(Movie).join(kind).filter(
    kind.name == 'War'
)
```

### Complete API example with Flask-SQLAlchemy

ApiQL is technology agnostic whenever possible and can be used with all popular python web frameworks (Flask, Bottle, Django etc.). 

(side note: ApiQL reference implementation fully supports Flask-SQLAlchemy extension as well). 

Here's is a simple Flask API with ApiQL filtering (assuming ``Movie`` and ``Genre`` classes are ``json`` serializable)

```python
from apiql.backends.sqlalchemy.orm import with_criteria

# ...

@app.route("/api/movies", methods=["GET"])
def movies():
    criteria = request.args.get('filter', '')
    return jsonify(Movie.query.join(Genre).with_criteria(criteria).all())
```
Now we can filter resources with ApiQL:

``wget -q -O - 'localhost:5000/api/movies?filter=and(or(title like "Python";original_title like "Python");source=="TMDB")'``

Note: that we can use empty string when API consumer do not specify filtering query.

This query:

``wget -q -O - 'localhost:5000/api/movies'``

will return all, unfiltered resources.

#### Whitelisting API attributes

In most cases API providers gives only limited access to attributes consumers can use. ApiQL supports this capability by _whitelisting_ which attributes can be accessed in queries (this does not change however what attributes are exposed in resources).

Whitelists can be enabled with `whitelisted` `Query` extension method. _By default all resource attributes are are whitelisted_.

##### Whitelisting only specific attributes

ApiQL `just` builder will only whitelist explicitly specified resource attributes.

```python

from apiql.backends.sqlalchemy.orm import with_criteria, whitelisted
from apiql.backends.sqlalchemy.orm.whitelist import everything, everything_but, just, mapped, prefixed

@app.route("/api/movies", methods=["GET"])
def movies():
    criteria = request.args.get('filter', '')
    query = Movie.query.join(Genre).whitelisted(just((Movie.title, Movie.release_year))).with_criteria(criteria)
    return jsonify(query.all())
```

Now, this query:

``wget -q -O - 'http://localhost:5000/api/movies?filter=release_year==2001'``

will work just fine, as Movie.release_year is whitelisted,

however, this call:

``wget -q -O - 'http://localhost:5000/api/movies?filter=rating=="8.0"'``

will fail with:

``ValueError: Invalid query attribute: 'rating'``.

##### Whitelisting all attributes

`everything` builder whitelists *all* entity (or entities) attributes. This is default behavior when whitelist is not specified. ApiQL engine will scan all ``Query`` entities, and whitelist all attributes.

```python
from apiql.backends.sqlalchemy.orm import with_criteria, whitelisted
from apiql.backends.sqlalchemy.orm.whitelist import everything, everything_but, just, mapped, prefixed

@app.route("/api/movies", methods=["GET"])
def movies():
    criteria = request.args.get('filter', '')
    query = Movie.query.join(Genre).whitelisted(everything(Movie)).with_criteria(criteria)
    return jsonify(query.all())
```

Note, that in this case, only ``Movie`` attributes are whitelisted, while all ``Genre`` attributes are not.

In this case:

``wget -q -O - 'http://localhost:5000/api/movies?filter=rating=="8.0"'``

will work as expected. However, this query:

``wget -q -O - 'http://localhost:5000/api/movies?filter=name=="Sci-Fi"'``

will fail again.

##### Whitelisting all attributes, except specified set of attributes

`everything_but` builder whitelists all attributes, except those specified in ``but`` clause.

```python
from apiql.backends.sqlalchemy.orm import with_criteria, whitelisted
from apiql.backends.sqlalchemy.orm.whitelist import everything, everything_but, just, mapped, prefixed

@app.route("/api/movies", methods=["GET"])
def movies():
    criteria = request.args.get('filter', '')
    query = Movie.query.join(Genre).whitelisted(everything_but(entities=Movie, but=Movie.id)).with_criteria(criteria)
    return jsonify(query.all())
```

Now, this call will fail as ``Movie.id`` is not whitelisted:

``wget -q -O - 'http://localhost:5000/api/movies?filter=id==1'``

##### Merging whitelists
 
Finally `merged` whitelist builder can combine (merge) two whitelists. Following example:

```python
from apiql.backends.sqlalchemy.orm import with_criteria, whitelisted
from apiql.backends.sqlalchemy.orm.whitelist import everything, everything_but, just, mapped, prefixed

@app.route("/api/movies", methods=["GET"])
def movies():    
    criteria = request.args.get('filter', '')
    query = Movie.query.join(Genre).whitelisted(merged([everything(Movie), just(Genre.name)])).with_criteria(criteria)
    return jsonify(query.all())
```

will whitelist all attributes from `Movie` and just `Genre.name` from ``Genre``.

#### Prefixed attributes

Query attributes can be prefixed to be more consumer friendly. For instance, in above examples, `name` attribute will resolve to `Genre.name` (we don't have column name collision here between ``Movie`` and ``Genre``). However from consumer perspective it would be much elegant to map this attribute to something more obvious; `prefixed` does exactly this. Here's an example:
```python
from apiql.backends.sqlalchemy.orm.whitelist import everything, everything_but, just, mapped, prefixed

actual = session.query(Movie).join(Genre) \
            .whitelisted(everything(Movie, prefixed('genre', Genre))) \
            .with_criteria('rating=="9";genre.name=="War"')

# is equivalent to

expected = session.query(Movie).filter(Movie.rating == "9") \
    .join(Genre).filter(Genre.name == 'War')
```

#### Mapped attributes

Sometimes we would like to expose query attribute under different name (for example we would like to keep backward contract compatibility). `mapped` function is does just for this.

Let's say we would like to map `Genre.name` to query attribute `kind`, so we can use nicer queries like ``kind=="War"``

```python
from apiql.backends.sqlalchemy.orm import with_criteria, whitelisted
from apiql.backends.sqlalchemy.orm.whitelist import everything, everything_but, just, mapped, prefixed

@app.route("/api/movies", methods=["GET"])
def movies():    
    criteria = request.args.get('filter', '')
    query = Movie.query.join(Genre).whitelisted(just(mapped('kind', Genre.name))).with_criteria(criteria)
    return jsonify(query.all())
```




