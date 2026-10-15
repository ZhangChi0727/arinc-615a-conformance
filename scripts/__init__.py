"""Repository-owned validation and maintenance entry points.

The directory remains usable as a collection of executable scripts.  Marking
it as a package also makes its public validation helpers importable by the
repository's production-path tests when ``pytest`` is invoked through its
console entry point, whose import path does not necessarily include the
repository root.
"""
