from base64 import b64encode, b64decode

import strawberry


@strawberry.interface
class Node:
    id: strawberry.ID

    @staticmethod
    def get_global_id(type_name: str, id: str | int) -> str:
        return b64encode(f"{type_name}:{id}".encode()).decode()

    @staticmethod
    def get_id(obj: object) -> int:
        id_: str = obj.id  # type: ignore

        return Node.get_id_from_string(id_)

    @staticmethod
    def get_id_from_string(id_: str) -> int:
        return int(b64decode(id_.encode()).decode().split(":")[1])
