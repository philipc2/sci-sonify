import numpy as np

from IPython.display import Audio

from .waveforms import sine_wave, square_wave, sawtooth_wave
from .soundmaps import DiscreteNoteBins


class Sonify:
    def __init__(self, data, smap=DiscreteNoteBins, fs=44100):
        # add check for data, must be 1D
        self._data = self._normalize_data(data)
        self.smap = smap
        self.fs = fs

    def __add__(self, other):
        pass

    def _normalize_data(self, data):
        """TODO: Docstring"""
        data = np.asarray(data)
        return (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))

    def to_frequency(self):
        """Converts each data point into a frequency using a SoundMap"""
        freqs = [self.smap.get_frequency(val) for val in self._data]
        # convert to numpy?
        return freqs

    def to_waveform(self, wave="sine", note_length=1.0):
        waveform = np.empty(int(note_length * self.fs) * len(self._data))
        freqs = self.to_frequency()
        d_n = int(note_length * self.fs)

        if wave == "sine":
            _wave = sine_wave
        elif wave == "square":
            _wave = square_wave
        elif wave == "sawtooth":
            _wave = sawtooth_wave
        else:
            raise ValueError("TODO")

        # improve this
        for i, freq in enumerate(freqs):
            waveform[(i * (d_n)) : ((i + 1) * (d_n))] = _wave(
                freq, note_length, self.fs
            )

        return waveform

    def to_audio(self, wave="sine", note_length=1.0):
        """TODO: Docstring"""
        waveform = self.to_waveform(wave, note_length)
        return Audio(waveform, rate=self.fs)
