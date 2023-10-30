import numpy as np

import scipy.signal as signal



def sine_wave(freq, length, fs):
    return (np.sin(2 * np.pi * np.arange(fs * length) * freq / fs)).astype(np.float64)

def square_wave(freq, length, fs):
    return signal.square(2 * np.pi * np.arange(fs * length) * freq / fs).astype(np.float32)

def sawtooth_wave(freq, length, fs):
    return signal.sawtooth(2 * np.pi * np.arange(fs * length) * freq / fs).astype(np.float32)
