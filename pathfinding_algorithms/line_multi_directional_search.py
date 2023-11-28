from .multi_directional_search import MultiDirectionalSearch


class LineMultiDirectionalSearch(MultiDirectionalSearch):
    def __init__(self, maze):
        super().__init__(maze)
        line_cells = self.get_line_cells()
        self.add_clusters(line_cells)

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

        return cells



