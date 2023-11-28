import random


class Maze:
    WALL = "#"
    PATH = " "
    DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def __init__(self, rows, cols, cut_walls_percent=0.2):
        self.rows = rows
        self.cols = cols
        self.cut_walls_percent = cut_walls_percent

        self.maze = None
        self.start = None
        self.end = None

        self.build_maze()
        self.cut_walls(cut_walls_percent)  # makes the maze more interesting

    def get_dimensions(self):
        return self.rows, self.cols

    def find_start_end(self):
        return self.start, self.end

    def is_valid(self, node):
        return 0 <= node[0] < self.rows and 0 <= node[1] < self.cols

    def __getitem__(self, item):
        return self.maze[item]

    def build_maze(self):
        max_attempts = 3
        for _ in range(max_attempts):
            self.generate_maze()
            if self.select_start_end():
                break

    def generate_maze(self):
        self.maze = [[Maze.WALL] * self.cols for _ in range(self.rows)]

        # Start with a random cell
        start_cell = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
        self.maze[start_cell[0]][start_cell[1]] = Maze.PATH
        stack = [start_cell]

        while stack:  # stack-based DFS
            current = stack[-1]
            neighbors = self.find_neighbors(*current)
            if not neighbors:
                stack.pop()
            else:
                next_cell = random.choice(neighbors)
                self.maze[next_cell[0]][next_cell[1]] = Maze.PATH
                self.remove_wall(current, next_cell)
                stack.append(next_cell)

    def find_neighbors(self, x, y):
        neighbors = []
        for dx, dy in self.DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if self.is_valid((nx, ny)) and self.maze[nx][ny] == Maze.WALL:
                neighbors.append((nx, ny))
        return neighbors

    def remove_wall(self, current, next_cell):
        cx, cy = current
        nx, ny = next_cell
        wall_x, wall_y = (cx + nx) // 2, (cy + ny) // 2
        self.maze[wall_x][wall_y] = Maze.PATH

    def select_start_end(self):
        def get_region(x, y, region):
            stack = [(x, y)]

            while stack:
                cx, cy = stack.pop()

                if (cx, cy) in visited:
                    continue

                visited.add((cx, cy))
                region.add((cx, cy))

                for dx, dy in self.DIRECTIONS:
                    nx, ny = cx + dx, cy + dy
                    if self.is_valid((nx, ny)) and self.maze[nx][ny] != Maze.WALL:
                        stack.append((nx, ny))

        def manhattan_distance(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        visited = set()
        largest_region = set()

        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == Maze.WALL or (i, j) in visited:
                    continue
                region = set()
                get_region(i, j, region)
                if len(region) > len(largest_region):
                    largest_region = region

        if not largest_region:
            return None, None  # No valid regions found

        # Determine the maximum Manhattan distance within the region
        max_distance = 0
        for p1 in largest_region:
            for p2 in largest_region:
                max_distance = max(max_distance, manhattan_distance(p1, p2))

        required_distance = 0.5 * max_distance
        self.start, self.end = None, None

        largest_region = list(largest_region)
        random.shuffle(largest_region)

        for p1 in largest_region:
            for p2 in largest_region:
                if manhattan_distance(p1, p2) >= required_distance:
                    self.start, self.end = p1, p2
                    break
            if self.start and self.end:
                break

        return self.start, self.end

    def cut_walls(self, cut_percent=0.2):
        def is_adjacent_to_path(i, j):
            for dx, dy in self.DIRECTIONS:
                if self.is_valid((i + dx, j + dy)):
                    if self.maze[i + dx][j + dy] == self.PATH:
                        return True
            return False

        walls_positions = [(i, j) for i in range(self.rows) for j in range(self.cols)
                           if self.maze[i][j] == self.WALL and is_adjacent_to_path(i, j)]
        num_walls_to_cut = int(cut_percent * len(walls_positions))

        if walls_positions:
            walls_to_cut = random.sample(walls_positions, min(num_walls_to_cut, len(walls_positions)))
            for i, j in walls_to_cut:
                self.maze[i][j] = self.PATH

    def __str__(self):
        message = ""
        for row in self.maze:
            message += " ".join(map(str, row)) + "\n"
        return message
