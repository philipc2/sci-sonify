# todo

import numpy as np
import librosa


class DiscreteNoteBins:

    def __init__(self, notes):

        self._notes = notes
        self._bins = self._construct_bins(len(notes))

    @classmethod
    def from_key(cls, key = "C:maj", octave_range = (4, 4)):
        key_notes = librosa.key_to_notes(key)

        notes = []
        for i in range(octave_range[0], octave_range[1] + 1):
            notes.extend([note + str(i) for note in key_notes])

        return cls(notes)

    def get_frequency(self, value):
        note = self.get_note(value)
        return librosa.note_to_hz(note)

    def get_note(self, value):
        note_idx = np.searchsorted(self._bins, value, side='left') - 1
        return self._notes[note_idx]



    def _construct_bins(self, n_notes):
        """Constructs a discrete set of bins, which map normalized data values to musical notes.

        Example
        -------
        [0, 1/3) [1/3, 2/3) [2/3, 1]
           A         B          C

        """
        return np.linspace(0, 1, n_notes + 1)
