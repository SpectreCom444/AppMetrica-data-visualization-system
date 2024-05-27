import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data import load_data_wrapper, data_processing, create_session, create_users
from shared import shared_state
from visualization import create_chart

types_graphs = ["line","bar","pie","scatter","histogram","heatmap","bubble","area"]

def uploadin_and_processing():
    load_data_wrapper(load_data_done)
    data_processing(create_ui_session, create_ui_user)

def create_ui():
    global root
    global canvas
    global load_data_checkbox
    global create_sessions_checkbox
    global create_users_checkbox
    global fig_canvas

    root = tk.Tk()
    root.attributes('-fullscreen', True)

    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=True)

    close_button = tk.Button(root, text=" X ", command=root.quit, bg="red")
    canvas.create_window(1800, 50, window=close_button)

    

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

def create_fig_canvas():
    global fig_canvas

    fig_canvas = FigureCanvasTkAgg( Figure(figsize=(5, 4), dpi=150), master=canvas)  
    fig_canvas.draw()
    fig_canvas.get_tk_widget().pack(side=tk.RIGHT,padx=100)

def create_vizualization_button():
    global panel_json_event

    panel_json_event = tk.Frame(root)
    panel_json_event.pack_forget()

    def on_selected_data_change(*args):
        create_custom_event_menu(selected_data.get() == "event_json")

    panel = tk.Frame(root)
    canvas.create_window(400, 200, window=panel)

    selected_data = tk.StringVar()
    selected_data.set(shared_state.names[0])
    selected_data.trace('w', on_selected_data_change)
    dropdown_selected_data = tk.OptionMenu(panel, selected_data, *shared_state.names)
    dropdown_selected_data.pack(pady=10)

    
    selected_chart_type = tk.StringVar()
    selected_chart_type.set(types_graphs[0])   
    dropdown_selected_chart_type = tk.OptionMenu(panel, selected_chart_type, *types_graphs)
    dropdown_selected_chart_type.pack(pady=10)

    create_fig_canvas()
    plot_button = tk.Button(panel, text="Plot chart", command=lambda: create_chart(fig_canvas,selected_data.get(),selected_chart_type.get()))
    plot_button.pack(pady=10)



def create_custom_event_menu(show):
    if show:    
        panel_json_event.pack()
        canvas.create_window(700, 200, window=panel_json_event)
        max_buttons_per_row = 5
        row = 0
        col = 0

        for key in enumerate(shared_state.json_tree.keys()):
            button = tk.Button(panel_json_event, text=key) 
            button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col >= max_buttons_per_row:
                col = 0
                row += 1
    else:
        panel_json_event.pack_forget()
        
    
  
def load_data_done():

    load_data_checkbox.select()
    create_vizualization_button()

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
