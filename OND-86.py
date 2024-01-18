import numpy
from math import pi, sqrt
import matplotlib.pyplot as plt
import matplotlib as mpl
import tkinter as tk
from tkinter import ttk

flow_entry = None
height_entry = None
diameter_entry = None
w0_speed_entry = None
u_x_entry = None
u_y_entry = None
u_pdk_entry = None
strat_entry = None
dT_entry = None
coef_os_entry = None

def main(limit_x, limit_y, s_flow, s_height, s_diameter, s_speed, F, x0, y0, pdk, strat, dT):
    # Part 1: Calculation of maximum concentration
    v = ((pi * s_diameter**2) / 4) * s_speed       # calculation of the volumetric emission
    print('V: %s' % v)

    # Calculation of auxiliary parameters:
    f = 1000 * ((s_speed**2) * s_diameter) / ((s_height**2) * dT)
    vm = 0.65 * ((v * dT) / s_height)**(1/3)
    vm2 = 1.3 * (s_speed * s_diameter) / s_height
    fe = 800 * (vm2**3)
    print('f: %s' % f)
    print('fe: %s' % fe)
    print('vm: %s' % vm)
    print('vm2: %s' % vm2)

    # Calculate m
    if f < 100:
        m = 1 / (0.67 + 0.1 * sqrt(f) + 0.34 * (f**(1/3)))
    else:
        m = 1.47 / (f**(1/3))
    print('m: %s' % m)

    # Calculate n
    if vm >= 2:
        n = 1
    elif vm >= 0.5:
        n = 0.532 * (vm**2) - 2.13 * vm + 3.13
    else:
        n = 4.4 * vm
    print('n: %s' % n)

    # K and Cm:
    if f >= 100 and vm2 >= 0.5:
        K = s_diameter / 8 * v
        Cm = ((strat * s_flow * n * F) / (s_height**(4/3))) * K
    elif f < 100 and vm2 < 0.5:
        m = m * 2.86
        Cm = (strat * s_flow * m * F) / (s_height**(7/3))
    elif f >= 100 and vm2 < 0.5:
        m = 0.9
        Cm = (strat * s_flow * m * F) / (s_height ** (7 / 3))
    else:
        Cm = (strat * s_flow * m * n * F) / (s_height**2 * ((v * dT)**(1/3)))

    # Um and d
    if f >= 100:
        if vm2 < 0.5:
            Um = 0.5
            d = 5.7
        elif vm2 <= 2:
            d = 11.4 * vm2
            Um = vm
        else:
            d = 16 * sqrt(vm2)
            Um = 2.2 * vm2
    else:
        if vm2 < 0.5:
            d = 2.48 * (1 + 0.28 * (fe**(1/3)))
            Um = 0.5
        elif vm2 <= 2:
            d = 4.95 * vm * (1 + 0.28 * (f**(1/3)))
            Um = vm
        else:
            d = 7 * sqrt(vm) * (1 + 0.28 * (f ** (1 / 3)))
            Um = vm * (1 + 0.12 * sqrt(f))
    print('Cm: %s' % Cm)
    print('d: %s' % d)
    print('Um: %s' % Um)

    # Part 2: Dispersion calculation
    Num = numpy.zeros((limit_y, limit_x))
    Xm = ((5 - F) / 4) * d * s_height
    print('Xm: %s' % Xm)
    for j in range(int(x0) + 1, int(limit_x)):
        dx = j - x0
        if dx / Xm <= 1:
            if s_height >= 2 and s_height < 11:
                S = 0.125 * (10 - s_height) + 0.125 * (s_height - 2)
            else:
                S = 3 * (dx / Xm)**4 - 8 * (dx / Xm)**3 + 6 * (dx / Xm)**2
        elif dx / Xm <= 8:
            S = 1.13 / (0.13 * (dx / Xm)**2 + 1)
        elif dx / Xm > 8 and dx / Xm <= 100:
            if F <= 1.5:
                S = (dx / Xm) / (3.58 * (dx / Xm)**2 - 35.2 * (dx / Xm) + 120)
            else:
                S = 1 / (0.1 * (dx / Xm)**2 + 2.47 * (dx / Xm) - 17.8)
        else:
            if F <= 1.5:
                S = 144.3 * (dx / Xm)**(-7/3)
            else:
                S = 37.76 * (dx / Xm)**(-7/3)
        Num[int(y0), int(j)] = (Cm * S) / pdk   # concentration at the final point

        for i in range(int(limit_y)):  # Y-axis loop.
            dy = i - y0
            if Um <= 5:
                ty = (Um * (dy**2)) / (dx**2)
            else:
                ty = (5 * (dy**2)) / (dx**2)
            S = ((1 + 5 * ty + 12.8 * ty**2 + 17 * ty**3 + 45.1 * ty**4)**2)**(-1)
            if i != y0:
                Num[i, j] = Num[int(y0), j] * S
    return Num, Cm, Um, d

