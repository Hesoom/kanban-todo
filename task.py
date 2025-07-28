import tkinter as tk 
from utils import relative_to_assets


class Task():
    def __init__(self, parent_frame, text,move_callback=None , status="todo"):
        self.text = text
        self.status = status
        self.move_callback = move_callback
        self.parent_frame = parent_frame
        self.frame = None

    def render(self):
        self.frame = tk.Frame(self.parent_frame, bg="#292D36")
        self.frame.pack(fill="x", pady=2)

        self.label = tk.Label(
            self.frame,
            text=self.text,
            bg="#292D36",
            fg="white",
            padx=5,
            pady=5,
            anchor="w",
            font=("Inter", 12),
            justify="left",
            wraplength=145,
            width=16
        )
        self.label.pack(side="left", fill="x", expand=True)

        self.move_btn_image = tk.PhotoImage(file=relative_to_assets("arrow_1.png"))
        self.move_btn = tk.Button(
            self.frame,
            image=self.move_btn_image,
            command=self.move,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            activebackground=self.frame["bg"]
        )
        self.move_btn.pack(side='right')
        
        
        self.delete_btn_image = tk.PhotoImage(file=relative_to_assets("delete_1.png"))
        self.delete_btn = tk.Button(
            self.frame,
            image=self.delete_btn_image,
            command=self.delete,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            activebackground=self.frame["bg"]
        )
        self.delete_btn.pack(side='right')

        self.edit_btn_image = tk.PhotoImage(file=relative_to_assets("edit_1.png"))
        self.edit_btn = tk.Button(
            self.frame,
            image=self.edit_btn_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            activebackground=self.frame["bg"]
        )
        self.edit_btn.pack(side='right')


    def delete(self):
        self.frame.destroy()

    def move(self):
        self.move_callback(self)


    def move_to(self, new_parent):
        self.frame.pack_forget()
        self.frame.master = new_parent
        self.frame.pack(...)
