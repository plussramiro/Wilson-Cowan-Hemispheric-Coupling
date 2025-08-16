# src/metrics.py
from numba import njit
import numpy as np

@njit
def calc_corr_dist(A, B):
    n = A.shape[0]
    size = (n * (n - 1)) // 2
    v1 = np.empty(size)
    v2 = np.empty(size)
    idx = 0

    for i in range(n):
        for j in range(i):
            v1[idx] = A[i, j]
            v2[idx] = B[i, j]
            idx += 1

    # Media
    m1 = np.mean(v1)
    m2 = np.mean(v2)

    # Correlación de Pearson manual
    cov = 0.0
    var1 = 0.0
    var2 = 0.0
    for i in range(size):
        diff1 = v1[i] - m1
        diff2 = v2[i] - m2
        cov += diff1 * diff2
        var1 += diff1 ** 2
        var2 += diff2 ** 2

    corr = cov / np.sqrt(var1 * var2)

    # Distancia Euclídea Media (RMSE)
    rmse = 0.0
    for i in range(size):
        rmse += (v1[i] - v2[i]) ** 2
    rmse = np.sqrt(rmse / size)

    return corr, rmse