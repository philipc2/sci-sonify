def patch(name="sonify"):
    from . import SonifyAccessor

    try:
        import pandas as pd
    except ModuleNotFoundError:
        raise ImportError("TODO")

    pd.api.extensions.register_series_accessor("sonify")(SonifyAccessor)


patch()
