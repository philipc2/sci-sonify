# todo

import numpy as np
import librosa


class SoundMap:
    # define what every "soundmap" should have
    pass


class DiscreteNoteBins:
    # todo, make inherit from SoundMap

    def __init__(self, notes):
        self._notes = notes
        self._bins = self._construct_bins(len(notes))

    @classmethod
    def from_key(cls, key="C:maj", octave_range=(4, 4)):
        """TODO"""
        key_notes = librosa.key_to_notes(key)

        notes = []
        for i in range(octave_range[0], octave_range[1] + 1):
            notes.extend([note + str(i) for note in key_notes])

        notes = np.array(notes)
        freqs = np.array([librosa.note_to_hz(note) for note in notes])

        ordered_indices = freqs.argsort()

        return cls(notes[ordered_indices])

    @classmethod
    def from_midi(cls, start_note, end_note):
        """TODO"""
        # ensure end_node > start_note

        note_range = np.arange(start_note, end_note + 1)

        notes = [librosa.midi_to_note(note) for note in note_range]

        return cls(notes)

    @classmethod
    def from_notes(cls, start_note, end_note):
        """TODO"""

        start_note_midi = librosa.note_to_midi(start_note)
        end_note_midi = librosa.note_to_midi(end_note)

        return cls.from_midi(start_note_midi, end_note_midi)

    def get_frequency(self, value):
        note = self.get_note(value)
        return librosa.note_to_hz(note)

    def get_note(self, value):
        note_idx = np.searchsorted(self._bins, value, side="left") - 1
        return self._notes[note_idx]

    def _construct_bins(self, n_notes):
        """Constructs a discrete set of bins, which map normalized data values to musical notes.

        Example
        -------
        [0, 1/3) [1/3, 2/3) [2/3, 1]
           A         B          C

        """
        bins = np.linspace(0, 1, n_notes + 1)
        bins[0] -= 0.0001
        bins[-1] += 0.001

        return bins
