"""Independent D-stage engineering delivery for the bounded 615A control slice.

This package owns the installable ``cltav-615a-engineering`` command, the
closed evidence envelope, and transactional publication.  It consumes the
accepted C adapter and B object through their public APIs.  It is not the
PR #25 G3 synthetic producer, not an IUT executor, and not a protocol verdict.
"""

from .errors import EngineeringError

__all__ = ["EngineeringError"]
