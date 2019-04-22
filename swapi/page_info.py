import typing

import strawberry


@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: typing.Optional[str] = None
    end_cursor: typing.Optional[str] = None
