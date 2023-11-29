from .multi_directional_search import MultiDirectionalSearch
import random


class BogoBFSAstarMultiDirectionalSearch(MultiDirectionalSearch):
    def __init__(self, maze):
        super().__init__(maze)
        random_cells = self.get_random_valid_cells(max(self.maze.get_dimensions()) // 10)
        self.add_clusters(random_cells)

    def get_random_valid_cells(self, n, max_attempts=1000):
        valid_cells = []
        attempts = 0

        while len(valid_cells) < n and attempts < max_attempts:
            row = random.randint(0, self.maze.rows - 1)
            col = random.randint(0, self.maze.cols - 1)

            if self.maze.is_valid((row, col)) and self.maze[row][col] == self.maze.PATH:
                if (row, col) not in valid_cells:
                    valid_cells.append((row, col))

            attempts += 1

        return valid_cells


def get_class():
    return BogoBFSAstarMultiDirectionalSearch
