"""This is oldowan.genbank.read."""

__all__ = ['read_genbank']

from oldowan.genbank.iterate import iterate_genbank
from oldowan.genbank.constants import INCLUDE

def read_genbank(filename, what='guess', raw=False, include=INCLUDE):
    """Read genbank formatted entries from a file or text.

    """
    items = []
    for entry in iterate_genbank(filename, what=what, raw=raw, include=include):
        items.append(entry)
    return items

