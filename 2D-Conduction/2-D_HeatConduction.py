import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

# Physical parameters
plate_length_mm = 50
num_nodes = 20
thermal_diffusivity = 110
total_time_s = 4

# Derived parameters
dx = plate_length_mm / (num_nodes - 1)
dy = plate_length_mm / (num_nodes - 1)
dt = min(dx**2 / (4 * thermal_diffusivity),
         dy**2 / (4 * thermal_diffusivity))
num_time_steps = int(total_time_s / dt) + 1

# Initialize temperature field
temperature = np.zeros((num_nodes, num_nodes)) + 20
temperature[:, 0] = 10
temperature[:, -1] = 100
temperature[0, :] = 10
temperature[-1, :] = 100

# Prepare to save frames
os.makedirs("frames", exist_ok=True)
frame_files = []

# Plotting setup
fig, ax = plt.subplots()
color_mesh = ax.pcolormesh(temperature, cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(color_mesh, ax=ax)

current_time = 0.0
frame_count = 0

while current_time < total_time_s:
    temp_old = temperature.copy()
    for i in range(1, num_nodes - 1):
        for j in range(1, num_nodes - 1):
            d2T_dx2 = (temp_old[i+1, j] - 2 * temp_old[i, j] + temp_old[i-1, j]) / dx**2
            d2T_dy2 = (temp_old[i, j+1] - 2 * temp_old[i, j] + temp_old[i, j-1]) / dy**2
            temperature[i, j] = temp_old[i, j] + dt * thermal_diffusivity * (d2T_dx2 + d2T_dy2)

    current_time += dt
    print(f"t: {current_time:.3f} s, Avg T: {np.average(temperature):.2f} °C")

    color_mesh.set_array(temperature.ravel())
    ax.set_title(f"t = {current_time:.2f} s")

    # Save current frame as image
    frame_path = f"frames/frame_{frame_count:04d}.png"
    plt.savefig(frame_path)
    frame_files.append(frame_path)
    frame_count += 1

# Stitch frames into GIF
images = [Image.open(f) for f in frame_files]
images[0].save("heat_distribution.gif", save_all=True, append_images=images[1:], duration=40, loop=0)

# Optional: Clean up frames
for f in frame_files:
    os.remove(f)
