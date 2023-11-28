from .abstract_search import AbstractSearch
import copy

class IterativeDeepeningDFS(AbstractSearch):
    COLOR_1 = AbstractSearch.COLOR_FRONTIER
    COLOR_2 = AbstractSearch.COLOR_VISITED

    def __init__(self, maze):
        super().__init__(maze)
        self.colour = IterativeDeepeningDFS.COLOR_1

    def solve(self):
        depth = 0
        history = ["DEPTH"]  # for separating each depth in the history
        while True:
            self.visited = set()
            self.came_from = {self.start: None}

            if self.depth_limited_search(self.start, depth, history):
                self.remove_depth_markers(history)
                return history

            depth += 1
            self.colour_switch()
            history.append("DEPTH")

    def colour_switch(self):
        if self.colour == IterativeDeepeningDFS.COLOR_1:
            self.colour = IterativeDeepeningDFS.COLOR_2
        else:
            self.colour = IterativeDeepeningDFS.COLOR_1

    @staticmethod
    def remove_depth_markers(history):
        history[:] = [item for item in history if item != "DEPTH"]

    def depth_limited_search(self, node, limit, history):
        stack = [(node, 0)]  # Stack of (node, current_depth)
        while stack:
            current_node, current_depth = stack.pop()
            history.append((self.colour, current_node))

            if current_node == self.end:
                self.add_path_to_history(history)
                return True

            if current_depth <= limit:
                self.visited.add(current_node)
                for neighbor in self.get_neighbors(current_node):
                    if neighbor not in self.visited:
                        self.came_from[neighbor] = current_node
                        stack.append((neighbor, current_depth + 1))

        return False

    def add_path_to_history(self, history):
        path = self.reconstruct_path()
        for cell in path:
            history.append((IterativeDeepeningDFS.COLOR_PATH, cell))

def get_class():
    return IterativeDeepeningDFS
