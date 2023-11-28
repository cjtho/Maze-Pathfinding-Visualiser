import copy
import math
import tkinter as tk
from maze import Maze
from search_algorithm_panel import SearchAlgorithmPanel


class VisualPanel:
    def __init__(self, parent, event_listener):
        self.parent = parent
        self.initialize_frame()
        self.panels = []
        self.event_listener = event_listener
        self.event_listener.subscribe("begin_visuals_button_pressed", self.button_pressed)

    def initialize_frame(self):
        self.frame = tk.Frame(self.parent)
        self.frame.pack(side="top", expand=True, fill=tk.BOTH)

    def reset_frame(self):
        self.frame.destroy()
        self.panels.clear()
        self.initialize_frame()

    def button_pressed(self, data):
        self.speed = data["settings"]["speed"]

        self.reset_frame()
        self.create_panels(data)

        # gives time to settle the graphs
        current_load = (len(data["algorithms"]) * data["settings"]["rows"] *
                        data["settings"]["cols"] * data["settings"]["speed"])
        maximum_load = 100 * 100 * 100 * 9  # yes, this has to be manually updated, fix later
        fraction_of_maximum_load = math.sqrt(current_load / maximum_load)
        least_time_to_wait = 1000
        most_time_to_wait = 10_000
        time_to_wait = int(least_time_to_wait + (most_time_to_wait - least_time_to_wait) * fraction_of_maximum_load)
        self.frame.after(time_to_wait, self.run)

    def create_panels(self, data):
        walls = data["settings"]["walls"]
        maze_rows = data["settings"]["rows"]
        maze_cols = data["settings"]["cols"]
        maze = Maze(maze_rows, maze_cols, cut_walls_percent=walls)

        num_panels = len(data["algorithms"])
        rows = cols = int(num_panels ** 0.5)
        if rows * cols < num_panels:
            rows += 1

        for i, (name, data) in enumerate(data["algorithms"].items()):
            row, col = divmod(i, cols)
            frame = self.create_panel_frame(row, col)

            module = data["module"]
            class_ = module.get_class()
            instantiated_algorithm = class_(copy.deepcopy(maze))

            sap = SearchAlgorithmPanel(frame, instantiated_algorithm)
            self.panels.append(sap)

    def create_panel_frame(self, row, col):
        frame = tk.Frame(self.frame)
        frame.grid(row=row, column=col, sticky="nsew")
        self.frame.grid_rowconfigure(row, weight=1)
        self.frame.grid_columnconfigure(col, weight=1)
        return frame

    def run(self):
        if not self.panels:
            return
        for panel in self.panels:
            panel.update(self.speed)
            if panel.is_finished():
                self.panels.remove(panel)
        self.frame.after(16, self.run)  # 60 fps
