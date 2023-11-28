from .abstract_search import AbstractSearch
from collections import deque


class MultiDirectionalSearch(AbstractSearch):
    def __init__(self, maze):
        super().__init__(maze)
        self.history = []
        self.idx = 1

        self.clusters = {
            "start": {
                "frontier": deque([self.start]), "visited": set()
            },
            "end": {
                "frontier": deque([self.end]), "visited": set()
            }
        }

        self.distances_to_end = {self.end: 0}


    def add_additional_cells(self, cells):
        for cell in cells:
            cluster_name = f"cluster_{self.idx}"
            self.idx += 1
            self.clusters[cluster_name] = {
                "frontier": deque([cell]), "visited": set()
            }

    def solve(self):
        while not self.start_end_met():
            for cluster_1 in self.clusters:
                a = False
                data_1 = self.clusters[cluster_1]
                frontier_1 = data_1["frontier"]
                visited_1 = data_1["visited"]

                if frontier_1:
                    current = frontier_1.popleft()
                    visited_1.add(current)

                    for cluster_2 in self.clusters:
                        if cluster_1 != cluster_2:
                            data_2 = self.clusters[cluster_2]
                            frontier_2 = data_2
                            visited_2 = data_2["visited"]

                            if current in visited_2:
                                # merge cluster1 and cluster2
                                cluster_name = f"cluster_{self.idx}"
                                self.idx += 1
                                self.clusters[cluster_name] = {
                                    "frontier": frontier_1 + frontier_2, "visited": visited_1 | visited_2,
                                }
                                self.clusters.pop(cluster_1)
                                self.clusters.pop(cluster_2)
                                a = True
                                break

                if a is True:
                    break


            return

    def start_end_met(self):
        return self.start in self.distances_to_end


class LineMultiDirectionalSearch(MultiDirectionalSearch):
    def __init__(self, maze):
        super().__init__(maze)
        line_cells = self.get_line_cells()
        self.add_additional_cells(line_cells)

    def get_line_cells(self):
        # Bresenham's line algorithm
        cells = []
        x0, y0 = self.start
        x1, y1 = self.end
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        err = dx - dy

        while True:
            if self.maze.is_valid((x, y)) and self.maze[x][y] == self.maze.PATH:
                cells.append((x, y))
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

        cells = set(cells)
        cells.remove(self.start)
        cells.remove(self.end)
        cells = list(cells)
        return cells


def _get_class():
    return LineMultiDirectionalSearch
