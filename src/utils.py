# src/utils.py
from pathlib import Path
import numpy as np
import json
import datetime

def load_json(filename: str, config_dir: str = "configs") -> dict:
    """
    Load a JSON file from the configs folder.

    Parameters
    ----------
    filename : str
        Name of the JSON file (e.g., "global.json").
    config_dir : str
        Folder where configs are stored (default: "configs").

    Returns
    -------
    dict
        Dictionary with the loaded JSON content.
    """
    base_path = Path(__file__).resolve().parent.parent / config_dir
    with open(base_path / filename, "r") as f:
        return json.load(f)

def load_connectivity_matrices(base_path: str, group: str = "schz", scale: str = "1"):
    """
    Load structural (SC) and functional (FC) connectivity matrices.

    Parameters
    ----------
    base_path : str
        Path to folder containing the connectivity .csv files.
    group : str
        Group to load ("schz" or "ctrl").
    scale : str
        Scale identifier (e.g. "1" for 68x68).

    Returns
    -------
    SC : np.ndarray
        Structural connectivity matrix (normalized).
    FCemp : np.ndarray
        Empirical functional connectivity matrix.
    N : int
        Number of nodes (matrix size).
    """
    base = Path(base_path)
    class_matrix_sc = f"avg_sc_{group}_{scale}"
    class_matrix_fc = f"avg_fc_{group}_{scale}"

    file_path_sc = base / f"{class_matrix_sc}.csv"
    file_path_fc = base / f"{class_matrix_fc}.csv"

    SC = np.genfromtxt(file_path_sc, delimiter=",")
    FCemp = np.genfromtxt(file_path_fc, delimiter=",")
    SC /= np.max(SC)
    N = SC.shape[0]

    return SC, FCemp, N

def setup_logging_and_configs(results_root: Path, global_params: dict, plotting_params: dict, sim_params: dict):
    """
    Create timestamped log and config files for reproducibility.

    Parameters
    ----------
    results_root : Path
        Root directory where logs and configs will be saved.
    global_params : dict
        Dictionary of global parameters.
    plotting_params : dict
        Dictionary of plotting parameters.
    sim_params : dict
        Dictionary of simulation parameters.

    Returns
    -------
    log_file : Path
        Path to the log file (use it with log_message()).
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Log file path
    log_file = results_root / f"log_{timestamp}.txt"

    # Configs to save
    configs_to_save = {
        "G_params": global_params,
        "plotting_params": plotting_params,
        "sim_params": sim_params
    }

    # Save configs with timestamp
    config_file = results_root / f"used_configs_{timestamp}.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(configs_to_save, f, indent=4)

    return log_file

def log_message(message: str, log_file: Path):
    """
    Print a message and also append it to the log file.

    Parameters
    ----------
    message : str
        Message to log.
    log_file : Path
        Path to the log file.
    """
    print(message)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")