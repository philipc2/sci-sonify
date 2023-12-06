import numpy as np
import librosa


class SoundMap:
    """Base class for a SoundMap"""

    pass


class DiscreteNoteBins(SoundMap):
    """Maps normalized data points to a discrete set of musical notes."""

    def __init__(self, notes):
        self._notes = notes
        self._bins = self._construct_bins(len(notes))

    @classmethod
    def from_key(cls, key="C:maj", octave_range=(4, 4)):
        """Constructs a ``DiscreteNoteBins`` SoundMap from a key (i.e. "C:maj") and an octave range.

        Uses the ``librosa.key_to_notes`` method to obtain the musical notes of a given key.

        Parameters
        ----------
        key: optional, str
            Must be in the form TONIC:key.  Tonic must be upper case (``CDEFGAB``),
            key must be lower-case
            (``major``, ``minor``, ``ionian``, ``dorian``, ``phrygian``, ``lydian``, ``mixolydian``, ``aeolian``, ``locrian``).

            The following abbreviations are supported for the modes: either the first three letters of the mode name
            (e.g. "mix") or the mode name without "ian" (e.g. "mixolyd").

            Both ``major`` and ``maj`` are supported as mode abbreviations.

            Single and multiple accidentals (``b!♭`` for flat, ``#♯`` for sharp, ``𝄪𝄫`` for double-accidentals, or any combination thereof) are supported.

            Examples: ``C:maj, C:major, Dbb:min, A♭:min, D:aeo, E𝄪:phryg``.

        octave_range: optional, tuple
            An inclusive range to use to select the octave range.
        """
        key_notes = librosa.key_to_notes(key, unicode=False)

        notes = []
        for i in range(octave_range[0], octave_range[1] + 1):
            notes.extend([note + str(i) for note in key_notes])

        notes = np.array(notes)
        freqs = np.array([librosa.note_to_hz(note) for note in notes])

        ordered_indices = freqs.argsort()

        return cls(notes[ordered_indices])

    @classmethod
    def from_midi(cls, start_note=60, end_note=72):
        """Constructs a ``DiscreteNoteBins`` SoundMap between two midi note numbers..

        Uses the ``librosa.midi_to_note`` method to obtain the range of notes between two midi note numbers.

        Parameters
        ----------
        start_note: int
            Starting midi note number between [0, 127]

        end_note: int
            Ending midi note number between [0, 127], must be greater or equal to start_note


        """
        if start_note > end_note:
            raise ValueError("Starting Note must be less than or equal to End Note")

        note_range = np.arange(start_note, end_note + 1)

        notes = [librosa.midi_to_note(note, unicode=False) for note in note_range]

        notes = np.array(notes)
        freqs = np.array([librosa.note_to_hz(note) for note in notes])

        ordered_indices = freqs.argsort()

        return cls(notes[ordered_indices])

    @classmethod
    def from_notes(cls, start_note="C4", end_note="C5"):
        """Constructs a ``DiscreteNoteBins`` SoundMap between two musical notes.

        Converts each musical note into its midi note number and calls ``DiscreteNoteBins.from_midi()`` to construct
        the SoundMap.

        Uses the ``librosa.note_to_midi`` to convert a note to its midi note number.

        Parameters
        ----------
        start_note: str
            Starting note, spelled out with optional accidentals or octave numbers (i.e. "C4", "C#3", etc.)

        end_note: str
            Ending note, spelled out with optional accidentals or octave numbers (i.e. "C4", "C#3", etc.), must be greater or equal to start_note
        """

        start_note_midi = librosa.note_to_midi(start_note)
        end_note_midi = librosa.note_to_midi(end_note)

        return cls.from_midi(start_note_midi, end_note_midi)

    def get_frequency(self, value):
        """Maps a normalized data point to its frequency (hz)"""
        note = self.get_note(value)
        return librosa.note_to_hz(note)

    def get_note(self, value):
        """Maps a normalized data point to its musical note"""
        note_idx = np.searchsorted(self._bins, value, side="left") - 1

        if note_idx == len(self._notes):
            note_idx = -1

        return self._notes[note_idx]

    @property
    def notes(self):
        """The list of musical notes in the SoundMap"""
        return self._notes

    @property
    def frequencies(self):
        """The frequency of each note in the SoundMap"""
        return [librosa.note_to_hz(note) for note in self.notes]

    def _construct_bins(self, n_notes):
        """Constructs a discrete set of bins, which map normalized data values to musical notes.

        Example
        -------
        [0, 1/3) [1/3, 2/3) [2/3, 1]
           A         B          C

        """
        bins = np.linspace(0, 1, n_notes + 1)
        bins[0] -= 0.001
        bins[-1] += 0.001

        return bins
