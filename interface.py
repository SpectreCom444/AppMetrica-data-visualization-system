import tkinter as tk
from data import names,load_data_wrapper,data_processing



def create_ui():
    root = tk.Tk()
    root.title("Tkinter Example with Buttons")

    canvas = tk.Canvas(root, width=300, height=200)
    canvas.pack()
    button1 = tk.Button(root, text="Load Data", command=load_data_wrapper)
    canvas.create_window(50, 100, window=button1)   
    
    root.mainloop()
    
def crate_data_processing_ui():
    pass
    
    