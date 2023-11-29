from .multi_directional_search import MultiDirectionalSearch
from collections import deque

class TriBFSAstarMultiDirectionalSearch(MultiDirectionalSearch):
    def __init__(self, maze):
        super().__init__(maze)
        middle_cell = self.get_manhattan_middle(self.maze.start, self.maze.end)
        path_cell = self.find_valid_path_bfs(middle_cell)

        if path_cell:
            self.add_clusters([path_cell])

    def get_manhattan_middle(self, start, end):
        middle_row = (start[0] + end[0]) // 2
        middle_col = (start[1] + end[1]) // 2
        return middle_row, middle_col

    def find_valid_path_bfs(self, start):
        visited = set()
        queue = deque([start])

        while queue:
            current = queue.popleft()
            if self.maze.is_valid(current) and self.maze[current[0]][current[1]] == self.maze.PATH:
                return current

            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)

        return None

def get_class():
    return TriBFSAstarMultiDirectionalSearch