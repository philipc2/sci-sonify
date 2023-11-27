import numpy as np

from IPython.display import Audio

from .waveforms import sine_wave, square_wave, sawtooth_wave
from .soundmaps import DiscreteNoteBins

from .envelope import EnvelopeADSR


class Sonify:
    def __init__(self, data, smap=None, envelope=None, fs=44100):
        # add check for data, must be 1D
        self._data = self._normalize_data(data)
        self.n_notes = len(data)
        self.fs = fs

        if envelope is None:
            self.envelope = EnvelopeADSR()
        else:
            self.envelope = envelope

        if smap is None:
            self.smap = DiscreteNoteBins.from_key()
        else:
            self.smap = smap

    def _normalize_data(self, data):
        """TODO: Docstring"""
        data = np.asarray(data)

        return (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))

    def to_frequency(self):
        """Converts each data point into a frequency using a SoundMap"""
        freqs = [self.smap.get_frequency(val) for val in self._data]
        return freqs

    def to_waveform(self, wave="sine", note_length=1.0):
        if wave == "sine":
            _wave = sine_wave
        elif wave == "square":
            _wave = square_wave
        elif wave == "sawtooth":
            _wave = sawtooth_wave
        else:
            raise ValueError("TODO")

        # empty array to store waveform
        waveform = np.empty(int(note_length * self.fs) * len(self._data))

        # obtain the frequency (note) of each data point
        freqs = self.to_frequency()

        # number of samples per data point
        n_samples = int(note_length * self.fs)

        envelope_amplitudes = self.envelope.get_amplitudes(np.linspace(0, 1, n_samples))

        for i, freq in enumerate(freqs):
            # indices to slice waveform
            start = i * n_samples
            end = (i + 1) * n_samples

            # sample wave and apply envelope amplitudes
            waveform[start:end] = (
                _wave(freq, note_length, self.fs) * envelope_amplitudes
            )

        return waveform

    def to_audio(self, wave="sine", note_length=1.0):
        """TODO: Docstring"""
        waveform = self.to_waveform(wave, note_length)
        return Audio(waveform, rate=self.fs)
