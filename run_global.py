import numpy as np
import os
from pathlib import Path
from src.utils import load_json, load_connectivity_matrices, setup_logging_and_configs, log_message
from src.model import simulate
from src.preprocessing import bessel_filter_bandpass_and_envelope
from src.metrics import calc_corr_dist
from src.plotting import plot_simulation_results_global


# ========================== Load configs ==========================
global_params = load_json("global.json")
plotting_params = load_json("plotting_parameters.json")
sim_params = load_json("simulation_parameters.json")
# ==================================================================

scale = sim_params["scale"] # parcellation scale (e.g., "1" → 68x68, "2" → ...)
group = sim_params["group"] # subject group(s) to simulate ("ctrl", "schz", or both)
groups = [group] if isinstance(group, str) else group
base_path = "data/avg_conn_matrices_no_subcortical" # relative path to connectivity matrices

# ========================== Model constants ==========================
mu, sigma = sim_params["mu"], sim_params["sigma"] # mu: threshold of sigmoid, sigma: slope (steepness)
E0, I0 = sim_params["E0"], sim_params["I0"]       # initial excitatory and inhibitory activity
rE, rI = sim_params["rE"], sim_params["rI"]       # refractory parameters for excitatory and inhibitory populations
rhoE = sim_params["rhoE"]                         # excitatory threshold

a_ee   = sim_params["a_ee"]                       # E → E coupling
a_ei_0 = sim_params["a_ei_0"]                     # I → E initial coupling (adaptive variable)
a_ie   = sim_params["a_ie"]                       # E → I fixed coupling
a_ii   = sim_params["a_ii"]                       # I → I coupling
num_simuls = sim_params["num_simuls"]             # number of independent simulations to run
P_init = sim_params["P_init"]                     # initialization parameters for external input P (distribution and values)
Q_init = sim_params["Q_init"]                     # initialization parameters for external input Q (distribution and values)
# ====================================================================

# ========================== Time constants ==========================
tauE = sim_params["tauE"]         # excitatory population time constant
tauI = sim_params["tauI"]         # inhibitory population time constant
tau_ip = sim_params["tau_ip"]     # time constant of inhibitory plasticity
# ====================================================================

# ========================== Time parameters ==========================
dt = sim_params["dt"]             # integration step for recorded signals
dtSim = sim_params["dt_sim"]      # internal integration step for numerical solver
downsamp = int(dt / dtSim)        # downsampling factor (number of internal steps per output step)
# ====================================================================

# ========================== Noise and coupling ==========================
D = sim_params["D"]                   # noise diffusion coefficient
sqdtD = D / np.sqrt(dtSim)            # scaled noise term (variance adapted to dtSim)
G_vals = global_params["G"]           # list of global coupling values to explore
# ========================================================================

# ========================== Simulation time ==========================
tTrans = sim_params["t_trans"]            # transient period (discarded from analysis)
tstop = sim_params["t_stop"]              # total simulation time
timeTrans = np.arange(0, tTrans, dtSim)   # time array for transient period
timeSim = np.arange(0, tstop, dtSim)      # time array for simulation with internal step
time = np.arange(0, tstop, dt)            # time array for recorded signals
# =====================================================================

# ========================== Plotting config ==========================
save_figures = plotting_params["save_figures"]          # whether to save generated figures
save_fc_txt = plotting_params["save_fc_txt"]            # whether to save simulated FC matrices as .txt
save_signals_txt = plotting_params["save_signals_txt"]  # whether to save raw signals and envelopes as .txt

xlim_zoom = (tstop - 1, tstop)                                   # x-axis range for excitatory activity (zoom)
ylim_exc_activity = tuple(plotting_params["ylim_exc_activity"])  # y-axis range for excitatory activity (zoom)

xlim_global = (0, tstop)                            # x-axis range for filtered signal and envelope
ylim_global = tuple(plotting_params["ylim_global"]) # y-axis range for filtered signal and envelope
# =====================================================================

