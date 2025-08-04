import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Physical parameters
rod_length_mm = 50              # mm
num_nodes = 20                  # number of grid points
thermal_diffusivity = 210       # mm^2/s
total_time_s = 4                # seconds

# Derived parameters
dx = rod_length_mm / (num_nodes - 1)
dt = 0.5 * dx**2 / thermal_diffusivity
num_time_steps = int(total_time_s / dt) + 1

# Initialize temperature field
temperature = np.zeros(num_nodes) + 20  # start at 20 °C
temperature[0] = 70                      # left boundary
temperature[-1] = 100                    # right boundary

# Visualization setup
fig, ax = plt.subplots()
color_mesh = ax.pcolormesh([temperature], cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(color_mesh, ax=ax)
ax.set_ylim([-2, 3])  # narrow strip for 1D visualization

# Animation update function
current_time = 0.0
def update(frame):
    global temperature, current_time
    temp_old = temperature.copy()
    for i in range(1, num_nodes - 1):
        laplacian = (temp_old[i + 1] - 2 * temp_old[i] + temp_old[i - 1]) / dx**2
        temperature[i] = temp_old[i] + dt * thermal_diffusivity * laplacian

    current_time += dt
    print(f"t: {current_time:.3f} s, Average temperature: {np.average(temperature):.2f} °C")
    color_mesh.set_array([temperature])
    ax.set_title(f"Distribution at t = {current_time:.2f} s")
    return color_mesh,

# Run animation
anim = FuncAnimation(fig, update, frames=num_time_steps, interval=50)

# --- Save as GIF ---
writer = PillowWriter(fps=15)
anim.save("temperature_distribution.gif", writer=writer)

plt.show()
