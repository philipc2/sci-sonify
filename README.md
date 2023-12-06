<img src="docs/source/_static/logo.svg" data-canonical-src="docs/source/_static/logo.svg" width="400"/><br>

-----------------

# Turning Scientific Data into Sounds & Music

## What is it?

Sci-Sonify is a Python package that enables simple and straightforward data sonification (a.k.a. representing data as sounds). It converts data stored using common packages in the Scientific Python Ecosystem such as Numpy, Pandas, and Xarray as musical notes.

## Soundmaps
Instead of using colors (i.e. colormaps) for visualuzing data, Sci-Sonify introduces the concept of "soundmaps", which allow for mapping quantitative data to a range of musical notes.

## Accessors
In addition to providing standalone functionality for working with lists and arrays, Sci-Sonify introduces accessors into commonly used packages in the Scientific Python Ecosystem.

### Xarray
Sonification through a `xr.DataArray`
```Python
import xarray as xr
import scisonify.xarray

da = xr.DataArray([1, 2, 3])

da.sonify()
```

### Pandas
Sonification through a `pd.Series`
```Python
import pandas as pd
import scisonify.pandas

s = pd.Series([1, 2, 3])

s.sonify()
```

## Installation
