"""Wavefront PyFormance Plugin."""

__version__ = None

try:
    import importlib.metadata
    try:
        __version__ = importlib.metadata.version('wavefront-pyformance')
    except importlib.metadata.PackageNotFoundError:
        # __version__ is only available when distribution is installed.
        pass
except ImportError:
    pass
