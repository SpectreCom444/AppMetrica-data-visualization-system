
import matplotlib.pyplot as plt


def plot_line_chart():
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    plt.plot(x, y, marker='o')
    plt.title("Line Chart")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()

def plot_bar_chart():
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [3, 7, 5, 6, 4]
    plt.bar(categories, values)
    plt.title("Bar Chart")
    plt.xlabel("Categories")
    plt.ylabel("Values")
    plt.show()

def plot_pie_chart():
    labels = ['A', 'B', 'C', 'D']
    sizes = [15, 30, 45, 10]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title("Pie Chart")
    plt.show()

def plot_scatter_plot():
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    plt.scatter(x, y)
    plt.title("Scatter Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()

def plot_histogram():
    data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]
    plt.hist(data, bins=5)
    plt.title("Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()

import numpy as np

def plot_heatmap():
    data = np.random.rand(10, 10)
    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.title("Heatmap")
    plt.colorbar()
    plt.show()

def plot_bubble_chart():
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    sizes = [20, 50, 80, 200, 500]
    plt.scatter(x, y, s=sizes, alpha=0.5)
    plt.title("Bubble Chart")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()

def plot_area_chart():
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    plt.fill_between(x, y, color="skyblue", alpha=0.4)
    plt.plot(x, y, color="Slateblue", alpha=0.6)
    plt.title("Area Chart")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()
