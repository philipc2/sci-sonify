import numpy as np

class Sonify:
    def __init__(self, data, smap):
        self._data = self._normalize_data(data)
        self._smap = smap

    def _normalize_data(self, data):
        """TODO: Docstring"""
        data = np.asarray(data)
        return (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