params = (
    mu, sigma,
    a_ee, a_ie, a_ii,
    rE, rI, rhoE,
    sqdtD, tauE, tauI
)

results_root = Path("results_global")
results_root.mkdir(exist_ok=True)   # crea la carpeta si no existe
output_file = results_root / "corr_dist_results.txt"

header = "group,G,simulation,correlation,distance\n"

if not os.path.exists(output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header)

log_file = setup_logging_and_configs(results_root, global_params, plotting_params, sim_params) # Saving Log and Parameters Used

with open(output_file, "a", encoding="utf-8") as f:       
    for g in groups:

        SC, FCemp, N = load_connectivity_matrices(base_path, group=g, scale=scale)

        group_folder = results_root / g
        group_folder.mkdir(exist_ok=True)

        results = [] 

        for sim in range(1, num_simuls + 1):
            sim_folder = group_folder / f"sim_{sim}"
            sim_folder.mkdir(exist_ok=True)

            for G in G_vals:
                CM = SC * G                     # Scale the structural connectivity (SC) matrix by the global coupling G

                if P_init["dist"] == "uniform": P = np.random.uniform(P_init["low"], P_init["high"], N)   # Initialize external input P with a uniform distribution across nodes

                if Q_init["dist"] == "normal": Q = np.random.normal(Q_init["mean"], Q_init["std"], N)     # Initialize external input Q with a normal distribution across nodes

                Var = np.array([E0, I0, a_ei_0])[:, None] * np.ones((1, N))  # Initial state vector: excitatory, inhibitory activity, and I→E coupling (replicated for all nodes)

                tau_ip_temp = 0.05              # Temporary fast time constant for inhibitory plasticity (used for transient stabilization)
                Var, _ = simulate(timeTrans, Var, CM, P, Q, tau_ip_temp, params, dtSim, downsamp) # Transient simulation with fast inhibitory plasticity → helps stabilize dynamics
                Var, _ = simulate(timeTrans, Var, CM, P, Q, tau_ip_temp / 2, params, dtSim, downsamp) # Second transient with slightly slower plasticity → smoother convergence before main run

                Var, Var_t = simulate(timeSim, Var, CM, P, Q, tau_ip, params, dtSim, downsamp) # Main simulation over analysis period with biologically plausible tau_ip

                E_t = Var_t[:, 0, :]                                             # Extract excitatory activity from simulated state variables

                E_filt, envelope = bessel_filter_bandpass_and_envelope(E_t, dt)  # Apply Bessel band-pass filter and compute Hilbert envelope

                FC = np.corrcoef(envelope, rowvar=False)       # Compute simulated functional connectivity (Pearson correlation across envelopes)

                corr, dist = calc_corr_dist(FC, FCemp)         # Compare simulated FC with empirical FC (correlation + distance metrics)

                results.append([g, G, sim, corr, dist])       

                if save_figures:
                    plot_simulation_results_global(time, E_t, E_filt, envelope, SC, FC, FCemp, G, sim, corr, dist, g, sim_folder, xlim_zoom, ylim_exc_activity, xlim_global, ylim_global)
                if save_fc_txt:
                    np.savetxt(os.path.join(sim_folder, f"FC_G{G:.2f}_sim{sim}_{g}.txt"), FC, fmt="%.6f", delimiter=",")
                if save_signals_txt:
                    np.savetxt(os.path.join(sim_folder, f"E_t_G_{G:.2f}_sim{sim}_{g}.txt"), E_t, fmt="%.6f", delimiter=",")
                    np.savetxt(os.path.join(sim_folder, f"envelope_G_{G:.2f}_sim{sim}_{g}.txt.txt"), envelope, fmt="%.6f", delimiter=",")

                f.write(f"{g},{G:.4f},{sim},{corr:.6f},{dist:.6f}\n")

                log_message(f"[INFO] Done global model with G = {G:.2f} for group = {g}, sim = {sim}", log_file)





