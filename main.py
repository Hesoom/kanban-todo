import tkinter as tk
from tkinter import ttk
from pathlib import Path
from task import Task 
from utils import relative_to_assets


class KanbanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kanban To-Do")
        self.geometry("1200x750")
        self.configure(bg="#292D36")
        self.resizable(False, False)

        self.todo_tasks = []
        self.doing_tasks = []
        self.done_tasks = []

        self._setup_style()
        self._create_widgets()



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

        self.image_1 = tk.PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(600, 375, image=self.image_1)

        # Entry field background image
        self.entry_bg_image = tk.PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(220, 644, image=self.entry_bg_image)

        # Task entry widget
        self.task_entry = tk.Entry(
            self, bd=0, bg="#292D36", fg="white",
            font=("Inter", 12), highlightthickness=0
        )
        self.task_entry.place(x=125, y=631, width=170, height=27)

        # Add task button
        self.add_button_image = tk.PhotoImage(file=relative_to_assets("button_1.png"))
        self.add_button = tk.Button(
            self, image=self.add_button_image,
            borderwidth=0, highlightthickness=0,
            relief="flat", command=self.add_task
        )
        self.add_button.place(x=300, y=630, width=26, height=26)

        # === To Do canvas ===
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

        task = Task(self.task_list_frame, text=task_text)
        task.move_callback = lambda t=task: self.move_task(t, self.todo_tasks, self.doing_tasks, self.done_tasks)

        self.todo_tasks.append(task)
        task.render() 
        print(self.todo_tasks)
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

    def move_task(self, task, todo, doing, done):
        if task in todo:
            print("in todo")
            todo.remove(task)
            doing.append(task)
            task.current_list = "doing"
            task.move_to(self.doing_frame)
        elif task in doing:
            doing.remove(task)
            done.append(task)
            task.current_list = "done"
            task.move_to(self.done_frame)

if __name__ == "__main__":
    app = KanbanApp()
    app.mainloop()
