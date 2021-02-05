class Edge():
    def __init__(self, v_1: int, v_2: int, weight: float = 0.0) -> None:
        self.v_1 = v_1
        self.v_2 = v_2
        self.weight = weight

    def __repr__(self) -> str:
        return '[Edge: {} <-{}-> {}]'.format(self.v_1, self.weight, self.v_2)

    def __eq__(self, other) -> bool:
        return self.v_1 == other.v_1 and self.v_2 == other.v_2

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self) -> int:
        return hash(str(self.v_1) +
                    str(self.v_2)) if self.v_1 <= self.v_2 else hash(
                        str(self.v_2) + str(self.v_1))

    def set_weight(self, weight: float) -> float:
        self.weight = weight
        return self.weight
