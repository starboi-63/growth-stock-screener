import sys


def python_version() -> str:
    """Return the version of Python that is installed."""
    return sys.version.split()[0]
