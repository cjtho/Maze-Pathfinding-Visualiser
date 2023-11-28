import tkinter as tk


class WelcomeScreen:
    def __init__(self, master, event_listener):
        self.master = master
        self.event_listener = event_listener

        self.frame = tk.Frame(self.master, background="white")
        self.frame.pack(fill="both", expand=True)

        self.label = tk.Label(self.frame, text="Welcome",
                              font=("Helvetica", 20), bg="white", fg=self.get_color(1))
        self.label.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame.after(250, self.fade_in)

    def fade_in(self, alpha=1):
        if alpha > 0:
            alpha -= 0.01
            self.label.config(fg=self.get_color(alpha))
            self.master.after(16, lambda: self.fade_in(alpha))
        else:
            self.animate_title()

    def animate_title(self, current_font_size=20, size_increment=1):
        max_font_size = 100000

        if current_font_size < max_font_size:
            current_font_size += size_increment

            if current_font_size % 3 == 0:
                size_increment *= 2

            transition_threshold = max_font_size / 10
            alpha = min(1.0, current_font_size / transition_threshold) ** 0.2
            self.label.config(fg=self.get_color(alpha), font=("Helvetica", int(current_font_size)))
            self.master.after(16, lambda: self.animate_title(current_font_size, size_increment))
        else:
            self.event_listener.notify("welcome_screen_enter_pressed")

    def get_color(self, alpha):
        alpha_value = int(alpha * 255)
        return f"#{alpha_value:02x}{alpha_value:02x}{alpha_value:02x}"
