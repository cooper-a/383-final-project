import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import math
from scipy.optimize import fsolve
from tqdm.auto import tqdm

# Constants (Assuming water @ 20°C)
GRAVITY = 9.81 # UNITS: m/s^2 {L/T^2}
DENSITY = 998 # UNITS: kg/m^3 {M/L^3}
VISCOSITY = 1.002e-3 #UNITS: kg/(m*s) {M/(L*T)}
ROUGHNESS = 0.0015 # UNITS: N/A
MINOR_LOSS_FACTOR = 1 #not sure
SIN_THETA = 1 / 150

# Tube Dimensions
TUBE_DIAMETER = 0.00794 # UNITS: m {L}
TUBE_LENGTHS = [0.2, 0.3, 0.4, 0.4] # UNITS: m {L}
TUBE_AREA = (TUBE_DIAMETER / 2)**2 * np.pi # UNITS: m^2 {L^2}

# Box Dimensions
BOX_AREA = 0.0832 # UNITS: m^2 {L^2} - Length=0.32, Width=0.26
BOX_TOTAL_HEIGHT = 0.1 # UNITS: m {L}
BOX_TOTAL_VOLUME = BOX_AREA * BOX_TOTAL_HEIGHT # UNITS: m^3 {L^3}

# Heights
END_HEIGHT = 0.02 # UNITS: m {L}
TOTAL_HEIGHT_DOWN = 0.08 # UNITS: m {L}

# Losses
# ROUGHNESS =  # WHERE DO WE FIND THIS ????
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
                    (k / GRAVITY + tube_length * friction /(GRAVITY * TUBE_DIAMETER) + 1) #denomiator 
                )

def get_pipe_surface_area():
    return TUBE_DIAMETER ** 2 / 4 * np.pi

def get_tube_volume(tube_length):
    return tube_length * get_pipe_surface_area()

def get_box_volume():
    return BOX_TOTAL_VOLUME

def get_friction_coefficient(v2, tube_length, tube_area, tube_diameter): # Need to work on
    reynolds_number = get_reynolds_number(v2, tube_length)
    # get
    return

def get_starting_relative_height(tube_length):
    return tube_length * SIN_THETA + (END_HEIGHT + TOTAL_HEIGHT_DOWN)

def get_reynolds_number(v2, tube_length):
    return (DENSITY * v2 * tube_length) / VISCOSITY
    
# Run Experiment Method 
def run_experiment():
    water_height = 0.1

    tube_length = TUBE_LENGTHS[0] # CHANGE THIS LATER!!

    while water_height > 0.02: 
        v2 = get_v2_velocity(water_height, tube_length)
        friction_coeff = get_friction_coefficient(v2, tube_length, TUBE_AREA, TUBE_DIAMETER)
        water_height =- get_change_in_height(water_height, tube_length, v1, k, get_friction_coefficient())

        cur_v2 = calculate_v2_velocity()

# Plot Diagram Method
def plot_diagram():
    return

if __name__ == "__main__":
    calculate_height()