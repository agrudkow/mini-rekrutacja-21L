
class Vertex():
    def __init__(self, id: int, x: float = 0.0, y: float = 0.0) -> None:
        self.id = id
        self.x = x
        self.y = y

    def __eq__(self, o) -> bool:
        return self.id == o.id

    def __ne__(self, o):
        return not (self == o)

    def __hash__(self) -> int:
        return hash(self.id)
