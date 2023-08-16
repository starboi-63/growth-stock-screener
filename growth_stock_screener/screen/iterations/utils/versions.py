import sys


def python_version() -> str:
    """Return the version of Python that is installed."""
    return sys.version.split()[0]


def assert_python_updated(min_version: str) -> bool:
    """Assert whether Python is up-to-date with an inputted version number of the form 'x.x.x...'"""
    return version_greater(python_version(), min_version)


def version_greater(vnum_a: str, vnum_b: str) -> bool:
    "Returns 'True' if version 'a.a.a...' > 'b.b.b...'"
    a_components = vnum_a.split(".")
    b_components = vnum_b.split(".")
    min_len = min(len(a_components), len(b_components))

    for i in range(min_len):
        if a_components[i] > b_components[i]:
            return True
        elif a_components[i] < b_components[i]:
            return False

    return True
