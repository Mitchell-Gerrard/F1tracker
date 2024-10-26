import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Create the main application window
root = tk.Tk()
root.title("Multi-Graph and Input Dashboard")
root.geometry("1000x800")

# Notebook widget for multiple tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill='both')

# Create tab frames
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
notebook.add(tab1, text="Graphs Page 1")
notebook.add(tab2, text="Graphs Page 2")
notebook.add(tab3, text="Graphs Page 3")

# Create frames for the text inputs
input_frame = ttk.Frame(root)
input_frame.pack(side="top", fill="x", pady=10)

# Add 4 text input fields with labels
entries = []
for i in range(4):
    label = tk.Label(input_frame, text=f"Input {i + 1}")
    label.grid(row=0, column=i * 2, padx=5, pady=5)
    entry = tk.Entry(input_frame, width=20)
    entry.grid(row=0, column=i * 2 + 1, padx=5, pady=5)
    entries.append(entry)

# Add a submit button next to input fields
def on_submit():
    # Retrieve and print the input values
    inputs = [entry.get() for entry in entries]
    print("Submitted inputs:", inputs)
    # Optionally, process the inputs as needed

submit_button = tk.Button(input_frame, text="Submit", command=on_submit)
submit_button.grid(row=0, column=8, padx=10, pady=5)

# Function to create a random graph
def create_random_graph():
    x = list(range(10))
    y = [random.randint(1, 10) for _ in range(10)]
    fig = Figure(figsize=(4, 3), dpi=100)
    plot = fig.add_subplot(111)
    plot.plot(x, y, marker='o')
    return fig

# Function to add three graphs to a given tab
def add_three_graphs_to_tab(tab):
    for i in range(3):
        fig = create_random_graph()
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=10, pady=10)
        canvas._tkcanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Add three graphs to each tab
for tab in [tab1, tab2, tab3]:
    add_three_graphs_to_tab(tab)

# Start the main loop
root.mainloop()

