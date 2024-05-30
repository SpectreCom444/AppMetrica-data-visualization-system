import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data import load_data_wrapper, data_processing, create_session, create_users
from shared import shared_state, TypeOfData
from visualization import create_chart
from tkcalendar import DateEntry
from visualization_params import VisualizationParams
import constants
import type_graphs
from tkinterdnd2 import DND_FILES, TkinterDnD

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
        current_level = self.shared_state.json_tree
        for opt in self.selected_options:
            if isinstance(current_level, dict):
                current_level = current_level.get(opt, {})
            else:
                current_level = {}
                break
        for idx, option in enumerate(self.current_options):     
            has_children = isinstance(current_level.get(option, {}), dict) and bool(current_level.get(option, {}))
            state = tk.NORMAL if has_children else tk.DISABLED
            button = tk.Button(self.panel, text=option, command=lambda opt=option: self.add_to_selected(opt), state=state)
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
            if isinstance(current_level, dict):
                current_level = current_level.get(opt, {})
            else:
                current_level = {}
                break

        if isinstance(current_level, dict):
            self.current_options = list(current_level.keys())
        else:
            self.current_options = [current_level]
        self.create_buttons()
    
    def create_text_widget(self):
        self.text_widget = tk.Text(self.panel, height=1, width=40)
        self.text_widget.grid(row=0, column=0, columnspan=5, padx=5, pady=5)
    
    def update_text_widget(self):
        self.text_widget.delete(1.0, tk.END)
        for option in self.selected_options:
            self.text_widget.insert(tk.END, str(option) + '->')

    def remove_panel(self):
        if self.panel:
            self.panel.destroy()
            self.panel = None

    def get_selected_options(self):
        return self.selected_options 
    
    
def uploading_and_processing(path):
    drop_frame.destroy()
    load_data_wrapper(path,load_data_done)
    data_processing(create_events_done)
    if constants.SESSION_ID in  shared_state.names:
        create_session(create_session_done)

        if constants.DEVICE_ID in  shared_state.names:
            create_users(create_user_done)

    
def create_ui():
    global root
    global canvas
    global load_data_checkbox
    global create_events_checkbox
    global create_sessions_checkbox
    global create_users_checkbox
    global fig_canvas
    global drop_frame
    global load_data_frame
    root = TkinterDnD.Tk()
    root.attributes('-fullscreen', True)

    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=True)

    close_button = tk.Button(root, text=" X ", command=root.quit, bg="red")
    canvas.create_window(1800, 50, window=close_button)
    drop_frame = tk.Frame(root, width=300, height=300, bg='lightgrey')
    drop_frame.pack_propagate(False)
    canvas.create_window(root.winfo_screenwidth()/2, root.winfo_screenheight()/2, window=drop_frame)

    drop_frame.drop_target_register(DND_FILES)
    drop_frame.dnd_bind('<<Drop>>', lambda event: uploading_and_processing(event.data))

    label = tk.Label(drop_frame, text="Drag and drop the file here", bg='lightgrey')
    label.pack(expand=True)


    load_data_frame = tk.Frame(root)
    load_data_frame.pack()
    canvas.create_window(100, 150, window=load_data_frame)

    load_data_checkbox_var = tk.IntVar()
    load_data_checkbox = tk.Checkbutton(load_data_frame, text="Load Data", variable=load_data_checkbox_var, state='disabled')
    load_data_checkbox.grid(row=1, column=1, padx=5, pady=5)

    create_events_checkbox_var = tk.IntVar()
    create_events_checkbox = tk.Checkbutton(load_data_frame, text="Create events", variable=create_events_checkbox_var, state='disabled')
    create_events_checkbox.grid(row=2, column=1, padx=5, pady=5)

    create_sessions_checkbox_var = tk.IntVar()
    create_sessions_checkbox = tk.Checkbutton(load_data_frame, text="Create sessions", variable=create_sessions_checkbox_var, state='disabled')
    create_sessions_checkbox.grid(row=3, column=1, padx=5, pady=5)

    create_users_checkbox_var = tk.IntVar()
    create_users_checkbox = tk.Checkbutton(load_data_frame, text="Create users", variable=create_users_checkbox_var, state='disabled')
    create_users_checkbox.grid(row=4, column=1, padx=5, pady=5)

    root.mainloop()

def create_date_selector():
    global start_date_entry
    global end_date_entry

    frame_date_selector = tk.Frame(root)
    frame_date_selector.pack()
    canvas.create_window(200, 400, window=frame_date_selector)

    tk.Label(frame_date_selector, text="Start Date:").grid(row=0, column=0, padx=5, pady=5)
    
    start_date_entry = DateEntry(frame_date_selector, width=12, background='darkblue',foreground='white', borderwidth=2, date_pattern='y-mm-dd')
    start_date_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_date_selector, text="End Date:").grid(row=1, column=0, padx=5, pady=5)
    
    end_date_entry = DateEntry(frame_date_selector, width=12, background='darkblue',foreground='white', borderwidth=2, date_pattern='y-mm-dd')
    end_date_entry.grid(row=1, column=1, padx=5, pady=5)


def create_vizualization_button():
    global fig_canvas   
    global menu_instance
    global selected_data
    global selected_chart_type

    def on_selected_data_change(*args):
        create_custom_event_menu(selected_data.get() == constants.EVENT_JSON)

    panel = tk.Frame(root)
    canvas.create_window(200, 200, window=panel)

    selected_data = tk.StringVar()
    selected_data.set(shared_state.names[0])
    selected_data.trace('w', on_selected_data_change)
    dropdown_selected_data = tk.OptionMenu(panel, selected_data, *shared_state.names)
    dropdown_selected_data.pack(pady=10)

    
    selected_chart_type = tk.StringVar()
    selected_chart_type.set( next(iter(type_graphs.TYPES_GRAPHS)))   
    dropdown_selected_chart_type = tk.OptionMenu(panel, selected_chart_type, *type_graphs.TYPES_GRAPHS)
    dropdown_selected_chart_type.pack(pady=10)

    fig_canvas = FigureCanvasTkAgg( Figure(figsize=(5, 4), dpi=150), master=canvas)  
    fig_canvas.draw()
    fig_canvas.get_tk_widget().pack(side=tk.RIGHT,padx=100)      
    plot_button = tk.Button(panel, text="Plot chart", command=data_for_chart)
    plot_button.pack(pady=10)

    menu_instance = None 
    if constants.EVENT_DATATIME in shared_state.names:
        create_date_selector()

def data_for_chart():
    if selected_data.get() == constants.EVENT_JSON:
        if len(menu_instance.get_selected_options())>0:
            visualization_params=VisualizationParams(TypeOfData.TREE,fig_canvas,menu_instance.get_selected_options(),type_graphs.TYPES_GRAPHS[selected_chart_type.get()] )
        else:
            if constants.EVENT_NAME in shared_state.names :
                visualization_params=VisualizationParams(TypeOfData.FIELD_NAME,fig_canvas,constants.EVENT_NAME,type_graphs.TYPES_GRAPHS[selected_chart_type.get()] )
    else:
        visualization_params=VisualizationParams(TypeOfData.FIELD_NAME,fig_canvas,selected_data.get(),type_graphs.TYPES_GRAPHS[selected_chart_type.get()] )


    if constants.EVENT_DATATIME in shared_state.names:
        visualization_params.set_data_time(start_date_entry.get(),end_date_entry.get())

    create_chart(visualization_params)
            

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
    load_data_frame.destroy()

