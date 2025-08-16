# src/plotting.py
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import signal
import numpy as np

def plot_simulation_results_global(
    time, E_t, E_filt, envelope, SC, FC, FCemp,
    G, sim, corr, dist, g, sim_folder,
    xlim_zoom, ylim_exc_activity, xlim_global, ylim_global
):
    """
    Plot and save simulation results: activity, filtered signals, SC, and FC matrices.
    """
    fig = plt.figure(figsize=(18, 14))
    gs = gridspec.GridSpec(3, 3, height_ratios=[1, 1, 1.4], hspace=0.35, wspace=0.28)

    # (a) Excitatory activity
    ax1 = plt.subplot(gs[0, :])
    ax1.plot(time, E_t[:, ::5])
    ax1.set_xlim(xlim_zoom)
    ax1.set_ylim(ylim_exc_activity)
    ax1.set_title("(a) Excitatory activity", fontsize=20)

    # (b) Filtered signal and Hilbert envelope
    ax2 = plt.subplot(gs[1, :])
    ax2.plot(time, E_filt[:, :3], alpha=0.5, label="Filtered")
    ax2.plot(time, envelope[:, :3], label="Envelope")
    ax2.set_xlim(xlim_global)
    ax2.set_ylim(ylim_global)
    ax2.legend(loc="upper right")
    ax2.set_title("(b) Filtered signal and Hilbert envelope", fontsize=20)

    # (c) Structural Connectivity
    ax3 = plt.subplot(gs[2, 0])
    im3 = ax3.imshow(SC, cmap="terrain_r", vmin=0, vmax=1)
    ax3.set_title("(c) Structural Connectivity Matrix (Normalized)", fontsize=16, pad=12)
    plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

    # (d) Simulated FC
    ax4 = plt.subplot(gs[2, 1])
    im4 = ax4.imshow(FC, cmap="jet", vmin=-1, vmax=1)
    ax4.set_title("(d) Simulated Functional Connectivity", fontsize=16, pad=12)
    plt.colorbar(im4, ax=ax4, fraction=0.046, pad=0.04)

    # (e) Empirical FC
    ax5 = plt.subplot(gs[2, 2])
    im5 = ax5.imshow(FCemp, cmap="jet", vmin=-1, vmax=1)
    ax5.set_title("(e) Empirical Functional Connectivity", fontsize=16, pad=12)
    plt.colorbar(im5, ax=ax5, fraction=0.046, pad=0.04)

    # Global title
    plt.suptitle(
        f"G: {G:.2f}, Sim: {sim}\nCorrelation: {corr:.4f}, Distance: {dist:.4f}",
        fontsize=20, y=0.96
    )
    
    #plt.tight_layout(rect=[0, 0, 1, 0.94])

    # Save
    base_name = os.path.join(sim_folder, f"{g}_sim{sim}_G{G:.2f}")
    fig.savefig(f"{base_name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(f"{base_name}.pdf", bbox_inches="tight")
    plt.close(fig)

def plot_simulation_results_hemispheric(
    time, E_t, E_filt, envelope, SC, FC, FCemp,
    G1, G2, sim, corr, dist, g, sim_folder,
    xlim_zoom, ylim_exc_activity, xlim_global, ylim_global
):
    """
    Plot and save simulation results: activity, filtered signals, SC, and FC matrices.
    """
    fig = plt.figure(figsize=(18, 14))
    gs = gridspec.GridSpec(3, 3, height_ratios=[1, 1, 1.4], hspace=0.35, wspace=0.28)

    # (a) Excitatory activity
    ax1 = plt.subplot(gs[0, :])
    ax1.plot(time, E_t[:, ::5])
    ax1.set_xlim(xlim_zoom)
    ax1.set_ylim(ylim_exc_activity)
    ax1.set_title("(a) Excitatory activity", fontsize=20)

    # (b) Filtered signal and Hilbert envelope
    ax2 = plt.subplot(gs[1, :])
    ax2.plot(time, E_filt[:, :3], alpha=0.5, label="Filtered")
    ax2.plot(time, envelope[:, :3], label="Envelope")
    ax2.set_xlim(xlim_global)
    ax2.set_ylim(ylim_global)
    ax2.legend(loc="upper right")
    ax2.set_title("(b) Filtered signal and Hilbert envelope", fontsize=20)

    # (c) Structural Connectivity
    ax3 = plt.subplot(gs[2, 0])
    im3 = ax3.imshow(SC, cmap="terrain_r", vmin=0, vmax=1)
    ax3.set_title("(c) Structural Connectivity Matrix (Normalized)", fontsize=16, pad=12)
    plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

    # (d) Simulated FC
    ax4 = plt.subplot(gs[2, 1])
    im4 = ax4.imshow(FC, cmap="jet", vmin=-1, vmax=1)
    ax4.set_title("(d) Simulated Functional Connectivity", fontsize=16, pad=12)
    plt.colorbar(im4, ax=ax4, fraction=0.046, pad=0.04)

    # (e) Empirical FC
    ax5 = plt.subplot(gs[2, 2])
    im5 = ax5.imshow(FCemp, cmap="jet", vmin=-1, vmax=1)
    ax5.set_title("(e) Empirical Functional Connectivity", fontsize=16, pad=12)
    plt.colorbar(im5, ax=ax5, fraction=0.046, pad=0.04)

    # Global title
    plt.suptitle(
        f"(G1,G2) = ({G1:.2f},{G2:.2f}), Sim: {sim}\nCorrelation: {corr:.4f}, Distance: {dist:.4f}",
        fontsize=20, y=0.96
    )
    
    #plt.tight_layout(rect=[0, 0, 1, 0.94])

    # Save
    base_name = os.path.join(sim_folder, f"{g}_sim{sim}_G1_{G1:.2f}_G2_{G2:.2f}")
    fig.savefig(f"{base_name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(f"{base_name}.pdf", bbox_inches="tight")
    plt.close(fig)
