import importlib
import os
from tkinter import ttk
import tkinter as tk


class SidePanel:
    def __init__(self, frame, event_listener):
        self.frame = frame
        self.event_listener = event_listener
        self.checkboxes = []
        self.checkbox_vars = []

        # initialize variables for sliders
        self.rows_var = tk.IntVar()
        self.cols_var = tk.IntVar()
        self.speed_var = tk.IntVar()
        self.walls_var = tk.DoubleVar()

        self.font = ("Helvetica", 16)
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", font=self.font)

        self.construct()

    def construct(self):
        self.create_title_frame()
        self.create_checkboxes_frame()
        self.create_sliders_frame()
        self.create_start_button()

    def create_title_frame(self):
        title_frame = tk.Frame(self.frame, bg="gray99")
        title_frame.pack(side="top", fill="x", pady=(0, 10))

        title_label = tk.Label(title_frame, text="Select Search Algorithm(s)", font=self.font, bg="gray99")
        title_label.pack(side="top")

    def create_checkboxes_frame(self):
        canvas_width = 300
        canvas = tk.Canvas(self.frame, width=canvas_width)
        list_frame = tk.Frame(canvas)

        canvas.create_window((0, 0), window=list_frame, anchor="nw")

        self.search_algorithms = self.load_modules_from_folder("pathfinding_algorithms")
        for name, algorithm in self.search_algorithms.items():
            var = tk.IntVar()
            checkbox = tk.Checkbutton(list_frame, text=algorithm["module"].get_class().__name__,
                                      variable=var, font=self.font)
            checkbox.pack(anchor="w")
            self.checkboxes.append((name, checkbox))
            self.checkbox_vars.append(var)

        canvas.pack(side="top", fill="both", expand=True)

    def create_sliders_frame(self):
        sliders_frame = tk.Frame(self.frame)
        sliders_frame.pack(side="top", fill="x", pady=10)

        self.create_slider(sliders_frame, "Rows", 10, 100, self.rows_var)
        self.create_slider(sliders_frame, "Cols", 10, 100, self.cols_var)
        self.create_slider(sliders_frame, "Speed", 1, 10, self.speed_var)
        self.create_slider(sliders_frame, "Walls", 0, 1.0, self.walls_var)

    def create_slider(self, parent_frame, label, from_, to, variable):
        variable.set(from_)

        resolution = 0.01 if isinstance(variable, tk.DoubleVar) else 1

        # container frame for each slider and its labels
        slider_container = tk.Frame(parent_frame)
        slider_container.pack(side="top", fill="x", padx=10)

        # title label on the left
        title_label = tk.Label(slider_container, text=label, font=self.font, anchor="w")
        title_label.pack(side="left")

        # slider
        slider = tk.Scale(slider_container, from_=from_, to=to, orient="horizontal", variable=variable,
                          resolution=resolution)
        slider.pack(side="top", fill="x", expand=True)

    def create_start_button(self):
        button = ttk.Button(self.frame, text="START", style="Custom.TButton", command=self.on_button_pressed)
        button.pack(side="bottom", fill="x", padx=5, pady=5)

    @staticmethod
    def load_modules_from_folder(folder_path):
        modules = {}
        package_name = "pathfinding_algorithms"

        for filename in os.listdir(folder_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                module_full_path = f"{package_name}.{module_name}"
                module = importlib.import_module(module_full_path)
                try:
                    module.get_class()
                except AttributeError:
                    continue
                modules[module_name] = {"module": module}

        return modules

    def on_button_pressed(self):
        checked_algorithms = [name
                              for (name, _), var in zip(self.checkboxes, self.checkbox_vars)
                              if var.get() == 1]
        if not checked_algorithms:
            return
        checked_modules = {x: self.search_algorithms[x] for x in checked_algorithms}

        # collect slider values
        slider_values = {
            "rows": self.rows_var.get(),
            "cols": self.cols_var.get(),
            "speed": self.speed_var.get(),
            "walls": 1 - self.walls_var.get(),
        }

        data = {
            "algorithms": checked_modules,
            "settings": slider_values
        }

        self.event_listener.notify("begin_visuals_button_pressed", data)
