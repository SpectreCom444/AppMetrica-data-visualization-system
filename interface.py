import tkinter as tk
from data import load_data_wrapper, data_processing, create_session, create_users

def uploadin_and_processing():
    load_data_wrapper(load_data_done)
    data_processing(create_ui_session, create_ui_user)

def create_ui():
    global root
    global canvas
    global load_data_checkbox
    global create_sessions_checkbox
    global create_users_checkbox

    root = tk.Tk()
    root.title("Tkinter Example with Buttons")

    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()

    load_data_button = tk.Button(root, text="Load Data", command=uploadin_and_processing)
    canvas.create_window(50, 100, window=load_data_button)

    load_data_checkbox_var = tk.IntVar()
    load_data_checkbox = tk.Checkbutton(root, text="Load Data", variable=load_data_checkbox_var, state='disabled')
    canvas.create_window(50, 150, window=load_data_checkbox)

    create_sessions_checkbox_var = tk.IntVar()
    create_sessions_checkbox = tk.Checkbutton(root, text="Create sessions", variable=create_sessions_checkbox_var, state='disabled')
    canvas.create_window(50, 200, window=create_sessions_checkbox)

    create_users_checkbox_var = tk.IntVar()
    create_users_checkbox = tk.Checkbutton(root, text="Create users", variable=create_users_checkbox_var, state='disabled')
    canvas.create_window(50, 250, window=create_users_checkbox)
 
    root.mainloop()

def load_data_done():
    load_data_checkbox.select()

def create_session_done():
    create_sessions_checkbox.select()

def create_user_done():
    create_users_checkbox.select()

def create_ui_session():
    create_session_button = tk.Button(root, text="Create sessions", command=lambda: create_session(create_session_done))
    canvas.create_window(150, 100, window=create_session_button)
   
def create_ui_user():
    create_user_button = tk.Button(root, text="Create users", command=lambda: create_users(create_user_done))
    canvas.create_window(250, 100, window=create_user_button)
