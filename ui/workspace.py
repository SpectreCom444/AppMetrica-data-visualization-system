import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shared import shared_state, TypeOfData
from visualization import create_chart
from tkcalendar import DateEntry
import type_graphs
import constants
from visualization_params import VisualizationParams

from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QPushButton, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class WorkspaceWindow(QMainWindow):
    def __init__(self):
        super(WorkspaceWindow, self).__init__()
        loadUi('ui/workspace.ui', self)
        self.create_vizualization_button()

    def create_vizualization_button(self):


        def on_selected_data_change(*args):
            self.create_custom_event_menu(self.dropdown_selected_data.currentText() == constants.EVENT_JSON)

        self.dropdown_selected_data.addItems(shared_state.names)
        self.dropdown_selected_data.setCurrentText(shared_state.names[0])
        self.dropdown_selected_data.currentTextChanged.connect(on_selected_data_change)

        self.selected_chart_type.addItems(type_graphs.TYPES_GRAPHS.keys())
        self.selected_chart_type.setCurrentText(next(iter(type_graphs.TYPES_GRAPHS)))
        self.selected_chart_type.currentTextChanged.connect(on_selected_data_change)

        self.plot_button.clicked.connect(self.data_for_chart)

        if constants.EVENT_DATATIME in shared_state.names:
            self.create_date_selector()



        # fig = Figure(figsize=(5, 4), dpi=150)
        # fig_canvas = FigureCanvasTkAgg(fig, master=canvas)
        # fig_canvas.draw()
        # fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)      
    
    

    def data_for_chart(self):
        pass
        # if selected_data.get() == constants.EVENT_JSON:
        #     if len(menu_instance.get_selected_options())>0:
        #         visualization_params=VisualizationParams(TypeOfData.TREE,fig_canvas,menu_instance.get_selected_options(),type_graphs.TYPES_GRAPHS[selected_chart_type.get()] )
        #     else:
        #         if constants.EVENT_NAME in shared_state.names :
        #             visualization_params=VisualizationParams(TypeOfData.FIELD_NAME,fig_canvas,constants.EVENT_NAME,type_graphs.TYPES_GRAPHS[selected_chart_type.get()] )
        # else:
        #     visualization_params=VisualizationParams(TypeOfData.FIELD_NAME,fig_canvas,selected_data.get(),type_graphs.TYPES_GRAPHS[selected_chart_type.get()] )


        # if constants.EVENT_DATATIME in shared_state.names:
        #     visualization_params.set_data_time(start_date_entry.get(),end_date_entry.get())

        # create_chart(visualization_params)

    def create_date_selector(self):
        pass
        # global root
        # global canvas
        # global start_date_entry
        # global end_date_entry

        # frame_date_selector = tk.Frame(root)
        # frame_date_selector.pack()
        # canvas.create_window(200, 400, window=frame_date_selector)

        # tk.Label(frame_date_selector, text="Start Date:").grid(row=0, column=0, padx=5, pady=5)
        
        # start_date_entry = DateEntry(frame_date_selector, width=12, background='darkblue',foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        # start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        # tk.Label(frame_date_selector, text="End Date:").grid(row=1, column=0, padx=5, pady=5)
        
        # end_date_entry = DateEntry(frame_date_selector, width=12, background='darkblue',foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        # end_date_entry.grid(row=1, column=1, padx=5, pady=5)

    def create_custom_event_menu(self, show):
        global menu_instance
        # if show:
        #     if menu_instance is None:
        #         menu_instance = CustomEventMenu(canvas, shared_state)
        # else:
        #     if menu_instance is not None:
        #         menu_instance.remove_panel()
        #         menu_instance = None
            

   

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
