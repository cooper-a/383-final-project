import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
from scipy.optimize import fsolve
from tqdm.auto import tqdm
import math

# Constants
GRAVITY = 9.81 # UNITS: m/s^2 {L/T^2}
DENSITY = 998 # UNITS: kg/m^3 {M/L^3}
VISCOSITY = 1.002e-3 #UNITS: kg/(m*s) {M/(L*T)}
ROUGHNESS = 0.0025 # UNITS: N/A
MINOR_LOSS_FACTOR = 1 #not sure

# Tube Dimensions
TUBE_DIAMETER = 0.00794 # UNITS: m {L}
TUBE_LENGTHS = [0.2, 0.3, 0.4, 0.4] # UNITS: m {L}
TUBE_AREA = (TUBE_DIAMETER / 2)**2 * np.pi # UNITS: m^2 {L^2}

# Box Dimensions
BOX_LENGTH = 0.32 # UNITS: m {L}
BOX_WIDTH = 0.26 # UNITS: m {L}
BOX_TOTAL_HEIGHT = 0.1 # UNITS: m {L}
BOX_TOTAL_VOLUME = BOX_LENGTH * BOX_TOTAL_HEIGHT * BOX_TOTAL_HEIGHT # UNITS: m^3 {L^3}


