# adapted from https://www.youtube.com/watch?v=OSCzKOqtgcA

import numpy as np


class EnvelopeADSR:
    """Attack-Decay-Sustain-Release Envelope Implementation, adapted from the C++ implementation by javidx9
    (https://www.youtube.com/watch?v=OSCzKOqtgcA)

    Parameters
    ----------
    attack_length: optional, float
        Duration of "attack"

    decay_length: optional, float
        Duration of "decay"

    release_length: optional, float
        Duration of "release"

    note_length: optional, float
        The total length of a note

    start_amplitude: optional, float
        Initial amplitude for a note

    sustian_amplitude: optional, float
        Sustain amplitude for a note

    """

    def __init__(
        self,
        attack_length=0.2,
        decay_length=0.1,
        release_length=0.2,
        note_length=1.0,
        start_amplitude=0.0,
        sustian_amplitude=0.8,
    ):
        self.attack_length = attack_length
        self.decay_length = decay_length
        self.release_length = release_length
        self.start_amplitude = start_amplitude
        self.sustian_amplitude = sustian_amplitude
        self.note_length = note_length

        self.attack_until = attack_length
        self.decay_until = attack_length + decay_length
        self.sustian_until = note_length - release_length

    def get_amplitude(self, time):
        """Returns the envelope amplitude at a given time step"""

        if time < self.attack_until:
            return (1.0 / self.attack_length) * time

        elif time < self.decay_until:
            m = (self.sustian_amplitude - 1.0) / self.decay_length
            return m * (time - self.decay_until) + self.sustian_amplitude

        elif time < self.sustian_until:
            return self.sustian_amplitude

        else:
            m = (-1.0 * self.sustian_amplitude) / self.release_length
            return m * (time - self.note_length)

    def get_amplitudes(self, times):
        """Returns all the amplitudes for an array of discrete times."""

        return np.array([self.get_amplitude(time) for time in times])
