from .abstract_search import AbstractSearch

import random


class BogoSearch(AbstractSearch):

    def __init__(self, maze):
        super().__init__(maze)

    def solve(self):
        history = []
        while self.open_set:
            current = self.open_set.pop()
            self.visited.add(current)
            history.append((BogoSearch.COLOR_VISITED, current))

            if current == self.end:
                self.path = self.reconstruct_path()
                for cell in self.path:
                    history.append((BogoSearch.COLOR_PATH, cell))
                break

            neighbours = self.get_neighbors(current)
            random.shuffle(neighbours)
            for neighbor in neighbours:
                if neighbor not in self.visited:
                    self.open_set.append(neighbor)
                    history.append((BogoSearch.COLOR_FRONTIER, neighbor))
                    self.came_from[neighbor] = current

        return history


def get_class():
    return BogoSearch
