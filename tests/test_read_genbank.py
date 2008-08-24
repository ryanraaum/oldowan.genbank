from oldowan.genbank import read_genbank
from oldowan.genbank import iterate_genbank

import os

TEN_DLOOPS_FILEPATH = os.path.join(os.path.dirname(__file__), 
        'test_files', 'ten_dloops.gb')
_f = open(TEN_DLOOPS_FILEPATH)
TEN_DLOOPS_TEXT = _f.read()
_f.close()

def test_read_genbank_from_text():
    """read_genbank given text"""
    # first, explicitly tell it this is text
    entries = read_genbank(TEN_DLOOPS_TEXT, what='text')
    assert 10 == len(entries)

    # next, make it guess
    entries = read_genbank(TEN_DLOOPS_TEXT)
    assert 10 == len(entries)

def test_read_genbank_from_filename():
    """read_genbank given filename"""
    # first, explicitly tell it this is a filename
    entries = read_genbank(TEN_DLOOPS_FILEPATH, what='filename')
    assert 10 == len(entries)

    # next, make it guess
    entries = read_genbank(TEN_DLOOPS_FILEPATH)
    assert 10 == len(entries)

def test_read_genbank_from_file():
    """read_genbank given file"""
    # first, explicitly tell it this is a file
    f = open(TEN_DLOOPS_FILEPATH, 'r')
    entries = read_genbank(f, what='file')
    assert 10 == len(entries)

    # next, make it guess
    f = open(TEN_DLOOPS_FILEPATH, 'r')
    entries = read_genbank(f)
    assert 10 == len(entries)

def test_iterate_genbank_with_dict_return():
    """iterate_genbank with default options"""
    # first, from text
    for entry in iterate_genbank(TEN_DLOOPS_TEXT):
        assert isinstance(entry, dict)
    # next, from file
    for entry in iterate_genbank(TEN_DLOOPS_FILEPATH):
        assert isinstance(entry, dict)

def test_iterate_genbank_with_raw_return():
    """iterate_genbank with raw option"""
    # first, from text
    for entry in iterate_genbank(TEN_DLOOPS_TEXT, raw=True):
        assert isinstance(entry, str)
    # next, from file
    for entry in iterate_genbank(TEN_DLOOPS_FILEPATH, raw=True):
        assert isinstance(entry, str)

