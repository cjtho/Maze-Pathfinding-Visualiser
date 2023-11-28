from .abstract_search import AbstractSearch


class HeuristicDFS(AbstractSearch):

    def __init__(self, maze):
        super().__init__(maze)

    def solve(self):
        history = []
        while self.open_set:
            current = self.open_set.pop()
            self.visited.add(current)
            history.append((HeuristicDFS.COLOR_VISITED, current))

            if current == self.end:
                self.path = self.reconstruct_path()
                for cell in self.path:
                    history.append((HeuristicDFS.COLOR_PATH, cell))
                break

            neighbours = self.get_neighbors(current)
            neighbours.sort(key=lambda neighbour: self.euclidean_distance(neighbour, self.end), reverse=True)
            for neighbor in neighbours:
                if neighbor not in self.visited:
                    self.open_set.append(neighbor)
                    history.append((HeuristicDFS.COLOR_FRONTIER, neighbor))
                    self.came_from[neighbor] = current

        return history


def get_class():
    return HeuristicDFS
