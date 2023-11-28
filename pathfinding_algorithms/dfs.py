from .abstract_search import AbstractSearch


class DFS(AbstractSearch):

    def __init__(self, maze):
        super().__init__(maze)
        self.frontier = [self.start]  # explicitly DFS

    def solve(self):
        history = []
        while self.frontier:
            current = self.frontier.pop()
            self.visited.add(current)
            history.append((DFS.COLOR_VISITED, current))

            if current == self.end:
                self.path = self.reconstruct_path()
                for cell in self.path:
                    history.append((DFS.COLOR_PATH, cell))
                break

            for neighbor in self.get_neighbors(current):
                if neighbor not in self.visited:
                    self.frontier.append(neighbor)
                    history.append((DFS.COLOR_FRONTIER, neighbor))
                    self.came_from[neighbor] = current

        return history


def get_class():
    return DFS
