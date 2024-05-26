
import matplotlib.pyplot as plt
import numpy as np


def plot_line_chart(canvas):
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o')
    ax.set_title("Line Chart")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig  
    canvas.draw()

def plot_bar_chart(canvas):
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [3, 7, 5, 6, 4]
    fig, ax = plt.subplots()
    ax.bar(categories, values)
    ax.set_title("Bar Chart")
    ax.set_xlabel("Categories")
    ax.set_ylabel("Values")
    canvas.figure = fig  
    canvas.draw()

def plot_pie_chart(canvas):
    labels = ['A', 'B', 'C', 'D']
    sizes = [15, 30, 45, 10]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.set_title("Pie Chart")
    canvas.figure = fig 
    canvas.draw()

def plot_scatter_plot(canvas):
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_title("Scatter Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig 
    canvas.draw()

def plot_histogram(canvas):
    data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]
    fig, ax = plt.subplots()
    ax.hist(data, bins=5)
    ax.set_title("Histogram")
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    canvas.figure = fig 
    canvas.draw()

def plot_heatmap(canvas):
    data = np.random.rand(10, 10)
    fig, ax = plt.subplots()
    cax = ax.imshow(data, cmap='hot', interpolation='nearest')
    fig.colorbar(cax)
    ax.set_title("Heatmap")
    canvas.figure = fig 
    canvas.draw()

def plot_bubble_chart(canvas):
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    sizes = [20, 50, 80, 200, 500]
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=sizes, alpha=0.5)
    ax.set_title("Bubble Chart")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig 
    canvas.draw()

def plot_area_chart(canvas):
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]
    fig, ax = plt.subplots()
    ax.fill_between(x, y, color="skyblue", alpha=0.4)
    ax.plot(x, y, color="Slateblue", alpha=0.6)
    ax.set_title("Area Chart")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig 
    canvas.draw()