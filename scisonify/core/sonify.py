import numpy as np

from typing import Optional

from IPython.display import Audio

from .waveforms import sine_wave, square_wave, sawtooth_wave
from .soundmaps import SoundMap, DiscreteNoteBins

from .envelope import EnvelopeADSR


class Sonify:
    """Class for performing Data Sonification.

    Turns a 1-dimensional array-like data variable into musical notes.

    Parameters
    ----------
    data: array-like, required
        1-D data variable to perform data sonification on
    smap: SoundMap, optional
        SoundMap for mapping data to musical notes
    envelope: EnvelopeADSR, optional
        Envelope to apply to each note
    fs: int, optional
        Sampling Frequency

    """

    def __init__(
        self,
        data: np.ndarray,
        smap: Optional[SoundMap] = None,
        envelope: Optional[EnvelopeADSR] = None,
        fs: Optional[int] = 44100,
    ):
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
        """Normalizes a one-dimensional array-like data variable into the range [0, 1]

        Parameters
        ----------
        data: array-like
            1-D array-like data variable to normalize

        Returns
        -------
        data_norm: np.ndarray
            1-D normalized data variable
        """
        data = np.asarray(data)
        if data.ndim > 1:
            raise ValueError(
                f"Expected data with 1 dimension, but received {data.ndim} dimensions."
            )

        if np.all(np.isclose(data, data[0])):
            # uniform data maps to all ones to avoid floating point division
            data_norm = np.ones_like(data)
        else:
            # normalize data to [0, 1]
            data_norm = (data - data.min(axis=0)) / (
                data.max(axis=0) - data.min(axis=0)
            )

        return data_norm

    def to_waveform(self, wave="sine", note_length=1.0):
        """Converts a normalized data variable into a waveform.

        Parameters
        ----------
        wave: optional, str
            Wave to use for oscillator, one of ['sine', 'square', 'sawtooth']

        Returns
        -------
        waveform: np.ndarray
            An array of length int(note_length * self.fs) * len(self._data) containing len(self._data) of duration
            note_length computed using the provided wave.

        """
        if wave == "sine":
            _wave = sine_wave
        elif wave == "square":
            _wave = square_wave
        elif wave == "sawtooth":
            _wave = sawtooth_wave
        else:
            raise ValueError(
                f"Invalid wave {wave}:, expected one of 'sine', 'square', or 'sawtooth"
            )

        # empty array to store waveform
        waveform = np.empty(int(note_length * self.fs) * len(self._data))

        # obtain the frequency (note) of each data point
        freqs = self.to_frequencies()

        # number of samples per data point
        n_samples = int(note_length * self.fs)

        # obtain the amplitudes to use when applying envelope to each note
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
        """Returns an interactive Audio object for use in Notebooks"""
        waveform = self.to_waveform(wave, note_length)
        return Audio(waveform, rate=self.fs)

    def to_notes(self):
        """Each data point represented as a Musical Note computed using the stored SoundMap"""
        return [self.smap.get_note(val) for val in self._data]

    def to_frequencies(self):
        """Each data point represented as a frequency (hz) computed using the stored SoundMap"""
        freqs = [self.smap.get_frequency(val) for val in self._data]
        return freqs

    def plot(
        self,
        x=None,
        xlabel=None,
        title=None,
        figsize=(10, 5),
        marker="o",
        linewidth=0,
        **kwargs,
    ):
        """Plots each data point in terms of its Musical Note representation"""
        import matplotlib.pyplot as plt

        plt.figure(figsize=figsize)

        if x is None:
            x = range(len(self._data))

        note_values = np.linspace(0, 1, len(self.smap.notes))
        order_notes = {note: val for note, val in zip(self.smap.notes, note_values)}

        notes_ordered = [order_notes[note] for note in self.to_notes()]

        plt.plot(x, notes_ordered, marker=marker, linewidth=linewidth, **kwargs)
        plt.yticks(note_values, self.smap.notes)
        plt.ylabel("Note")
        plt.xlabel(xlabel)
        plt.title(title)


class SonifyAccessor:
    """Accessor to support Data Sonification when linked to another data store object (i.e. Xarray DataArray,
    Pandas Series)"""

    def __init__(self, obj):
        self._obj = obj
        self._sonify_cache = None

    def __call__(
        self, wave="sine", note_length=1.0, smap=None, envelope=None, fs=44100
    ):
        sonify = self._construct_sonify_obj(smap, envelope, fs)
        self._sonify_cache = sonify
        return sonify.to_audio(wave, note_length)

    def _construct_sonify_obj(self, smap, envelope, fs):
        """Attempts to construct a ``Sonify`` instance from the parent data structure."""

        data = self._obj.values

        sonify = Sonify(data=data, smap=smap, envelope=envelope, fs=fs)
        return sonify

    def plot(
        self,
        x=None,
        xlabel=None,
        title=None,
        figsize=(10, 5),
        marker="o",
        linewidth=0,
        **kwargs,
    ):
        """Plots each data point in terms of its Musical Note representation"""
        if self._sonify_cache is None:
            raise ValueError("TODO")

        return self._sonify_cache.plot(
            x, xlabel, title, figsize, marker, linewidth, **kwargs
        )
