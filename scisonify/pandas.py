def patch(name="sonify"):
    """Patches a ``pandas.Series`` to include a ``sonify`` instance."""
    from . import SonifyAccessor

    try:
        import pandas as pd
    except ModuleNotFoundError:
        raise ImportError("Pandas library not found.")

    pd.api.extensions.register_series_accessor("sonify")(SonifyAccessor)


patch()
