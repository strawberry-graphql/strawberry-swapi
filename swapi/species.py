import typing

import strawberry

from tables import species

from .page_info import PageInfo


@strawberry.type
class Specie:
    id: strawberry.ID
    name: str
    created: typing.Optional[str] = None
    edited: typing.Optional[str] = None
    designation: typing.Optional[str] = None
    eye_colors: typing.List[str] = None
    skin_colors: typing.List[str] = None
    hair_colors: typing.List[str] = None
    language: typing.Optional[str] = None
    average_lifespan: typing.Optional[int] = None
    average_height: typing.Optional[int] = None


@strawberry.type
class SpeciesEdge:
    node: typing.Optional[Specie]
    cursor: str

    @staticmethod
    def from_row(row):
        id_ = row[species.c.id]

        return SpeciesEdge(
            cursor=id_,
            node=Specie(
                id=id_,
                name=row[species.c.name],
                created=row[species.c.created],
                edited=row[species.c.edited],
                designation=row[species.c.designation],
                eye_colors=[
                    color.strip()
                    for color in row[species.c.eye_colors].split(",")
                ],
                skin_colors=[
                    color.strip()
                    for color in row[species.c.skin_colors].split(",")
                ],
                hair_colors=[
                    color.strip()
                    for color in row[species.c.hair_colors].split(",")
                ],
                language=row[species.c.language],
                average_lifespan=row[species.c.average_lifespan],
                average_height=row[species.c.average_height],
            ),
        )


@strawberry.type
class SpeciesConnection:
    page_info: PageInfo
    edges: typing.List[SpeciesEdge]
    total_count: int
    species: typing.List[Specie] = None


@strawberry.type
class FilmSpeciesEdge(SpeciesEdge):
    @staticmethod
    def from_row(row):
        id_ = row[species.c.id]

        return FilmSpeciesEdge(cursor=id_, node=Specie.from_row(row))


@strawberry.type
class FilmSpeciesConnection(SpeciesConnection):
    edges: typing.List[typing.Optional[FilmSpeciesEdge]]
