"""This is the OldowanGenbank package."""

import os

VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION')).read().strip()

__all__ = ['read_genbank', 
           'iterate_genbank', 
           'parse_genbank', 
           'write_genbank']

from oldowan.genbank.read import read_genbank
from oldowan.genbank.iterate import iterate_genbank
from oldowan.genbank.parse import parse_genbank
from oldowan.genbank.write import write_genbank

