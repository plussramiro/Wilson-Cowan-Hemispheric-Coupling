# src/preprocessing.py
from scipy import signal
import numpy as np

def bessel_filter_bandpass_and_envelope(E_t: np.ndarray, dt: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Band-pass filter excitatory activity and compute its Hilbert envelope.

    Parameters
    ----------
    E_t : np.ndarray
        Excitatory activity (time x nodes).
    dt : float
        Sampling step of recorded signals.

    Returns
    -------
    E_filt : np.ndarray
        Band-pass filtered signals.
    envelope : np.ndarray
        Hilbert envelope of the filtered signals.
    """
    # Design Bessel band-pass filter (EEG-like band 12–16 Hz in normalized freq units)
    b, a = signal.bessel(2, (12 * 2 * dt, 16 * 2 * dt), btype='bandpass')
    E_filt = signal.filtfilt(b, a, E_t, axis=0)
    envelope = np.abs(signal.hilbert(E_filt, axis=0))
    return E_filt, envelope
