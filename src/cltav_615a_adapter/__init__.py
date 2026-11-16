"""C-stage session adapter for the bounded ARINC 615A LUR-start object.

This is deliberately a sibling of :mod:`cltav_615a`, rather than an export
from it.  The accepted B-stage object has a closed five-file loaded-source
identity; importing or changing its public package surface for the C adapter
would silently expand that identity.  This package owns a separate, explicit
C-stage source identity and only consumes the B controller through its public
API.
"""

from .identity import AdapterSourceIdentity, AdapterSourceIdentityError, register_loaded_module

__all__ = ["AdapterSourceIdentity", "AdapterSourceIdentityError"]


register_loaded_module(__name__, __file__)
