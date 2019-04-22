import sqlalchemy
from databases import Database

from settings import DATABASE_URL

metadata = sqlalchemy.MetaData()

movies = sqlalchemy.Table(
    "movies",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(length=100), unique=True),
    sqlalchemy.Column("director", sqlalchemy.String(length=100)),
    sqlalchemy.Column("producer", sqlalchemy.String(length=100)),
    sqlalchemy.Column("episode_id", sqlalchemy.Integer),
    sqlalchemy.Column("edited", sqlalchemy.DateTime()),
    sqlalchemy.Column("release_date", sqlalchemy.Date()),
    sqlalchemy.Column("opening_crawl", sqlalchemy.Text()),
)


people = sqlalchemy.Table(
    "people",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=100), unique=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime()),
    sqlalchemy.Column("edited", sqlalchemy.DateTime()),
    sqlalchemy.Column("gender", sqlalchemy.String(length=100)),
    sqlalchemy.Column("skin_color", sqlalchemy.String(length=100)),
    sqlalchemy.Column("hair_color", sqlalchemy.String(length=100)),
    sqlalchemy.Column("height", sqlalchemy.Integer),
    sqlalchemy.Column("mass", sqlalchemy.Float),
    sqlalchemy.Column("eye_color", sqlalchemy.String(length=100)),
    sqlalchemy.Column("birth_year", sqlalchemy.String(length=100)),
    sqlalchemy.Column("homeworld_id", sqlalchemy.Integer),
)


planets = sqlalchemy.Table(
    "planets",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=100), unique=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime()),
    sqlalchemy.Column("edited", sqlalchemy.DateTime()),
    sqlalchemy.Column("climate", sqlalchemy.String(length=100)),
    sqlalchemy.Column("terrain", sqlalchemy.String(length=100)),
    sqlalchemy.Column("gravity", sqlalchemy.String(length=100)),
    sqlalchemy.Column("surface_water", sqlalchemy.Integer),
    sqlalchemy.Column("diameter", sqlalchemy.Integer),
    sqlalchemy.Column("rotation_period", sqlalchemy.Integer),
    sqlalchemy.Column("orbital_period", sqlalchemy.Integer),
    sqlalchemy.Column("population", sqlalchemy.Integer),
)


species = sqlalchemy.Table(
    "species",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=100), unique=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime()),
    sqlalchemy.Column("edited", sqlalchemy.DateTime()),
    sqlalchemy.Column("designation", sqlalchemy.String(length=100)),
    sqlalchemy.Column("eye_colors", sqlalchemy.String(length=250)),
    sqlalchemy.Column("skin_colors", sqlalchemy.String(length=250)),
    sqlalchemy.Column("hair_colors", sqlalchemy.String(length=250)),
    sqlalchemy.Column("language", sqlalchemy.String(length=100)),
    sqlalchemy.Column("average_lifespan", sqlalchemy.Integer),
    sqlalchemy.Column("average_height", sqlalchemy.Integer),
    #   "people": [66, 67, 68, 74],
    #   "homeworld": 9,
)


starships = sqlalchemy.Table(
    "starships",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=100), unique=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime()),
    sqlalchemy.Column("edited", sqlalchemy.DateTime()),
    sqlalchemy.Column("model", sqlalchemy.String(length=100)),
    sqlalchemy.Column("manufacturer", sqlalchemy.String(length=100)),
    sqlalchemy.Column("cost_in_credits", sqlalchemy.String(length=100)),
    sqlalchemy.Column("length", sqlalchemy.String(length=100)),
    sqlalchemy.Column("max_atmosphering_speed", sqlalchemy.String(length=100)),
    sqlalchemy.Column("crew", sqlalchemy.String(length=100)),
    sqlalchemy.Column("passengers", sqlalchemy.String(length=100)),
    sqlalchemy.Column("cargo_capacity", sqlalchemy.String(length=100)),
    sqlalchemy.Column("consumables", sqlalchemy.String(length=100)),
    sqlalchemy.Column("hyperdrive_rating", sqlalchemy.String(length=100)),
    sqlalchemy.Column("MGLT", sqlalchemy.String(length=100)),
    sqlalchemy.Column("starship_class", sqlalchemy.String(length=100)),
    # pilots
    # films
)


database = Database(DATABASE_URL)
