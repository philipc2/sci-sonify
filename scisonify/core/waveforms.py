import numpy as np

import scipy.signal as signal


def sine_wave(freq, length, fs):
    """Sine Wave Waveform"""
    return (np.sin(2 * np.pi * np.arange(fs * length) * freq / fs)).astype(np.float32)


def square_wave(freq, length, fs):
    """Square Wave Waveform"""
    return signal.square(2 * np.pi * np.arange(fs * length) * freq / fs).astype(
        np.float32
    )


def sawtooth_wave(freq, length, fs):
    """Sawtooth Wave Waveform"""
    return signal.sawtooth(2 * np.pi * np.arange(fs * length) * freq / fs).astype(
        np.float32
    )
