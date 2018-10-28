# -*- coding: utf-8 -*-

"""A package for converting RGD to BEL."""

from .constants import VERSION
from .manager import Manager


def get_version() -> str:
    """Get the package version."""
    return VERSION
