def patch(name="sonify"):
    """Patches a ``xarray.DataArray`` to include a ``sonify`` instance."""
    from . import SonifyAccessor

    try:
        import xarray as xr
    except ModuleNotFoundError:
        raise ImportError("Xarray Library not found.")

    xr.register_dataarray_accessor(name)(SonifyAccessor)


patch()