# limit_x = 1000      # Limits of the area
# limit_y = 1000
# flow = 6            # Emission power
# height = 10          # Emission height
# diameter = 1.3       # Diameter of the emission source
# u_x = 500           # Coordinates of the emission
# u_y = 500
# u_pdk = 0.15        # MAC
# coef_os = 1         # Settling coefficient F
# strat = 135         # Stratification coefficient
# dT = 192            # Temperature difference between the emission and the environment
# w0_speed = 5        # Emission velocity



# flow = 6            # Emission power
# height = 10          # Emission height
# diameter = 1.3       # Diameter of the emission source
# w0_speed = 5        # Emission velocity
# u_x = 500           # Coordinates of the emission
# u_y = 500
# u_pdk = 0.15        # MAC
# strat = 135         # Stratification coefficient
# dT = 192            # Temperature difference between the emission and the environment
# coef_os = 1         # Settling coefficient F

def create_input_entry(frame, row, label_text, unit_label_text):
    label = ttk.Label(frame, text=label_text)
    label.grid(row=row, column=0, padx=5, pady=5, sticky="e")

    entry = ttk.Entry(frame)
    entry.grid(row=row, column=1, padx=5, pady=5)

    unit_label = ttk.Label(frame, text=unit_label_text)
    unit_label.grid(row=row, column=2, padx=5, pady=5)

    return entry

def on_button_click():
    input_values = {
        'limit_x': 1000,
        'limit_y': 1000,
        's_flow': float(input_entries[0].get()),
        's_height': float(input_entries[1].get()),
        's_diameter': float(input_entries[2].get()),
        's_speed': float(input_entries[3].get()),
        'F': float(input_entries[9].get()),
        'x0': float(input_entries[4].get()),
        'y0': float(input_entries[5].get()),
        'pdk': float(input_entries[6].get()),
        'strat': float(input_entries[7].get()),
        'dT': float(input_entries[8].get())
    }

    diffusion = main(**input_values)

    ax.clear()
    cmap = mpl.colors.ListedColormap(['green', 'yellow', 'orange', 'red', 'black'])
    bounds = [0.1, 0.5, 1, diffusion[1] / 0.2 / 2, diffusion[1] / 0.2 - 0.25, diffusion[1] / 0.2]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    ax.imshow(diffusion[0], cmap=cmap, norm=norm)
    canvas.draw()

def autofill_values():
    autofill_values = {
        's_flow': 6,
        's_height': 10,
        's_diameter': 1.3,
        's_speed': 5,
        'x0': 500,
        'y0': 500,
        'pdk': 0.15,
        'strat': 135,
        'dT': 192,
        'F': 1
    }

    for entry, value in zip(input_entries, autofill_values.values()):
        entry.delete(0, tk.END)
        entry.insert(0, str(value))

root = tk.Tk()
root.title("Emission Dispersion Calculator")

variables_frame = ttk.LabelFrame(root, text="Input Variables")
variables_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

unit_labels = {
    'emission_rate': 'g/s',
    'emission_height': 'm',
    'emission_diameter': 'm',
    'emission_speed': 'm/s',
    'x_coordinate': 'm',
    'y_coordinate': 'm',
    'mac': 'g/m³',
    'stratification_coefficient': '',
    'temperature_difference': '°C',
    'settling_coefficient': ''
}

input_entries = []

for i, (var, unit) in enumerate(unit_labels.items()):
    entry = create_input_entry(variables_frame, i, f"{var.capitalize()}:",
                                unit)
    input_entries.append(entry)

# flow_label = ttk.Label(variables_frame, text="Flow:")
# flow_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
# flow_entry = ttk.Entry(variables_frame)
# flow_entry.grid(row=0, column=1, padx=5, pady=5)
# flow_unit_label = ttk.Label(variables_frame, text=unit_labels['flow'])
# flow_unit_label.grid(row=0, column=2, padx=5, pady=5)

