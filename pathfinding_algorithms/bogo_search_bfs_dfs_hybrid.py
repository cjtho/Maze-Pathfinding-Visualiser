from .abstract_search import AbstractSearch
import random
from collections import deque


class BogoBFSDFSHybrid(AbstractSearch):

    def __init__(self, maze):
        super().__init__(maze)
        self.frontier = deque([self.start])

    def solve(self):
        history = []
        dfs_bias = 0.1
        bfs_bias = 0.5
        curr_bias = 0
        i = 0
        while self.frontier:
            if i % 25 == 0:
                curr_bias = random.choice([dfs_bias, bfs_bias])
            if random.random() < curr_bias:
                current = self.frontier.popleft()
            else:
                current = self.frontier.pop()
            self.visited.add(current)
            history.append((BogoBFSDFSHybrid.COLOR_VISITED, current))

            if current == self.end:
                self.path = self.reconstruct_path()
                for cell in self.path:
                    history.append((BogoBFSDFSHybrid.COLOR_PATH, cell))
                break

            random.shuffle(self.directions)
            for neighbor in self.get_neighbors(current):
                if neighbor not in self.visited:
                    self.frontier.append(neighbor)
                    history.append((BogoBFSDFSHybrid.COLOR_FRONTIER, neighbor))
                    self.came_from[neighbor] = current

            i += 1

        return history


def get_class():
    return BogoBFSDFSHybrid
