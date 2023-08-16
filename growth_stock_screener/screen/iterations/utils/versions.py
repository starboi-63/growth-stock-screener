import sys


def python_version() -> str:
    """Return the version of Python that is installed."""
    return sys.version.split()[0]


def assert_python_updated(min_version: str) -> bool:
    """Assert whether Python is up-to-date with an inputted version number of the form 'x.x.x...'"""
    return version_geq(python_version(), min_version)


def version_geq(vnum_a: str, vnum_b: str) -> bool:
    "Returns 'True' if version 'a.a.a...' >= 'b.b.b...'"
    a_components = vnum_a.split(".")
    b_components = vnum_b.split(".")
    max_len = max(len(a_components), len(b_components))

    # fill in '0's when version lengths are not the same
    if len(a_components) < max_len:
        for i in range(max_len - len(a_components)):
            a_components.append("0")
    elif len(b_components) < max_len:
        for i in range(max_len - len(b_components)):
            b_components.append("0")

    for i in range(max_len):
        if a_components[i] > b_components[i]:
            return True
        elif a_components[i] < b_components[i]:
            return False

    return True
