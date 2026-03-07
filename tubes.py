import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from svgpathtools import svg2paths
import numpy as np
import random
from matplotlib.animation import FuncAnimation

# --- Load SVG paths ---
svg_file = "path.svg"  # replace with your SVG file
paths, _ = svg2paths(svg_file)

# --- Sample points from SVG paths ---
def sample_path(path, n_points=100):
	points = []
	for i in range(n_points):
		t = i / (n_points-1)
		point = path.point(t)
		points.append((point.real, point.imag))
	return points

all_lines = []
for path in paths:
	pts = sample_path(path, n_points=50)
	# Extrude in Z with small random offsets
	z_vals = np.random.uniform(-0.1, 0.1, len(pts))
	xyz = [(x, y, z) for (x, y), z in zip(pts, z_vals)]
	all_lines.append(xyz)

# --- Calculate total 3D length ---
def line_length_3d(points):
	length = 0.0
	for i in range(1, len(points)):
		x0, y0, z0 = points[i-1]
		x1, y1, z1 = points[i]
		dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
		length += np.sqrt(dx*dx + dy*dy + dz*dz)
	return length

total_length = sum(line_length_3d(line) for line in all_lines)
print(f"Total 3D line length: {total_length}")

# --- Set up 3D plot ---
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor("black")
ax.grid(False)
ax.axis('off')

# --- Plot lines ---
lines = []
for line in all_lines:
	xs, ys, zs = zip(*line)
	color = [random.random() for _ in range(3)]
	l, = ax.plot(xs, ys, zs, color=color, linewidth=2)
	lines.append(l)

# --- Animate rotation ---
def update(frame):
	ax.view_init(elev=30, azim=frame)
	return lines

ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50)
plt.show()