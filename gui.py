import tkinter as tk
from tkinter import ttk
from pathlib import Path

class KanbanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kanban To-Do")
        self.geometry("1200x750")
        self.configure(bg="#292D36")
        self.resizable(False, False)

        self.assets_path = Path(__file__).parent / "assets" / "frame0"

        self._setup_style()
        self._create_widgets()


    def _relative_to_assets(self, filename):
        return self.assets_path / filename

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Custom.Vertical.TScrollbar",
            gripcount=0,
            background="#161616",
            darkcolor="#292D36",
            lightcolor="#292D36",
            troughcolor="#292D36",
            bordercolor="#292D36",
            arrowcolor="#161616"
        )
        self.style = style

    def _create_widgets(self):
        # Background canvas and image
        self.canvas = tk.Canvas(
            self, bg="#292D36", height=750, width=1200,
            bd=0, highlightthickness=0, relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_1 = tk.PhotoImage(file=self._relative_to_assets("image_1.png"))
        self.canvas.create_image(600, 375, image=self.image_1)

        # Entry field background image
        self.entry_bg_image = tk.PhotoImage(file=self._relative_to_assets("entry_1.png"))
        self.canvas.create_image(220, 644, image=self.entry_bg_image)

        # Task entry widget
        self.task_entry = tk.Entry(
            self, bd=0, bg="#292D36", fg="white",
            font=("Inter", 12), highlightthickness=0
        )
        self.task_entry.place(x=125, y=631, width=170, height=27)

        # Add task button
        self.add_button_image = tk.PhotoImage(file=self._relative_to_assets("button_1.png"))
        self.add_button = tk.Button(
            self, image=self.add_button_image,
            borderwidth=0, highlightthickness=0,
            relief="flat", command=self.add_task
        )
        self.add_button.place(x=300, y=630, width=26, height=26)

        # Scrollable task list area
        self.todo_canvas = tk.Canvas(
            self, bg="#292D36", width=245, height=425,
            highlightthickness=0
        )
        self.todo_canvas.place(x=100, y=160)

        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical",
            command=self.todo_canvas.yview,
            style="Custom.Vertical.TScrollbar"
        )
        self.todo_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.task_list_frame = tk.Frame(self.todo_canvas, bg="#292D36")
        self.todo_canvas.create_window((0, 0), window=self.task_list_frame, anchor="nw")

        self.task_list_frame.bind("<Configure>", self._on_frame_configure)

        # Initial scrollbar visibility
        self._update_scrollbar_visibility()

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            return
        task_label = tk.Label(
            self.task_list_frame,
            text=task_text,
            bg="#292D36",
            fg="white",
            padx=5,
            pady=5,
            anchor="w",
            font=("Inter", 12),
            justify="left",
            wraplength=200
        )
        task_label.pack(fill="x", pady=2)
        self.task_entry.delete(0, tk.END)
        self.todo_canvas.update_idletasks()
        self._update_scrollbar_visibility()

    def _on_frame_configure(self, event=None):
        self.todo_canvas.configure(scrollregion=self.todo_canvas.bbox("all"))
        self._update_scrollbar_visibility()

    def _update_scrollbar_visibility(self, event=None):
        canvas_height = self.todo_canvas.winfo_height()
        bbox = self.todo_canvas.bbox("all")
        content_height = bbox[3] if bbox else 0

        if content_height <= canvas_height:
            self.scrollbar.place_forget()
        else:
            self.scrollbar.place(x=335, y=180, height=375)

if __name__ == "__main__":
    app = KanbanApp()
    app.mainloop()
