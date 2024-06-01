from visualization.visualization import Plotter

TYPES_GRAPHS= {
    'line': Plotter.plot_line_chart,
    'bar': Plotter.plot_bar_chart,
    'pie': Plotter.plot_pie_chart,
    'ring': Plotter.plot_ring_chart,
    'scatter': Plotter.plot_scatter_plot,
    'histogram': Plotter.plot_histogram,
    'bubble': Plotter.plot_bubble_chart,
    'area': Plotter.plot_area_chart,
    'funnel': Plotter.plot_funnel,
}