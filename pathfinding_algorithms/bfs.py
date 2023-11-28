from .abstract_search import AbstractSearch
from collections import deque


class BFS(AbstractSearch):

    def __init__(self, maze):
        super().__init__(maze)
        self.frontier = deque([self.start])

    def solve(self):
        history = []
        while self.frontier:
            current = self.frontier.popleft()
            self.visited.add(current)
            history.append((BFS.COLOR_VISITED, current))

            if current == self.end:
                path = self.reconstruct_path()
                for cell in path:
                    history.append((BFS.COLOR_PATH, cell))
                break

            for neighbor in self.get_neighbors(current):
                if neighbor not in self.visited and neighbor not in self.frontier:
                    self.frontier.append(neighbor)
                    history.append((BFS.COLOR_FRONTIER, neighbor))
                    self.came_from[neighbor] = current

        return history


def get_class():
    return BFS
