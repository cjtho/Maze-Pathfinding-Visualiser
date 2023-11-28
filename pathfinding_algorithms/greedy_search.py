from .abstract_search import AbstractSearch
import heapq
import numpy as np


class GreedySearch(AbstractSearch):

    def __init__(self, maze):
        super().__init__(maze)
        self.open_set = [(self.heuristic(self.start, self.end), self.start)]

    def heuristic(self, point_a, point_b):
        return self.euclidean_distance(point_a, point_b)

    def solve(self):
        history = []
        while self.open_set:
            _, current = heapq.heappop(self.open_set)
            history.append((GreedySearch.COLOR_VISITED, current))

            if current == self.end:
                path = self.reconstruct_path()
                for cell in path:
                    history.append((GreedySearch.COLOR_PATH, cell))
                break

            for neighbor in self.get_neighbors(current):
                if neighbor not in self.came_from:
                    self.came_from[neighbor] = current
                    heapq.heappush(self.open_set, (self.heuristic(neighbor, self.end), neighbor))
                    history.append((GreedySearch.COLOR_FRONTIER, neighbor))

        return history


def get_class():
    return GreedySearch
