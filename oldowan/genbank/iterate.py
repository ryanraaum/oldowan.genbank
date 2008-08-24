"""This is oldowan.genbank.iterate."""

__all__ = ['iterate_genbank']

from oldowan.genbank.constants import INCLUDE
from oldowan.genbank.parse import parse_genbank

import StringIO

def iterate_genbank(something, what='guess', raw=False, include=INCLUDE):
    """Iterate through genbank formatted entries in a file or text."""
    if what == 'guess':
        if type(something) == file:
            what = 'file'
        elif type(something) == str:
            if len(something) > 256:
                what = 'text'
            else:
                what = 'filename'
    if what == 'file':
        f = something
    elif what == 'filename':
        f = open(something, 'r')
    elif what == 'text':
        f = StringIO.StringIO(something)
    else:
        raise TypeError("don't know how to handle '%s'" % what)

    # find the beginning of the first entry
    buf = ''
    while not buf.startswith('LOCUS'):
        buf = f.readline()

    if buf == '':
        f.close()
        raise IOError("file '%s' does not appear to be in Genbank format" % filename)

    done = False
    while not done:
        entry = []
        while buf != '':
            entry.append(buf)
            buf = f.readline()
            # read until the next entry ('LOCUS') or end of file ('')
            if buf.startswith('LOCUS') or buf == '':
                if raw:
                    yield ''.join(entry)
                else:
                    yield parse_genbank(''.join(entry))
                entry = []
        f.close()
        done = True
  
