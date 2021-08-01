import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import fsolve
from tqdm.auto import tqdm
import math

BIN_WIDTH_M = 0.32
BIN_LENGTH_M = 0.26
BIN_HEIGHT_M = 0.08

TUBE_DIAMETER_M = 0.00794
TUBE_LENGTHS_M = [0.2, 0.3, 0.4, 0.6]

END_HEIGHT_M = 0.02
TOTAL_HEIGHT_CHANGE_M = 0.08
START_HEIGHT_M = END_HEIGHT_M + TOTAL_HEIGHT_CHANGE_M

WATER_DYNANIC_MU = 1.0005e-3
WATER_RHO = 998.23
GRAVITY = 9.81

ROUGHNESS = 0.75
FRICTION_FACTOR = 0.5
K_ENTRY = 0.5
K_TJOINT = 1

SIN_THETA_RADS = 1 / 150

TIMESTEP_S = 1e-2

EXPERIMENTAL_RESULTS = [199, 214, 266, 288]

AX_INDICES = {0: (0, 0), 1: (0, 1), 2: (1, 0), 3: (1, 1)}


def get_bin_volume_m3():
    return BIN_WIDTH_M * BIN_LENGTH_M * (BIN_HEIGHT_M + END_HEIGHT_M)


def get_pipe_area():
    return np.pi * TUBE_DIAMETER_M ** 2 / 4


def get_tube_volume_m3(L):
    return get_pipe_area() * L


def get_start_relative_height_m(L):
    return SIN_THETA_RADS * L + START_HEIGHT_M


def get_velocity_v2_m_per_s(v1, h, L, k_tot, f):
    numerator = v1 ** 2 + 2 * GRAVITY * h
    denominator = 1 + k_tot / GRAVITY + f * L / (GRAVITY * TUBE_DIAMETER_M)

    return np.sqrt(numerator / denominator)


def get_reynolds_number(rho, u, L, mu):
    return rho * u * L / mu


def colebrook(f_coeff, Re):
    return 1 / math.sqrt(f_coeff) + 2 * math.log(ROUGHNESS / 3.7 + 2.51 / (Re * math.sqrt(f_coeff)), 10)


def get_friction_coeff(Re):
    return fsolve(colebrook, 0.01, Re)


def run_simulation(L, with_t_joint=False):
    bin_volume_m3 = get_bin_volume_m3()
    tube_volume_m3 = get_tube_volume_m3(L)

    total_volume_m3 = bin_volume_m3 + tube_volume_m3

    start_relative_height_m = get_start_relative_height_m(L)

    absolute_height_m = START_HEIGHT_M

    elapsed_time_s = 0
    v1 = 0
    relative_height_m = start_relative_height_m
    prev_relative_height_m = relative_height_m
    total_delta_h_m = 0
    PIPE_AREA_M2 = get_pipe_area()
    dt = TIMESTEP_S
    previous_volume_m3 = total_volume_m3

    k_tot = K_ENTRY
    if with_t_joint:
        k_tot += K_TJOINT

    columns = ["t", "v1", "v2", "h", "V", "dh", "dV"]
    data = []
    computed_f = 1  # assume infinite friction at start?

    while absolute_height_m >= END_HEIGHT_M and elapsed_time_s < 500:
        v2 = get_velocity_v2_m_per_s(v1, relative_height_m, L, k_tot, f=computed_f)
        dV = v2 * PIPE_AREA_M2 * dt
        current_volume_m3 = previous_volume_m3 - dV
        dh = dV / (BIN_WIDTH_M * BIN_LENGTH_M)
        relative_height_m = prev_relative_height_m - dh
        absolute_height_m -= dh
        v1 = dh / dt

        data.append([elapsed_time_s, v1, v2, absolute_height_m, current_volume_m3, dh, dV])

        previous_volume_m3 = current_volume_m3
        prev_relative_height_m = relative_height_m
        elapsed_time_s += dt
        total_delta_h_m += dh

        reynolds = get_reynolds_number(WATER_RHO, v2, TUBE_DIAMETER_M, WATER_DYNANIC_MU)
        computed_f = get_friction_coeff(reynolds)[0]

    df = pd.DataFrame(data=data, columns=columns)
    return df


def plot_height_vs_time_superimposed(tube_lengths=TUBE_LENGTHS_M, with_t_joint=False):
    fig, ax = plt.subplots()

    fig.suptitle("Water height vs time for different tubing lengths")

    for i, L in enumerate(tube_lengths):
        df = run_simulation(L, with_t_joint)

        x = df["t"]
        y = df["h"]
        label = f"{round(L, 1)}m"
        ax.plot(x, y, label=label)

        total_time_s = round(x.iloc[-1], 2)
        difference_with_experimental_results_s = round(EXPERIMENTAL_RESULTS[i] - total_time_s, 3)
        print(f"Total time for L={round(L, 1)}m: {total_time_s}s; difference={difference_with_experimental_results_s}s")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Water height (m)")

    ax.set_ylim([0.01, 0.11])

    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper right", borderaxespad=0.)
    plt.grid(True)
    plt.show()


def plot_avg_velocity_vs_length():
    tube_lengths = []
    average_velocities = []

    for i in tqdm(range(1, 20)):
        L = i / 10

        df = run_simulation(L)

        tube_lengths.append(L)
        average_velocities.append(np.mean(df["v2"]))

    plt.scatter(tube_lengths, average_velocities, c="r", alpha=0.5)
    plt.title("Average outlet velocity vs tube length")
    plt.xlabel("Tube length (m)")
    plt.ylabel("Average outlet velocity")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    plot_height_vs_time_superimposed()
    plot_avg_velocity_vs_length()
    plot_height_vs_time_superimposed(tube_lengths=[0.2, 0.4], with_t_joint=True)