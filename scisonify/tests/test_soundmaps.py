import pytest

from scisonify.core.soundmaps import DiscreteNoteBins


class TestDiscreteNoteBins:
    keys = ["A#:min", "B:min", "C:maj"]

    def test_notes(self):
        for key in self.keys:
            smap_one_oct = DiscreteNoteBins.from_key(key, octave_range=(4, 4))
            smap_two_oct = DiscreteNoteBins.from_key(key, octave_range=(4, 5))
            smap_three_oct = DiscreteNoteBins.from_key(key, octave_range=(3, 5))

            assert len(smap_one_oct._notes) == 12

            assert len(smap_two_oct._notes) == 24

            assert len(smap_three_oct._notes) == 36

    def test_bins(self):
        for key in self.keys:
            smap_one_oct = DiscreteNoteBins.from_key(key, octave_range=(4, 4))
            smap_two_oct = DiscreteNoteBins.from_key(key, octave_range=(4, 5))
            smap_three_oct = DiscreteNoteBins.from_key(key, octave_range=(3, 5))

            assert len(smap_one_oct._bins) == len(smap_one_oct._notes) + 1

            assert len(smap_two_oct._bins) == len(smap_two_oct._notes) + 1

            assert len(smap_three_oct._bins) == len(smap_three_oct._notes) + 1
