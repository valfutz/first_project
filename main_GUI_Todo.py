import json
import tkinter as tk
from datetime import datetime, timedelta
from os import path
from tkinter import filedialog, messagebox

import customtkinter as ctk


class TodoListApp(ctk.CTk):

    # ctk.set_appearance_mode("system")  # default
    # ctk.set_appearance_mode("dark")
    ctk.set_appearance_mode("light")

    ctk.set_default_color_theme("blue")  # default
    # ctk.set_default_color_theme("green")
    # ctk.set_default_color_theme("dark-blue")

    def __init__(self):
        super().__init__()

        self.tasks = []

        self.title("TodoList - Шлях до Python розробника")
        self.geometry("1000x700")
        self.font = ctk.CTkFont(family="Helvetica", size=18)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(5, weight=1)

        self.open_file_button = ctk.CTkButton(self, text="Open file", font=self.font, command=self.load_task)
        self.open_file_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10, ipadx=40, ipady=10, sticky='ew')

        self.open_file_entry = ctk.CTkEntry(self, width=480, placeholder_text='File path', font=self.font)
        self.open_file_entry.grid(row=0, column=2, columnspan=2, padx=10, pady=10, ipady=10, sticky='ew')

        self.change_deadline_button = ctk.CTkButton(self, text="Choose deadline",
                                                    font=self.font, command=self.choose_deadline)
        self.change_deadline_button.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky='ew')

        self.choose_deadline_button = ctk.CTkButton(self, text="Change deadline", font=self.font,
                                                    command=self.change_deadline)
        self.choose_deadline_button.grid(row=1, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky='ew')

        self.deadline_entry = ctk.CTkEntry(self, width=500, placeholder_text='Deadline', font=self.font)
        self.deadline_entry.grid(row=1, column=2, columnspan=2, padx=10, pady=10, ipady=10, sticky='ew')

        self.add_button = ctk.CTkButton(self, text="Add", font=self.font, command=self.add_task)
        self.add_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, ipadx=40, ipady=10, sticky='ew')

        self.check_var = ctk.IntVar()
        self.checkbox_subtask = ctk.CTkCheckBox(self, width=50, text="SubTask", font=self.font, variable=self.check_var)
        self.checkbox_subtask.grid(row=2, column=3, padx=6, pady=6)

        self.task_entry = ctk.CTkEntry(self, width=40, font=self.font)
        self.task_entry.grid(row=3, column=0, columnspan=4, padx=10, pady=0, ipady=0, sticky='ew')

        self.task_listbox = tk.Listbox(self, width=50, height=20, font=self.font)
        self.task_listbox.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        self.delete_button = ctk.CTkButton(self, text="Delete", font=self.font, command=self.delete_task)
        self.delete_button.grid(row=5, column=0, padx=10, pady=10, ipadx=40, ipady=10, sticky='sw')

        self.clear_button = ctk.CTkButton(self, width=500, text="Clear all", font=self.font, command=self.clear_all)
        self.clear_button.grid(row=5, column=1, columnspan=2, padx=10, pady=10, ipady=10, sticky='ew')

        self.complete_button = ctk.CTkButton(self, text="Done", font=self.font, command=self.mark_as_done)
        self.complete_button.grid(row=5, column=3, padx=10, pady=10, ipadx=40, ipady=10, sticky='se')

    def load_task(self):
        self.open_file_entry.delete(0, ctk.END)
        filepath = filedialog.askopenfilename()
        self.open_file_entry.insert(ctk.END, filepath)
        if filepath != "":
            with open(filepath, "r") as f:
                self.tasks = json.load(f)
            self.task_listbox.delete(0, tk.END)
            self.display_tasks()
        else:
            self.tasks = []

    def save_tasks(self):
        filename = path.basename(self.open_file_entry.get())
        with open(filename, 'w') as file:
            json.dump(self.tasks, file, indent=2)

    def add_task(self):
        deadline = self.deadline_data()
        task = self.task_entry.get()
        if task and self.check_var.get() == 0:
            self.tasks.append({'task': task, 'done': False, 'deadline': deadline, 'subtasks': []})
        elif task and self.check_var.get() == 1:
            if self.selected()[4:6].isdecimal():
                self.tasks[int(self.selected()[4:6]) - 1]['subtasks'].append({'subtask': task})
            else:
                self.tasks[int(self.selected()[4]) - 1]['subtasks'].append({'subtask': task})
        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        self.task_listbox.delete(0, tk.END)
        self.display_tasks()

    @staticmethod
    def deadline_data():
        now = datetime.now()
        three_days = timedelta(3)
        in_three_days = str((now + three_days).strftime("%d.%m.%y %I:%M"))
        return in_three_days

    def delete_task(self):
        if len(self.task_listbox.get(0, tk.END)) == 1:
            self.tasks = []
        elif self.selected()[4].isdecimal():
            del self.tasks[int(self.selected()[4]) - 1]
            messagebox.showinfo("Deleted", "Task deleted.")
        elif self.selected()[10].isdecimal():
            del self.tasks[int(self.selected()[8]) - 1]['subtasks'][int(self.selected()[10]) - 1]
            messagebox.showinfo("Deleted", "Subtask deleted.")
        else:
            del self.tasks[int(self.selected()[8:10]) - 1]['subtasks'][int(self.selected()[11]) - 1]
            messagebox.showinfo("Deleted", "Subtask deleted.")
        self.save_tasks()
        self.display_tasks()

    def mark_as_done(self):
        if self.selected()[4:6].isdecimal():
            self.tasks[int(self.selected()[4:6]) - 1]['done'] = True
        else:
            self.tasks[int(self.selected()[4]) - 1]['done'] = True
        messagebox.showinfo("Completed", f"Task completed.")
        self.save_tasks()
        self.display_tasks()

    def choose_deadline(self):
        self.deadline_entry.delete(0, tk.END)
        if self.selected()[4:6].isdecimal():
            self.deadline_entry.insert(tk.END, self.tasks[int(self.selected()[4:6]) - 1]['deadline'])
        else:
            self.deadline_entry.insert(tk.END, self.tasks[int(self.selected()[4]) - 1]['deadline'])

    def change_deadline(self):
        text_deadline = self.deadline_entry.get()
        if self.selected()[4:6].isdecimal():
            self.tasks[int(self.selected()[4:6]) - 1].update(deadline=text_deadline)
        else:
            self.tasks[int(self.selected()[4]) - 1].update(deadline=text_deadline)
        self.save_tasks()
        self.display_tasks()
        messagebox.showinfo("Changed", "Deadline changed.")

    def clear_all(self):
        self.task_listbox.delete(0, tk.END)
        self.tasks = []
        self.save_tasks()
        self.display_tasks()
        messagebox.showinfo("Cleanup", "All tasks cleared.")

    def selected(self):
        selected_line = self.task_listbox.curselection()
        selected_elements = ''.join([self.task_listbox.get(i) for i in selected_line])
        return selected_elements

    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            self.task_listbox.insert(tk.END, f"{' + ' if task['done'] else '   '} {i + 1}. {task['task']}")
            for j, subtask in enumerate(self.tasks[i]['subtasks']):
                self.task_listbox.insert(tk.END,
                                         f"        {i + 1}.{j + 1}. {subtask['subtask']}")


if __name__ == "__main__":
    app = TodoListApp()
    app.mainloop()
