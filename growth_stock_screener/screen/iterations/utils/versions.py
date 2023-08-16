import sys


def python_version() -> str:
    """Return the version of Python that is installed."""
    return sys.version.split()[0]


def assert_python_updated(min_version: str) -> bool:
    """Assert whether Python is up-to-date with an inputted version number of the form 'x.x.x...'"""
    version = python_version()

    version_components = version.split(".")
    min_version_components = min_version.split(".")
    min_len = min(len(version_components), len(min_version_components))

    for i in range(min_len):
        if version_components[i] > min_version_components[i]:
            return True
        elif version_components[i] < min_version_components[i]:
            return False

    return True
