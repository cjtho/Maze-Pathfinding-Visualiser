import numpy as np
from abc import ABC, abstractmethod


class AbstractSearch(ABC):
    COLOR_FRONTIER = "green"
    COLOR_VISITED = "DarkOliveGreen1"
    COLOR_PATH = "gold"

    def __init__(self, maze):
        self.maze = maze
        self.start, self.end = maze.find_start_end()
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.visited = set()
        self.path = []
        self.came_from = {self.start: None}
        self.open_set = [self.start]
        self.modify_directions()

    def modify_directions(self):
        """Biases the directions towards the goal."""

        start_x, start_y = self.start
        direction_distances = []

        for dx, dy in self.directions:
            neighbor = (start_x + dx, start_y + dy)
            distance = self.manhattan_distance(neighbor, self.end)
            direction_distances.append((distance, (dx, dy)))

        direction_distances.sort(key=lambda x: x[0], reverse=True)
        self.directions = [direction[1] for direction in direction_distances]

    @abstractmethod
    def solve(self):
        pass

    def get_neighbors(self, node):
        neighbors = []
        x, y = node
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.maze.rows and 0 <= ny < self.maze.cols and self.maze[nx][ny] != self.maze.WALL:
                neighbors.append((nx, ny))
        return neighbors

    def reconstruct_path(self):
        path = []
        current = self.end
        while current != self.start:
            path.append(current)
            current = self.came_from[current]
        path.append(self.start)
        return path[::-1]

    @staticmethod
    def manhattan_distance(point_a, point_b):
        ax, ay = point_a
        bx, by = point_b
        return abs(ax - bx) + abs(ay - by)

    @staticmethod
    def euclidean_distance(point_a, point_b):
        return np.linalg.norm(np.array(point_a) - np.array(point_b))
