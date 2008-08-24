"""This is oldowan.genbank.write."""

__all__ = ['write_genbank', 'format_genbank_entry']

def write_genbank(filename, entry_list):
    """Write list of genbank data to file.

    """
    f = open(filename, 'w')
    for entry in entry_list:
        write_genbank_entry(f, entry)
    f.close()

def format_genbank_entry(hash):
    """Create genbank formatted text.
    
    """
    raise NotImplementedError

