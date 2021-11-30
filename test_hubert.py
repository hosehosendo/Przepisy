# Simple To-Do List App
# by TokyoEdtech
# Python 3.8 using Geany Editor
# Ubuntu Linux (Mac and Windows Compatible)
# Topics: tkinter, grid geometry manager
# Topics: Listbox Widget, Scrollbar widget, tkinter.messagebox, Try/Except Block, pickle

import tkinter
import tkinter.messagebox
import pickle

root1 = tkinter.Tk()
root1.title("to-do")

root2 = tkinter.Tk()
root2.title("to-do")

class window:

    def __init__(self, root):

        self.root = root

        # Create GUI
        frame_tasks = tkinter.Frame(root)
        frame_tasks.pack()

        listbox_tasks = tkinter.Listbox(frame_tasks, height=10, width=50)
        listbox_tasks.pack(side=tkinter.LEFT)

        scrollbar_tasks = tkinter.Scrollbar(frame_tasks)
        scrollbar_tasks.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
        scrollbar_tasks.config(command=listbox_tasks.yview)

        entry_task = tkinter.Entry(root, width=50)
        entry_task.pack()

    def add_buttons(self):
        button_add_task = tkinter.Button(self.root, text="Add task", width=48, command=self.add_task)
        button_add_task.pack()

        button_delete_task = tkinter.Button(self.root, text="Delete task", width=48, command=self.delete_task)
        button_delete_task.pack()

        button_load_tasks = tkinter.Button(self.root, text="Load tasks", width=48, command=self.load_tasks)
        button_load_tasks.pack()

        button_save_tasks = tkinter.Button(self.root, text="Save tasks", width=48, command=self.save_tasks)
        button_save_tasks.pack()

    def add_task(self):
        task = self.entry_task.get()
        if task != "":
            self.listbox_tasks.insert(tkinter.END, task)
            self.entry_task.delete(0, tkinter.END)
        else:
            tkinter.messagebox.showwarning(title="Warning!", message="You must enter a task.")

    def delete_task(self):
        try:
            task_index = self.listbox_tasks.curselection()[0]
            self.listbox_tasks.delete(task_index)
        except:
            tkinter.messagebox.showwarning(title="Warning!", message="You must select a task.")

    def load_tasks(self):
        try:
            tasks = pickle.load(open("tasks.dat", "rb"))
            self.listbox_tasks.delete(0, tkinter.END)
            for task in tasks:
                self.listbox_tasks.insert(tkinter.END, task)
        except:
            tkinter.messagebox.showwarning(title="Warning!", message="Cannot find tasks.dat.")

    def save_tasks(self):
        tasks = self.listbox_tasks.get(0, self.listbox_tasks.size())
        pickle.dump(tasks, open("tasks.dat", "wb"))


first_window = window(root1)
first_window.add_buttons()
root1.mainloop()