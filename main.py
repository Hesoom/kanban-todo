import tkinter as tk
from tkinter import ttk
from pathlib import Path
from task import Task 
from utils import relative_to_assets
import sqlite3

conn = sqlite3.connect("task.db")
c = conn.cursor()

# c.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, text text, status text)")

conn.commit()
# conn.close()

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
        self.render_tasks()


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

    def render_tasks(self):
        c.execute("SELECT * FROM tasks")
        all_tasks = c.fetchall()
        if all_tasks:
            for tt in all_tasks:
                
                task_id = tt[0]
                task_text = tt[1]
                task_status = tt[2]

                task_list_frame = getattr(self, f"{task_status}_task_list_frame")
                task = Task(task_list_frame, text=task_text,id=task_id)
                task.move_callback = lambda t=task: self.move_task(t, self.todo_tasks, self.doing_tasks, self.done_tasks)
                task.delete_callback = lambda t=task: self.delete_task(t, self.todo_tasks, self.doing_tasks, self.done_tasks)
                if task_status == "todo":
                    self.todo_tasks.append(task)
                elif task_status == "doing":
                    self.doing_tasks.append(task)
                elif task_status == "done":
                    self.done_tasks.append(task)

                task.render(status=task_status)


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

        self.task_entry.bind("<Return>", lambda e: self.add_task())

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

        self.todo_task_list_frame = tk.Frame(self.todo_canvas, bg="#292D36")
        self.todo_canvas.create_window((0, 0), window=self.todo_task_list_frame, anchor="nw")

        self.todo_task_list_frame.bind("<Configure>", self._on_todo_configure)

        

        # === Doing canvas ===
        self.doing_canvas = tk.Canvas(
            self, bg="#292D36", width=245, height=480,
            highlightthickness=0
        )
        self.doing_canvas.place(x=475, y=160)

        self.doing_scrollbar = ttk.Scrollbar(
            self, orient="vertical",
            command=self.doing_canvas.yview,
            style="Custom.Vertical.TScrollbar"
        )
        self.doing_canvas.configure(yscrollcommand=self.doing_scrollbar.set)

        self.doing_task_list_frame = tk.Frame(self.doing_canvas, bg="#292D36")
        self.doing_canvas.create_window((0, 0), window=self.doing_task_list_frame, anchor="nw")

        self.doing_task_list_frame.bind("<Configure>", self._on_doing_frame_configure)

        # === Done canvas ===
        self.done_canvas = tk.Canvas(
            self, bg="#292D36", width=245, height=480,
            highlightthickness=0
        )
        self.done_canvas.place(x=855, y=160)

        self.done_scrollbar = ttk.Scrollbar(
            self, orient="vertical",
            command=self.done_canvas.yview,
            style="Custom.Vertical.TScrollbar"
        )
        self.done_canvas.configure(yscrollcommand=self.done_scrollbar.set)

        self.done_task_list_frame = tk.Frame(self.done_canvas, bg="#292D36")
        self.done_canvas.create_window((0, 0), window=self.done_task_list_frame, anchor="nw")

        self.done_task_list_frame.bind("<Configure>", self._on_done_frame_configure)

        # Initial scrollbar visibility
        self._update_scrollbar_visibility()

        

    def insert_task(self, task):
        with conn:
            c.execute("INSERT INTO tasks (text, status) VALUES (?, ?)", (task.text, task.status))
            task.id = c.lastrowid


    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            return

        task = Task(self.todo_task_list_frame, text=task_text)
        task.move_callback = lambda t=task: self.move_task(t, self.todo_tasks, self.doing_tasks, self.done_tasks)
        task.delete_callback = lambda t=task: self.delete_task(t, self.todo_tasks, self.doing_tasks, self.done_tasks)

        task.render(status=task.status)
        self.todo_tasks.append(task)
        self.insert_task(task)

        self.task_entry.delete(0, tk.END)
        self.todo_canvas.update_idletasks()
        self._update_scrollbar_visibility()

    def _on_doing_frame_configure(self, event=None):    
        self.doing_canvas.configure(scrollregion=self.doing_canvas.bbox("all"))
        self._update_scrollbar_visibility()


    def _on_done_frame_configure(self, event=None):
        self.done_canvas.configure(scrollregion=self.done_canvas.bbox("all"))
        self._update_scrollbar_visibility()

    def _on_todo_configure(self, event=None):
        self.todo_canvas.configure(scrollregion=self.todo_canvas.bbox("all"))
        self._update_scrollbar_visibility()

    def _update_scrollbar_visibility(self, event=None):
        # To-Do
        todo_height = self.todo_canvas.winfo_height()
        todo_bbox = self.todo_canvas.bbox("all")
        todo_content = todo_bbox[3] if todo_bbox else 0

        if todo_content <= todo_height:
            self.scrollbar.place_forget()
        else:
            self.scrollbar.place(x=350, y=180, height=375)

        # Doing
        doing_height = self.doing_canvas.winfo_height()
        doing_bbox = self.doing_canvas.bbox("all")
        doing_content = doing_bbox[3] if doing_bbox else 0

        if doing_content <= doing_height:
            self.doing_scrollbar.place_forget()
        else:
            self.doing_scrollbar.place(x=725, y=180, height=420)

        # Done
        done_height = self.done_canvas.winfo_height()
        done_bbox = self.done_canvas.bbox("all")
        done_content = done_bbox[3] if done_bbox else 0

        if done_content <= done_height:
            self.done_scrollbar.place_forget()
        else:
            self.done_scrollbar.place(x=1105, y=180, height=420)

    def move_task(self, task, todo, doing, done):
        if task in todo:
            todo.remove(task)
            doing.append(task)
            task.status = "doing"
            with conn:
                c.execute("UPDATE tasks SET status = (?) WHERE id = (?)",("doing",task.id))
            task.move_to(self.doing_task_list_frame)

        elif task in doing:
            doing.remove(task)
            done.append(task)
            task.status = "done"
            with conn:
                c.execute("UPDATE tasks SET status = (?) WHERE id = (?)",("done",task.id))
            task.move_to(self.done_task_list_frame)

    def delete_task(self, task, todo, doing, done):
        if task in todo:
            todo.remove(task)
            with conn:
                c.execute("DELETE FROM tasks WHERE id = (?)",(task.id,))
        if task in doing:
            doing.remove(task)
            with conn:
                c.execute("DELETE FROM tasks WHERE id = (?)",(task.id,))
        if task in done:
            done.remove(task)
            with conn:
                c.execute("DELETE FROM tasks WHERE id = (?)",(task.id,))


if __name__ == "__main__":
    app = KanbanApp()
    app.mainloop()
