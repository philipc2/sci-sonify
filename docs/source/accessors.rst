Xarray & Pandas Accessors
=========================

In addition to directly working with a ``Sonify`` instance, you may elect to use the Xarray and Pandas accessors to
directly sonify data without needing to worry about constructing a ``Sonify`` object.

Sci-Sonify provides accessors for ``xarray.DataArray`` and ``pandas.Series`` classes.


..  code-block:: Python

    import xarray as xr
    import scisonify.xarray

    da = xr.DataArray([1, 2, 3])

    da.sonify()

..  code-block:: Python

    import pandas as pd
    import scisonify.pandas

    s = pd.Series([1, 2, 3])
    s.sonify()


Calling the accessor wraps the ``Sonify.to_audio()`` method, and will return an interactive audio widget through the IPython Display.
