# src/model.py
import numpy as np
from numba import njit

@njit
def S(x, mu, sigma):
    # Sigmoid with explicit params (no globals)
    return 1.0 / (1.0 + np.exp(-(x - mu) / sigma))

@njit
def wc(t, X, CM, P, Q, tau_ip, params):
    """
    Wilson-Cowan with inhibitory plasticity.

    params is a tuple:
      (mu, sigma, a_ee, a_ie, a_ii, rE, rI, rhoE, sqdtD, tauE, tauI)
    """
    mu, sigma, a_ee, a_ie, a_ii, rE, rI, rhoE, sqdtD, tauE, tauI = params

    E, I, a_ei_0 = X
    E = np.ascontiguousarray(E)

    # noise per node
    noise = np.random.normal(0.0, sqdtD, E.shape[0])

    dE = (-E + (1.0 - rE * E) * S(a_ee * E - a_ei_0 * I + np.dot(CM, E) + P + noise, mu, sigma)) / tauE
    dI = (-I + (1.0 - rI * I) * S(a_ie * E - a_ii * I + Q, mu, sigma)) / tauI
    da = (I * (E - rhoE)) / tau_ip

    return np.vstack((dE, dI, da))

@njit
def simulate(time_array, Var_init, CM, P, Q, tau_ip, params, dtSim, downsamp):
    """
    Integrate over time_array with fixed step dtSim.
    Stores every `downsamp` internal steps.
    """
    Var = Var_init.copy()
    N = Var.shape[1]
    out_len = len(time_array) // downsamp
    Var_t = np.zeros((out_len, 3, N))

    k = 0
    for i, t in enumerate(time_array):
        Var += dtSim * wc(t, Var, CM, P, Q, tau_ip, params)
        if i % downsamp == 0:
            Var_t[k] = Var
            k += 1

    return Var, Var_t

def build_hemispheric_coupling(SC: np.ndarray, G1: float, G2: float) -> np.ndarray:
    """
    Construye la matriz de acople hemisférico:
      CM = kron([[G1, G2], [G2, G1]], Ones(N/2, N/2)) * SC
    """
    N = SC.shape[0]
    assert N % 2 == 0, "Se espera número par de regiones (hemisferios del mismo tamaño)."
    A = np.array([[G1, G2], [G2, G1]], dtype=float)
    B = np.ones((N // 2, N // 2), dtype=float)
    return np.kron(A, B) * SC