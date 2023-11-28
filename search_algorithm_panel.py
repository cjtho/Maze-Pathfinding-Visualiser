import math
import tkinter as tk


class SearchAlgorithmPanel:
    def __init__(self, frame, algorithm):
        self.frame = frame
        self.algorithm = algorithm
        self.history = []

        self.title_frame = tk.Frame(self.frame)
        self.maze_frame = tk.Frame(self.frame, bg="gray99")

        self.create_title_frame()

        self.title_frame.pack(side="top", fill="x")
        self.maze_frame.pack(side="top", fill="both", expand=True)

        self.frame.after(100, self.render_maze)
        self.frame.after(100, self.solve_maze)
        self.i = 0

    def is_finished(self):
        return not (self.i < len(self.history))

    def create_title_frame(self):
        algorithm_class_name = self.algorithm.__class__.__name__
        title_label = tk.Label(self.title_frame, text=algorithm_class_name)
        title_label.pack()

    def render_maze(self):
        self.maze_drawer = MazeDrawer(self.algorithm.maze, self.maze_frame)
        self.maze_drawer.draw_maze()

    def solve_maze(self):
        self.history = self.algorithm.solve()

    def update(self, speed):
        end_index = min(len(self.history), self.i + speed)
        latest_cells = {}

        for cell in self.history[self.i: end_index]:
            _, coords = cell
            latest_cells[coords] = cell

        self.i += speed
        for cell in latest_cells.values():
            self.maze_drawer.update_cell(cell)


class MazeDrawer:
    def __init__(self, maze, frame):
        self.maze = maze
        self.frame = frame
        self.cell_size_x, self.cell_size_y = self.determine_cell_size()
        self.rows, self.cols = maze.get_dimensions()
        self.canvas = tk.Canvas(self.frame,
                                width=self.cols * self.cell_size_x,
                                height=self.rows * self.cell_size_y)
        self.canvas.pack()
        self.rectangles = [[None] * self.cols for _ in range(self.rows)]

    def determine_cell_size(self):
        cell_ratio_tolerance = 3
        frame_width, frame_height = self.frame.winfo_width(), self.frame.winfo_height()
        rows, cols = self.maze.get_dimensions()

        initial_cell_size_x = frame_width / cols
        initial_cell_size_y = frame_height / rows

        if initial_cell_size_x < initial_cell_size_y:
            if initial_cell_size_x * cell_ratio_tolerance < initial_cell_size_y:
                cell_size_x = initial_cell_size_x
                cell_size_y = min(initial_cell_size_y, initial_cell_size_x * cell_ratio_tolerance)
            else:
                cell_size_x = initial_cell_size_x
                cell_size_y = initial_cell_size_y
        else:
            if initial_cell_size_y * cell_ratio_tolerance < initial_cell_size_x:
                cell_size_y = initial_cell_size_y
                cell_size_x = min(initial_cell_size_x, initial_cell_size_y * cell_ratio_tolerance)
            else:
                cell_size_x = initial_cell_size_x
                cell_size_y = initial_cell_size_y

        # shhhhhh you don't see anything here
        cell_size_x = math.floor(cell_size_x)
        cell_size_y = math.floor(cell_size_y)
        return cell_size_x, cell_size_y

    def draw_maze(self):
        def draw_cell(row, col, color):
            x1 = col * self.cell_size_x
            y1 = row * self.cell_size_y
            x2 = x1 + self.cell_size_x
            y2 = y1 + self.cell_size_y
            rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            self.rectangles[row][col] = rect_id

        # draw the maze cells
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row][col] == self.maze.WALL:
                    cell_color = "black"
                else:
                    cell_color = "white"
                draw_cell(row, col, cell_color)

        # draw start and end points
        start, end = self.maze.find_start_end()
        if start:
            draw_cell(*start, "blue")
        if end:
            draw_cell(*end, "red")

    def update_cell(self, info):
        colour, (row, col) = info
        if (row, col) not in self.maze.find_start_end():
            rect_id = self.rectangles[row][col]
            self.canvas.itemconfig(rect_id, fill=colour)
