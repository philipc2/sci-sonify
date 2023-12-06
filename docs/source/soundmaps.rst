Sound Maps
==========

SoundMaps are analogous to ColorMaps in visualizations, but for representing data as sounds. Sci-Sonify introduces the idea of SoundMaps,
which map data points into musical notes and frequencies.

Sci-Sonify currently provides a single type of SoundMap, referred to as ``DiscreteNoteBins``. As the name implies, it
creates uniformly-spaced bins to discretize a normalized array of values into musical notes.

..  code-block:: Python

    from scisonify.core.soundmaps import DiscreteNoteBins

The ``DiscreteNoteBins```` sound map provides multiple class-methods for construction and customization.

Construction from a musical key and a desired octave range.

..  code-block:: Python

    DiscreteNoteBins.from_key("C:maj", octave_range=(3, 4))

Construction from a range of midi note values

..  code-block:: Python

    DiscreteNoteBins.from_midi(start_note = 40, end_note = 50)

Construction from a range of musical notes

..  code-block:: Python

    DiscreteNoteBins.from_notes(start_note = "C4", end_note = "C5")
