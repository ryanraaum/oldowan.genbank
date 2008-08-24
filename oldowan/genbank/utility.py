import re

# Everything in this file is private / an implementation detail
__all__ = []

RE_NEWLINE = re.compile(r"[\r\n]+")
"""OS-independent newline regex."""

def join_stripped_lines(s):
    """Join (variably indented) lines together with a single space.

    Returns a single string. The string does not have a newline appended.
    """
    to_join = []
    for line in RE_NEWLINE.split(s): 
        to_join.append(line.strip())
    return " ".join(to_join)

def split_into_lines(s, length=80):
    """Break string into lines <= length without splitting words.

    Returns a list of lines. Lines do not have newlines.
    """
    lines = []
    cur = ""
    for w in s.split():
        if len(cur) + len(w) + 1 < length:
            cur = cur + w + " "
        else:
            lines.append(cur)
            cur = w + " "
    lines.append(cur)
    return lines

def chunk(s, length):
    """Break string into lines == length.

    Returns a list of lines. Lines do not have newlines. This method
    does not preserve words. Typically used to break up a sequence into
    equal sized chunks for presentation.
    """
    chunks = []
    for x in re.findall("."*length, s):
        chunks.append(x)
    l = len(s)
    if (l % length) > 0:
        chunks.append(s[l - (l % length):])
    return chunks

