import tkinter as tk
from welcome_screen import WelcomeScreen
from side_panel import SidePanel
from visual_panel import VisualPanel
from event_controller import EventListener


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Visualiser")
        self.adjust_window()
        self.event_listener = EventListener()
        self.welcome_screen = WelcomeScreen(root, self.event_listener)
        self.event_listener.subscribe("welcome_screen_enter_pressed", self.close_welcome_screen)

    def close_welcome_screen(self):
        self.welcome_screen.frame.destroy()
        self.create_frames()
        self.run()

    def adjust_window(self):
        self.root.state("zoomed")

    def create_frames(self):
        self.side_panel_frame = tk.Frame(self.root, width=200, relief="sunken", borderwidth=2)
        self.side_panel_frame.pack(side="left", fill="y")
        self.side_panel = SidePanel(self.side_panel_frame, self.event_listener)

        self.visual_panel_frame = tk.Frame(self.root)
        self.visual_panel_frame.pack(side="right", expand=True, fill="both")
        self.visual_panel = VisualPanel(self.visual_panel_frame, self.event_listener)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.run()
