"""Python filesystem abstraction layer.
"""

from os import fsdecode, fsencode
from . import path
from ._version import __version__
from .enums import ResourceType, Seek
from .opener import open_fs

__all__ = ["__version__", "ResourceType", "Seek", "open_fs"]