# # Аналогічно для інших полів введення
# height_label = ttk.Label(variables_frame, text="Height:")
# height_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
# height_entry = ttk.Entry(variables_frame)
# height_entry.grid(row=1, column=1, padx=5, pady=5)
# height_unit_label = ttk.Label(variables_frame, text=unit_labels['height'])
# height_unit_label.grid(row=1, column=2, padx=5, pady=5)

# diameter_label = ttk.Label(variables_frame, text="Diameter:")
# diameter_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
# diameter_entry = ttk.Entry(variables_frame)
# diameter_entry.grid(row=2, column=1, padx=5, pady=5)
# diameter_unit_label = ttk.Label(variables_frame, text=unit_labels['diameter'])
# diameter_unit_label.grid(row=2, column=2, padx=5, pady=5)

# w0_speed_label = ttk.Label(variables_frame, text="Emission Velocity:")
# w0_speed_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
# w0_speed_entry = ttk.Entry(variables_frame)
# w0_speed_entry.grid(row=3, column=1, padx=5, pady=5)
# w0_speed_unit_label = ttk.Label(variables_frame, text=unit_labels['w0_speed'])
# w0_speed_unit_label.grid(row=3, column=2, padx=5, pady=5)

# u_x_label = ttk.Label(variables_frame, text="Emission X-coordinate:")
# u_x_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
# u_x_entry = ttk.Entry(variables_frame)
# u_x_entry.grid(row=4, column=1, padx=5, pady=5)
# u_x_unit_label = ttk.Label(variables_frame, text=unit_labels['u_x'])
# u_x_unit_label.grid(row=4, column=2, padx=5, pady=5)

# u_y_label = ttk.Label(variables_frame, text="Emission Y-coordinate:")
# u_y_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
# u_y_entry = ttk.Entry(variables_frame)
# u_y_entry.grid(row=5, column=1, padx=5, pady=5)
# u_y_unit_label = ttk.Label(variables_frame, text=unit_labels['u_y'])
# u_y_unit_label.grid(row=5, column=2, padx=5, pady=5)

# u_pdk_label = ttk.Label(variables_frame, text="MAC (u_pdk):")
# u_pdk_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
# u_pdk_entry = ttk.Entry(variables_frame)
# u_pdk_entry.grid(row=6, column=1, padx=5, pady=5)
# u_pdk_unit_label = ttk.Label(variables_frame, text=unit_labels['u_pdk'])
# u_pdk_unit_label.grid(row=6, column=2, padx=5, pady=5)

# strat_label = ttk.Label(variables_frame, text="Stratification Coefficient:")
# strat_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
# strat_entry = ttk.Entry(variables_frame)
# strat_entry.grid(row=7, column=1, padx=5, pady=5)
# strat_unit_label = ttk.Label(variables_frame, text=unit_labels['strat'])
# strat_unit_label.grid(row=7, column=2, padx=5, pady=5)

# dT_label = ttk.Label(variables_frame, text="Temperature Difference:")
# dT_label.grid(row=8, column=0, padx=5, pady=5, sticky="e")
# dT_entry = ttk.Entry(variables_frame)
# dT_entry.grid(row=8, column=1, padx=5, pady=5)
# dT_unit_label = ttk.Label(variables_frame, text=unit_labels['dT'])
# dT_unit_label.grid(row=8, column=2, padx=5, pady=5)

# coef_os_label = ttk.Label(variables_frame, text="Settling Coefficient (F):")
# coef_os_label.grid(row=9, column=0, padx=5, pady=5, sticky="e")
# coef_os_entry = ttk.Entry(variables_frame)
# coef_os_entry.grid(row=9, column=1, padx=5, pady=5)
# coef_os_unit_label = ttk.Label(variables_frame, text=unit_labels['coef_os'])
# coef_os_unit_label.grid(row=9, column=2, padx=5, pady=5)

##############

button_frame = ttk.Frame(root)
button_frame.grid(row=1, column=0, pady=10)

# Кнопка для автозаповнення
autofill_button = ttk.Button(button_frame, text="Autofill Example", command=autofill_values)
autofill_button.grid(row=0, column=0)

# Кнопка для розрахунку
calculate_button = ttk.Button(button_frame, text="Calculate", command=on_button_click)
calculate_button.grid(row=1, column=0)

graph_frame = ttk.Frame(root)
graph_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

fig, ax = plt.subplots(figsize=(6, 6))
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root.mainloop()