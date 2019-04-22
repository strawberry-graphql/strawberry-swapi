import strawberry


@strawberry.interface
class Node:
    id: strawberry.ID
