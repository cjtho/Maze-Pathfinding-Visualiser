from .abstract_search import AbstractSearch


class BidirectionalSearch(AbstractSearch):

    def __init__(self, maze):
        super().__init__(maze)
        self.open_set_start = [self.start]
        self.open_set_end = [self.end]
        self.came_from_start = {self.start: None}
        self.came_from_end = {self.end: None}
        self.intersection = None

    def solve(self):
        history = []
        while self.open_set_start and self.open_set_end:
            current_start = self.open_set_start.pop(0)
            history.append((BidirectionalSearch.COLOR_VISITED, current_start))

            if current_start in self.open_set_end:
                self.intersection = current_start
                break

            for neighbor in self.get_neighbors(current_start):
                if neighbor not in self.came_from_start:
                    self.came_from_start[neighbor] = current_start
                    self.open_set_start.append(neighbor)
                    history.append((BidirectionalSearch.COLOR_FRONTIER, neighbor))

            current_end = self.open_set_end.pop(0)
            history.append((BidirectionalSearch.COLOR_VISITED, current_end))

            if current_end in self.open_set_start:
                self.intersection = current_end
                break

            for neighbor in self.get_neighbors(current_end):
                if neighbor not in self.came_from_end:
                    self.came_from_end[neighbor] = current_end
                    self.open_set_end.append(neighbor)
                    history.append((BidirectionalSearch.COLOR_FRONTIER, neighbor))

        if self.intersection is not None:
            path = self.reconstruct_path()
            for cell in path:
                history.append((BidirectionalSearch.COLOR_PATH, cell))

        return history

    def reconstruct_path(self):
        path = []
        current = self.intersection
        while current != self.start:
            path.append(current)
            current = self.came_from_start[current]
        path.append(self.start)

        path_end = []
        current = self.intersection
        while current != self.end:
            path_end.append(current)
            current = self.came_from_end[current]
        path_end.append(self.end)

        final_path = [item for pair in zip(path[::-1], path_end[::-1]) for item in pair]
        return final_path


def get_class():
    return BidirectionalSearch
