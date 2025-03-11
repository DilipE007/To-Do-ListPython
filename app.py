import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def setup_db():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
    conn.commit()
    conn.close()

# Add Task
def add_task():
    task = task_entry.get()
    if task:
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
        task_entry.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

# Load Tasks
def load_tasks():
    task_list.delete(0, tk.END)
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        task_list.insert(tk.END, f"{task[0]} - {task[1]}")

# Delete Task
def delete_task():
    try:
        selected_task = task_list.get(task_list.curselection())
        task_id = selected_task.split(" - ")[0]
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task to delete!")

# GUI Setup
setup_db()
root = tk.Tk()
root.title("To-Do List")
root.geometry("400x400")

task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

task_add_button = tk.Button(root, text="Add Task", command=add_task)
task_add_button.pack()

task_list = tk.Listbox(root, width=50, height=15)
task_list.pack(pady=10)

load_tasks()

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack()

root.mainloop()
