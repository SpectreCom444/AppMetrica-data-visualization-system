import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data import load_data_wrapper, data_processing, create_session, create_users,shared_state
from visualization import plot_line_chart,plot_bar_chart,plot_scatter_plot,plot_histogram,plot_heatmap,plot_bubble_chart,plot_area_chart,plot_pie_chart

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
    
    create_fig_canvas()
    plot_line_button = tk.Button(root, text="Plot Line Chart", command=lambda: plot_line_chart(fig_canvas,shared_state.names[9]))
    canvas.create_window(400, 50, window=plot_line_button)

    plot_bar_button = tk.Button(root, text="Plot Bar Chart", command=lambda: plot_bar_chart(fig_canvas,shared_state.names[9]))
    canvas.create_window(400, 100, window=plot_bar_button)

    plot_scatter_button = tk.Button(root, text="Plot Scatter Plot", command=lambda: plot_scatter_plot(fig_canvas,shared_state.names[9]))
    canvas.create_window(400, 150, window=plot_scatter_button)

    plot_histogram_button = tk.Button(root, text="Plot Histogram", command=lambda: plot_histogram(fig_canvas,shared_state.names[9]))
    canvas.create_window(400, 200, window=plot_histogram_button)

    plot_heatmap_button = tk.Button(root, text="Plot Heatmap", command=lambda: plot_heatmap(fig_canvas,shared_state.names[9]),bg='grey')
    canvas.create_window(400, 250, window=plot_heatmap_button)

    plot_bubble_button = tk.Button(root, text="Plot Bubble Chart", command=lambda: plot_bubble_chart(fig_canvas,shared_state.names[9]))
    canvas.create_window(400, 300, window=plot_bubble_button)

    plot_area_button = tk.Button(root, text="Plot Area Chart", command=lambda: plot_area_chart(fig_canvas,shared_state.names[9]))
    canvas.create_window(400, 350, window=plot_area_button)

    plot_pie_button = tk.Button(root, text="Plot Pie Chart", command=lambda: plot_pie_chart(fig_canvas,shared_state.names[9]))
    canvas.create_window(400, 400, window=plot_pie_button)
    
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
