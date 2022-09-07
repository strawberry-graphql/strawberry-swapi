from base64 import b64encode

import strawberry


@strawberry.interface
class Node:
    id: strawberry.ID

    @staticmethod
    def get_global_id(type_name: str, id: str | int) -> str:
        return b64encode(f"{type_name}:{id}".encode()).decode()
