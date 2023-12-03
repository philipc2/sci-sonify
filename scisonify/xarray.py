def patch(name="sonify"):
    from . import SonifyAccessor

    try:
        import xarray as xr
    except ModuleNotFoundError:
        raise ImportError("TODO")

    xr.register_dataarray_accessor(name)(SonifyAccessor)


patch()
