import numpy as np
from typing import Dict, List, Set, Tuple, TypeVar, Union
from utils.graph import Graph, Edge, Vertex

T = TypeVar('T')


class CityGraph():
    def __init__(self) -> None:
        self.graph: Union[Graph, None] = None
        self.n = 5
        self.is_city = np.array([1, 1, 0, 0, 0])
        self.m = 2
        self.connected_cities = np.array([[1, 2], [2, 3]])
        self.cities_cords = np.array([
            [1, 1],
            [3, 1],
            [1, 3],
            [3, 3],
            [2, 2],
        ])

    def calculate_weight(self, v_1: int, v_2: int) -> float:
        '''
        Metoda wyznaczająca wagę dla krawędzi `v_1 <--> v2`
        '''
        weight = np.linalg.norm(self.cities_cords[v_1] -
                                self.cities_cords[v_2])

        is_city_v_1, is_city_v_2 = self.is_city[v_1], self.is_city[v_2]

        if is_city_v_1 == 1 and is_city_v_2 == 1:
            weight *= 2
        elif is_city_v_1 == 0 and is_city_v_2 == 0:
            weight *= 0.5

        return round(weight, 2)

    def calculate_weights(self, edges: List[Edge]) -> List[Edge]:
        '''
        Metoda przypisująca wyznaczająca wagę dla listy krawędzi,
        których waga jest różna od `0.0`.
        '''
        # Stwórz tymczasowy zbiór krawędzi z wagą 0.0
        tmp_edges_set = set(edge for edge in edges)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                edge = Edge(i, j, 0.0)
                if edge not in tmp_edges_set:
                    edge.set_weight(self.calculate_weight(i, j))
                    edges.append(edge)

        return edges

    def apply_connected_cities(self, edges: List[Edge]) -> List[Edge]:
        '''
        Metoda przypisująca połączonym miastom wagę `0.0`
        '''
        for v_1, v_2 in self.connected_cities:
            edge = Edge(v_1, v_2, 0.0)
            edges.append(edge)

        return edges

    def create_edges(self) -> List[Edge]:
        '''
        Metoda tworząca listę krawędzi
        '''
        edges: List[Edge] = []
        self.apply_connected_cities(edges)
        self.calculate_weights(edges)

        return edges

    def create_vertices_dict(self) -> Dict[int, Vertex]:
        '''
        Metoda tworząca słownik krawędzi
        '''
        vertices: List[Tuple[int, Vertex]] = []
        for i in range(self.n):
            x, y = self.cities_cords[i]
            vertex = Vertex(i, x, y)
            vertices.append((hash(vertex), vertex))

        return dict(vertices)

    def create_graph(self) -> None:
        '''
        Metoda tworząca graf pełny z przypisanymi wagami.

        Lista krawędzi tego grafu jest odrazu posortowana rosnąco.
        '''
        vertices = self.create_vertices_dict()
        edges = self.create_edges()
        edges = sorted(edges, key=lambda edge: edge.weight)

        self.graph = Graph(vertices, edges)

    def find_vertex_set(self, forest: List[Set[Vertex]],
                        edge: Edge) -> Tuple[int, int]:
        '''
        Metoda znajdująca zbiory/drzewa w których znajdują
        się wierzchołki danej krawędzi.
        '''
        v_1 = Vertex(edge.v_1)
        v_2 = Vertex(edge.v_2)
        v_1_index: Union[int, None] = None
        v_2_index: Union[int, None] = None

        for i in range(len(forest)):
            if v_1 in forest[i]:
                v_1_index = i

            if v_2 in forest[i]:
                v_2_index = i

            if v_1_index is not None and v_2_index is not None:
                return (v_1_index, v_2_index)

        raise RuntimeError('Vertices not found')

    def remove_indecies(self, list: List[T], idx_1: int,
                        idx_2: int) -> List[T]:
        '''
        Metoda usuwająca z przekazanej listy dwa elementy
        o indeksach `idx_1` i `idx_2`
        '''
        if idx_1 > idx_2:
            del list[idx_1]
            del list[idx_2]
        else:
            del list[idx_1]
            del list[idx_2 - 1]

        return list

    def eval_kruskal(self) -> Tuple[float, List[Edge]]:
        '''
        Metoda wyznaczająca MST algorytmem Kruskala.

        Metoda zwraca krotkę zawierającą całkowity koszt
        MST oraz listę krawędzi MST.
        '''
        if self.graph is not None:
            total_cost: float = 0.0
            # Zainicjalizuj las (jażdy wirzchołek należy do osobnego zbioru)
            forest: List[Set[Vertex]] = [
                set([vertex]) for vertex in self.graph.vertices.values()
            ]
            mst: List[Edge] = []

            # Iteruj dla kolejnych rosnących krawędzi w grafie
            for edge in self.graph.edges:
                # Jeśli nie ma więcej niepołączonych wierzchołków
                if len(forest) == 1:
                    break
                v_1_index, v_2_index = self.find_vertex_set(forest, edge)
                # Jeśli wierzchołki należą do tego samego zbioru to pomiń
                if v_1_index != v_2_index:
                    # dodaj krawędź do MST
                    mst.append(edge)
                    # zwiększ koszt
                    total_cost += edge.weight
                    # Połącz zbiory wierzchołków
                    forest.append(forest[v_1_index].union(forest[v_2_index]))
                    # Usuń stare zbiory/drzewa z lasu
                    self.remove_indecies(forest, v_1_index, v_2_index)

            # Zwróć znalezione drzewo i koszt całkowity
            return (round(total_cost, 2), mst)

        else:
            raise RuntimeError('Graph does not exist')


if __name__ == '__main__':
    mst = CityGraph()
    mst.create_graph()
    cost, edges = mst.eval_kruskal()
    print('cost', cost)
    print('edges', edges)
