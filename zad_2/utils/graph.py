
from typing import Dict, List
from utils.edge import Edge
from utils.vertex import Vertex


class Graph():
    def __init__(self, vertices: Dict[int, Vertex], edges: List[Edge]) -> None:
        self.vertices = vertices
        self.edges = edges
