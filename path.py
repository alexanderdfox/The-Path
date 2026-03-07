import tkinter as tk
from tkinter import filedialog
from svgpathtools import svg2paths
import random

# --- Setup Tkinter window ---
root = tk.Tk()
root.title("Python Turtle SVG Draw")
width, height = 1200, 800
canvas = tk.Canvas(root, width=width, height=height, bg="black")
canvas.pack(fill="both", expand=True)

# --- Turtle state ---
paths = []
turtle = {"path_index":0, "t":0.0, "dir":1, "x":0, "y":0}

# --- Scaling function ---
def scale_point(x, y, svg_width, svg_height):
	sx = width / svg_width
	sy = height / svg_height
	return x*sx, y*sy

# --- Load SVG ---
def load_svg():
	global paths, turtle
	file_path = filedialog.askopenfilename(filetypes=[("SVG files","*.svg")])
	if not file_path:
		return
	p, attributes = svg2paths(file_path)
	if not p:
		print("No paths found in SVG.")
		return
	paths = p
	# Initialize turtle at a random path start
	turtle["path_index"] = random.randint(0,len(paths)-1)
	start_point = paths[turtle["path_index"]].point(0)
	turtle["x"], turtle["y"] = scale_point(start_point.real, start_point.imag, 1000, 1000)
	animate()

# --- Animation ---
def animate():
	if not paths:
		return
	# Randomly flip direction
	if random.random() < 0.01:
		turtle["dir"] *= -1

	# Move along path
	turtle["t"] += 0.01 * turtle["dir"]

	# If t exceeds [0,1], pick new path
	if turtle["t"] > 1 or turtle["t"] < 0:
		turtle["t"] = random.random()
		turtle["path_index"] = random.randint(0,len(paths)-1)
		turtle["dir"] = 1 if random.random()<0.5 else -1

	path = paths[turtle["path_index"]]
	point = path.point(turtle["t"])
	x_new, y_new = scale_point(point.real, point.imag, 1000, 1000)

	# Draw line segment
	color = "#%02x%02x%02x" % (random.randint(50,255), random.randint(50,255), random.randint(50,255))
	canvas.create_line(turtle["x"], turtle["y"], x_new, y_new, fill=color, width=2)

	turtle["x"], turtle["y"] = x_new, y_new
	root.after(10, animate)  # 10 ms delay for smooth & fast drawing

# --- File load button ---
button = tk.Button(root, text="Load SVG", command=load_svg)
button.pack()

root.mainloop()