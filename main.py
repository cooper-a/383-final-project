import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.optimize import fsolve
from tqdm.auto import tqdm

# Constants (Assuming water @ 20°C)
GRAVITY = 9.81 # UNITS: m/s^2 {L/T^2}
DENSITY = 998.23 # UNITS: kg/m^3 {M/L^3}
VISCOSITY = 1.0005e-3 #UNITS: kg/(m*s) {M/(L*T)}
ROUGHNESS = 0.0025 / 1000 # UNITS: m
SIN_THETA = 1 / 150

# Tube Dimensions
TUBE_DIAMETER = 0.00794 # UNITS: m {L}
TUBE_LENGTHS_WITH_T_BOOLS = [(0.1, False), (0.2, False), (0.4, False), (0.6, False)] # UNITS: m {L}
TUBE_AREA = (TUBE_DIAMETER / 2)**2 * np.pi # UNITS: m^2 {L^2}
TUBE_WETTED_PERIMETER = 2 * np.pi * TUBE_DIAMETER / 2

# Box Dimensions
BOX_AREA = 0.0832 # UNITS: m^2 {L^2} - Length=0.32, Width=0.26
BOX_TOTAL_HEIGHT = 0.1 # UNITS: m {L}
BOX_TOTAL_VOLUME = BOX_AREA * BOX_TOTAL_HEIGHT # UNITS: m^3 {L^3}

# Heights
END_HEIGHT = 0.02 # UNITS: m {L}
TOTAL_HEIGHT_DOWN = 0.08 # UNITS: m {L}

# Losses
K_ENTRY = 0.5 
K_TJOINT = 1 + 0.075

# Time Increment
TIME_INCREMENT = 0.001 #Decide on this

# Get Methods
def get_change_in_height(v2):
    return v2 * TIME_INCREMENT * TUBE_AREA / BOX_AREA

def get_v2_velocity(relative_height, tube_length, v1, k, friction):
    # Transform Bernoulli to solve for v2
    return np.sqrt((2 * GRAVITY * relative_height + v1 ** 2) / # numerator
                    (1 + k / GRAVITY + friction * tube_length /(GRAVITY * TUBE_DIAMETER)) #denomiator 
                )

def get_v1_velocity(v2):
    return ((v2 * TUBE_AREA) / BOX_AREA)

def get_pipe_surface_area():
    return TUBE_DIAMETER ** 2 / 4 * np.pi

def get_tube_volume(tube_length):
    return tube_length * get_pipe_surface_area()

def get_box_volume():
    return BOX_TOTAL_VOLUME

def colebrook(f, reynolds_number):
    return 1 / math.sqrt(f) + 2 * math.log(ROUGHNESS / (3.7 * 4 * TUBE_AREA/TUBE_WETTED_PERIMETER) + 2.51 / (reynolds_number * math.sqrt(f)), 10)

def get_friction_coefficient(v2, tube_length): # Need to work on
    reynolds_number = get_reynolds_number(v2, tube_length)

    if reynolds_number < 2300:
        return 64/reynolds_number
    else:
        return fsolve(colebrook, 0.05, reynolds_number)[0]
    return

def get_starting_relative_height(tube_length):
    return tube_length * SIN_THETA + (END_HEIGHT + TOTAL_HEIGHT_DOWN)

def get_reynolds_number(v2, tube_length):
    return (DENSITY * v2 * tube_length) / VISCOSITY
    
# Run Experiment Method 
def run_experiment():
    for tube_length_with_t_bool in TUBE_LENGTHS_WITH_T_BOOLS:
        
        tube_length = tube_length_with_t_bool[0]
        k = K_ENTRY if not tube_length_with_t_bool[1] else K_ENTRY + K_TJOINT
        water_height = 0.1
        total_time = 0
        v1 = 0
        friction_coeff = 1 # friction is assumed to be infinite at start

        while water_height >= END_HEIGHT:
            v2 = get_v2_velocity(water_height, tube_length, v1, k, friction_coeff) # need to update parameters
            friction_coeff = get_friction_coefficient(v2, tube_length, TUBE_AREA, TUBE_DIAMETER)
            water_height -= get_change_in_height(v2)
            v1 = get_v1_velocity(v2)
            total_time += TIME_INCREMENT
        
        print(total_time)
            
# Plot Diagram Method
def plot_diagram():
    return

if __name__ == "__main__":
    run_experiment()