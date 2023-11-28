from .abstract_search import AbstractSearch
import heapq


class AStar(AbstractSearch):

    def __init__(self, maze):
        super().__init__(maze)
        self.open_set = [(0, self.start)]
        self.g_score = {self.start: 0}
        self.f_score = {self.start: self.heuristic(self.start, self.end)}

    def heuristic(self, point_a, point_b):
        return self.euclidean_distance(point_a, point_b)

    def solve(self):
        history = []
        while self.open_set:
            current_cost, current = heapq.heappop(self.open_set)
            history.append((AStar.COLOR_VISITED, current))

            if current == self.end:
                path = self.reconstruct_path()
                for cell in path:
                    history.append((AStar.COLOR_PATH, cell))
                break

            for neighbor in self.get_neighbors(current):
                tentative_g_score = self.g_score[current] + 1
                if tentative_g_score < self.g_score.get(neighbor, float("inf")):
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, self.end)
                    if neighbor not in [n for _, n in self.open_set]:
                        heapq.heappush(self.open_set, (f_score, neighbor))
                        history.append((AStar.COLOR_FRONTIER, neighbor))

        return history


def get_class():
    return AStar
