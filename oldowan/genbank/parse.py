"""This is oldowan.genbank.parse."""

__all__ = ['parse_genbank']

from oldowan.genbank.constants import INCLUDE
from oldowan.genbank.utility import join_stripped_lines

import re

#
# PARSER
#

def parse_genbank(entry, include=INCLUDE):
    """Parse text of genbank entry into dictionary.

    """
    include = set(include)
    if not entry.startswith('LOCUS'):
        raise TypeError('entry is not in genbank format') 

    hash = {}

    if 'locus' in include:
        loc_mo = RE_LOCUS.match(entry)
        if loc_mo:
            loc = loc_mo.group(0)
            hash['locus'] = loc[12:28].strip() 
            hash['division'] = loc[64:67].strip()
            hash['orientation'] = loc[55:63].strip()
            hash['strandedness'] = loc[44:47].strip()
            hash['nucleic_acid'] = loc[47:53].strip()
            date_mo = RE_DATE.search(loc)
            if date_mo:
                hash['date'] = date_mo.group(0)

    if 'definition' in include:
        defn_mo = RE_DEFINITION.search(entry)
        if defn_mo:
            hash['definition'] = join_stripped_lines(defn_mo.group(1))

    if 'version' in include:
        vers_mo = RE_VERSION.search(entry)
        if vers_mo:
            hash['accession'] = vers_mo.group(1)
            hash['version'] = vers_mo.group(2)
            hash['gi'] = vers_mo.group(3)

    if 'source' in include:
        src_mo = RE_SOURCE.search(entry)
        if src_mo:
            hash['source'] = src_mo.group(1)
            hash['organism'] = src_mo.group(2)
            hash['taxonomy'] = RE_TAXONOMY_WHITESPACE.sub('; ', src_mo.group(3))

    if 'features' in include:
        fea_mo = RE_FEATURE.search(entry)
        if fea_mo:
            hash['features'] = extract_features(fea_mo.group(0))
    elif 'source_feature_only' in include:
        fea_mo = RE_FEATURE.search(entry)
        if fea_mo:
            hash['features'] = extract_source_feature(fea_mo.group(0))

    if 'sequence' in include:
        ori_mo = RE_SEQUENCE.search(entry)
        if ori_mo:
            ori = ori_mo.group(1)
            # remove the first line from the origin string
            frst_line_mo = RE_FIRST_LINE.match(ori)
            ori = frst_line_mo.group(1)
            # strip out numbers and spaces
            ori = RE_NUMBERS_AND_WHITESPACE.sub('', ori)
            hash['sequence'] = ori
        else:
            hash['sequence'] = ''

    return hash

# 
# PRIVATE UTILITY FUNCTIONS USED IN PARSER
#
# These functions are implementation details and should not be used outside of
# this parser. There is no guarantee that any of these will be maintained or
# necessarily function the same as the parser evolves. The call signature and
# return values of the 'parse_genbank' function are the only supported public
# interface.
#

def extract_features(raw_features):
    features = RE_FEATURE_SPLITTER.split(raw_features)
    # first list entry after the split is the FEATURES header line
    # throw it away
    features.pop(0)
    return [parse_feature(x) for x in features]

def extract_source_feature(raw_features):
    source = []
    features = RE_FEATURE_SPLITTER.split(raw_features)
    # if there are any features at all, then after the split
    # index 0 will hold the FEATURES header line
    # and the first actual feature at index 1 will be the 'source' feature
    if len(features) > 1:
        return [parse_feature(features[1])]
    return None

def parse_feature(feature):
    parsed = []
    # split up the feature; sub-entry ids are prefixed by '/'
    feature_entries = feature.split('/')
    # the first sub-entry of any feature is its position
    position_line = feature_entries.pop(0)
    # NOTE this assumes a simple feature position
    # will probably break on complex positions
    # TODO make more robust to complex positions
    position_entries = position_line.split()
    feature_name = position_entries[0]
    position = position_entries[1]
    parsed.append(position)
    # for all other sub-entries, split by '='
    # with a maximum split of 1
    entries = [x.split('=', 1) for x in feature_entries]
    for x in entries:
        if 1 == len(x):
            parsed.append((clean_up(x[0]), True))
        elif 2 == len(x):
            parsed.append((clean_up(x[0]), clean_up(x[1])))
    return (feature_name, parsed)

def clean_up(strng):
    """Strip excess whitespace and de-quote a Genbank feature value string."""
    strng = strng.strip()
    # remove indentation whitespace (if this is a multiline string)
    strng = RE_FEATURE_INDENT.sub('', strng)
    # remove opening and closing "s if present
    quote_mo = RE_QUOTED.match(strng)
    if quote_mo:
        strng = quote_mo.group(1)
    return strng

#
# REGULAR EXPRESSIONS USED IN PARSER
#

RE_LOCUS        = re.compile(r"^LOCUS[^\r\n]*")
"""Match opening LOCUS line from full entry text."""

#: Match date in LOCUS line 
RE_DATE         = re.compile(r"\d\d-[A-Z][A-Z][A-Z]-\d\d\d\d")

#: Match DEFINITION line from full entry text
RE_DEFINITION   = re.compile(r"[\r\n]DEFINITION(.*?)[\r\n]\S")

#: Match VERSION line from full entry text
RE_VERSION      = re.compile(r"[\r\n]VERSION     (.+?)\.(\d)\s+GI:(\d+)\s*?[\r\n]\S")

#: Match SOURCE line in main body from full entry text
RE_SOURCE       = re.compile(r"[\r\n]SOURCE      ([^\r\n]+)[\r\n]  ORGANISM\s+([^\r\n]+)\s+(.*?)\S", re.S)

#: Match complete REFERENCE block from full entry text
#RE_REFERENCE   = re.compile(r"[\r\n](REFERENCE.*?)[\r\n]\S", re.S)

#: Match complete COMMENT block from full entry text
#RE_COMMENT     = re.compile(r"[\r\n](COMMENT.*?)[\r\n]\S", re.S)

#: Match complete FEATURE block from full entry text
RE_FEATURE      = re.compile(r"[\r\n](FEATURES.*?)[\r\n]\S", re.S)

#: Match indent inbetween feature entries in FEATURE block
RE_FEATURE_SPLITTER \
                = re.compile(r"[\r\n]     (?=\S)")

#: Match SEGMENT block from full entry text
#RE_SEGMENT     = re.compile(r"[\r\n](SEGMENT.*?)[\r\n]\S")

#: Match CONTIG block from full entry text
#RE_CONTIG      = re.compile(r"[\r\n](CONTIG.*?)[\r\n]\S")

#: Match ORIGIN block (contains the sequence) from full entry text
RE_SEQUENCE     = re.compile(r"[\r\n](ORIGIN.*?)[\r\n]\S", re.S)

#: Match "quoted" text, capturing the inner text
RE_QUOTED       = re.compile(r'^"(.*?)"$')

#: Match the 21 space indent in multiline feature entries
RE_FEATURE_INDENT \
                = re.compile(r'[\r\n] {21}')

#: Match semi-colon with whitespace in taxonomy listing.
RE_TAXONOMY_WHITESPACE \
                = re.compile(r";\s+")

#: Match a single line (used here to remove the ORIGIN line from the sequence)
RE_FIRST_LINE   = re.compile(r"^[^\r\n]+(.*)", re.S)

#: Match numbers and whitespace (used here to clear out all formatting from 
#: the sequence in the ORIGIN block)
RE_NUMBERS_AND_WHITESPACE \
                = re.compile(r"[\d\s]")

