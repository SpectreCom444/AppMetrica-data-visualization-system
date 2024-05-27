import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data import load_data_wrapper, data_processing, create_session, create_users
from shared import shared_state
from visualization import create_chart

types_graphs = ["line","bar","pie","scatter","histogram","heatmap","bubble","area"]

class CustomEventMenu:
    def __init__(self, canvas, shared_state):
        self.canvas = canvas
        self.shared_state = shared_state
        self.panel = tk.Frame(self.canvas)
        self.panel.pack()
        self.canvas.create_window(600, 200, window=self.panel)
        self.selected_options = []
        self.current_options = list(self.shared_state.json_tree.keys())
        self.create_text_widget()
        self.create_buttons()  
        self.create_undo_button()

    def create_buttons(self):
        for widget in self.panel.winfo_children():
            if isinstance(widget, tk.Button) and widget != self.undo_button:
                widget.destroy()

        for idx, option in enumerate(self.current_options):
            button = tk.Button(self.panel, text=option, command=lambda opt=option: self.add_to_selected(opt))
            button.grid(row=(idx // 5) + 1, column=idx % 5, padx=5, pady=5)

    def create_undo_button(self):
        self.undo_button = tk.Button(self.panel, text="Undo", command=self.undo_last_selection)
        self.undo_button.grid(row=0, column=5, padx=5, pady=5)

    def add_to_selected(self, option):
        if option not in self.selected_options:
            self.selected_options.append(option)
            self.update_text_widget()
            self.update_options()

    def undo_last_selection(self):
        if self.selected_options:
            self.selected_options.pop()
            self.update_text_widget()
            self.update_options()

    def update_options(self):
        current_level = self.shared_state.json_tree
        for opt in self.selected_options:
            current_level = current_level.get(opt, {})
        if isinstance(current_level, dict):
            self.current_options = list(current_level.keys())
        else:
            self.current_options = []
        self.create_buttons()
    
    def create_text_widget(self):
        self.text_widget = tk.Text(self.panel, height=1, width=40)
        self.text_widget.grid(row=0, column=0, columnspan=5, padx=5, pady=5)
    
    def update_text_widget(self):
        self.text_widget.delete(1.0, tk.END)
        for option in self.selected_options:
            self.text_widget.insert(tk.END, option + '->')

    def remove_panel(self):
        if self.panel:
            self.panel.destroy()
            self.panel = None

def uploadin_and_processing():
    load_data_wrapper(load_data_done)
    data_processing(create_events_done)
    if "session_id" in  shared_state.names:
        create_session(create_session_done)

        if "appmetrica_device_id" in  shared_state.names:
            create_users(create_user_done)
    
def create_ui():
    global root
    global canvas
    global load_data_checkbox
    global create_events_checkbox
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

    create_events_checkbox_var = tk.IntVar()
    create_events_checkbox = tk.Checkbutton(root, text="Create events", variable=create_events_checkbox_var, state='disabled')
    canvas.create_window(50, 200, window=create_events_checkbox)

    create_sessions_checkbox_var = tk.IntVar()
    create_sessions_checkbox = tk.Checkbutton(root, text="Create sessions", variable=create_sessions_checkbox_var, state='disabled')
    canvas.create_window(50, 250, window=create_sessions_checkbox)

    create_users_checkbox_var = tk.IntVar()
    create_users_checkbox = tk.Checkbutton(root, text="Create users", variable=create_users_checkbox_var, state='disabled')
    canvas.create_window(50, 300, window=create_users_checkbox)

    root.mainloop()

def create_vizualization_button():
    global fig_canvas   
    global menu_instance

    def on_selected_data_change(*args):
        create_custom_event_menu(selected_data.get() == "event_json")

    panel = tk.Frame(root)
    canvas.create_window(200, 200, window=panel)

    selected_data = tk.StringVar()
    selected_data.set(shared_state.names[0])
    selected_data.trace('w', on_selected_data_change)
    dropdown_selected_data = tk.OptionMenu(panel, selected_data, *shared_state.names)
    dropdown_selected_data.pack(pady=10)

    
    selected_chart_type = tk.StringVar()
    selected_chart_type.set(types_graphs[0])   
    dropdown_selected_chart_type = tk.OptionMenu(panel, selected_chart_type, *types_graphs)
    dropdown_selected_chart_type.pack(pady=10)

    fig_canvas = FigureCanvasTkAgg( Figure(figsize=(5, 4), dpi=150), master=canvas)  
    fig_canvas.draw()
    fig_canvas.get_tk_widget().pack(side=tk.RIGHT,padx=100)

    plot_button = tk.Button(panel, text="Plot chart", command=lambda: create_chart(fig_canvas,selected_data.get(),selected_chart_type.get()))
    plot_button.pack(pady=10)

    menu_instance = None 

def create_custom_event_menu(show):
    global menu_instance
    if show:
        if menu_instance is None:
            menu_instance = CustomEventMenu(canvas, shared_state)
    else:
        if menu_instance is not None:
            menu_instance.remove_panel()
            menu_instance = None
        
    
  
def load_data_done():

    load_data_checkbox.select()

def create_events_done():

    create_events_checkbox.select()
    create_vizualization_button()

def create_session_done():
    create_sessions_checkbox.select()

def create_user_done():
    create_users_checkbox.select()

