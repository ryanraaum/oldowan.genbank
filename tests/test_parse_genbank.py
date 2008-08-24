from oldowan.genbank import parse_genbank
from oldowan.genbank.parse import extract_source_feature
from oldowan.genbank.parse import extract_features

SINGLE_ENTRY = """LOCUS       NM_001071821             318 bp    mRNA    linear   PRI 09-OCT-2006
DEFINITION  Pan troglodytes somatic cytochrome c (CYCS), mRNA.
ACCESSION   NM_001071821 XM_001160382
VERSION     NM_001071821.1  GI:115392118
KEYWORDS    .
SOURCE      Pan troglodytes (chimpanzee)
  ORGANISM  Pan troglodytes
            Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi;
            Mammalia; Eutheria; Euarchontoglires; Primates; Haplorrhini;
            Catarrhini; Hominidae; Pan.
REFERENCE   1  (bases 1 to 318)
  AUTHORS   Wildman,D.E., Uddin,M., Liu,G., Grossman,L.I. and Goodman,M.
  TITLE     Implications of natural selection in shaping 99.4% nonsynonymous
            DNA identity between humans and chimpanzees: enlarging genus Homo
  JOURNAL   Proc. Natl. Acad. Sci. U.S.A. 100 (12), 7181-7188 (2003)
   PUBMED   12766228
REFERENCE   2  (bases 1 to 318)
  AUTHORS   Margoliash,E. and Fitch,W.M.
  TITLE     Evolutionary variability of cytochrome c primary structures
  JOURNAL   Ann. N. Y. Acad. Sci. 151 (1), 359-381 (1968)
   PUBMED   4975694
COMMENT     PROVISIONAL REFSEQ: This record has not yet been subject to final
            NCBI review. The reference sequence was derived from AY268594.1.
            On Oct 9, 2006 this sequence version replaced gi:114612441.
FEATURES             Location/Qualifiers
     source          1..318
                     /organism="Pan troglodytes"
                     /mol_type="mRNA"
                     /db_xref="taxon:9598"
                     /chromosome="7"
                     /map="7"
     gene            1..318
                     /gene="CYCS"
                     /note="cytochrome c, somatic"
                     /db_xref="GeneID:744779"
     CDS             1..318
                     /gene="CYCS"
                     /note="somatic cytochrome c"
                     /codon_start=1
                     /product="cytochrome c, somatic"
                     /protein_id="NP_001065289.1"
                     /db_xref="GI:115392119"
                     /db_xref="GeneID:744779"
                     /translation="MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQA
                     PGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKA
                     TNE"
ORIGIN      
        1 atgggtgatg ttgagaaagg caagaagatt tttattatga agtgttccca gtgccatacc
       61 gttgaaaagg gaggcaagca caagactggg ccaaatctcc atggtctctt cgggcggaag
      121 acaggtcagg cccctggata ttcttacaca gccgccaata agaacaaagg catcatctgg
      181 ggagaggata cactgatgga gtatttggag aatcccaaga agtacatccc tggaacaaaa
      241 atgatatttg tcggcattaa gaagaaggaa gaaagggcag acttaatagc ttatctcaaa
      301 aaagctacta atgagtaa
//"""

raw_features = """FEATURES             Location/Qualifiers
     source          1..318
                     /organism="Pan troglodytes"
                     /mol_type="mRNA"
                     /db_xref="taxon:9598"
                     /chromosome="7"
                     /map="7"
     gene            1..318
                     /gene="CYCS"
                     /note="cytochrome c, somatic"
                     /db_xref="GeneID:744779"
     CDS             1..318
                     /gene="CYCS"
                     /note="somatic cytochrome c"
                     /codon_start=1
                     /product="cytochrome c, somatic"
                     /protein_id="NP_001065289.1"
                     /db_xref="GI:115392119"
                     /db_xref="GeneID:744779"
                     /translation="MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQA
                     PGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKA
                     TNE"
"""

def test_source_feature_extraction():
    """genbank source feature extraction"""
    source = extract_source_feature(raw_features)[0][1]
    assert isinstance(source, list)

    assert 6 == len(source)
    assert '1..318' == source[0]
    assert ('organism', 'Pan troglodytes') == source[1]
    assert ('mol_type', 'mRNA') == source[2]
    assert ('db_xref', 'taxon:9598') == source[3]
    assert ('chromosome', '7') == source[4]
    assert ('map', '7') == source[5]

def test_features_extraction():
    """genbank all features extraction"""
    features = extract_features(raw_features)
    assert isinstance(features, list)

    assert 3 == len(features)

    assert 'source' == features[0][0]
    assert 'gene'   == features[1][0]
    assert 'CDS'    == features[2][0]

    gene = features[1][1]
    assert 4 == len(gene)
    assert '1..318' == gene[0]
    assert ('gene', 'CYCS') == gene[1]
    assert ('note','cytochrome c, somatic') == gene[2]
    assert ('db_xref','GeneID:744779') == gene[3]

    cds = features[2][1]
    assert 9 == len(cds)
    assert '1..318' == cds[0]
    assert ('gene','CYCS') == cds[1]
    assert ('note','somatic cytochrome c') == cds[2]
    assert ('codon_start','1') == cds[3]
    assert ('product','cytochrome c, somatic') == cds[4]
    assert ('protein_id','NP_001065289.1') == cds[5]
    assert ('db_xref','GI:115392119') == cds[6]
    assert ('db_xref','GeneID:744779') == cds[7]
    assert ('translation','MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE') == cds[8]

def test_entry_parsing():
    """genbank entry parsing"""
    parsed = parse_genbank(SINGLE_ENTRY)
    assert isinstance(parsed, dict)

    assert 'locus' in parsed
    assert 'NM_001071821' == parsed['locus']

    assert 'division' in parsed
    assert 'PRI' == parsed['division']

    assert 'orientation' in parsed
    assert 'linear' == parsed['orientation']

    assert 'strandedness' in parsed
    assert '' == parsed['strandedness']

    assert 'nucleic_acid' in parsed
    assert 'mRNA' == parsed['nucleic_acid']

    assert 'date' in parsed
    assert '09-OCT-2006' == parsed['date']

    assert 'definition' in parsed
    assert 'Pan troglodytes somatic cytochrome c (CYCS), mRNA.' == parsed['definition']

    assert 'accession' in parsed
    assert 'NM_001071821' == parsed['accession']

    assert 'version' in parsed
    assert '1' == parsed['version']

    assert 'gi' in parsed
    assert '115392118' == parsed['gi']

    assert 'source' in parsed
    assert 'Pan troglodytes (chimpanzee)' == parsed['source']

    assert 'organism' in parsed
    assert 'Pan troglodytes' == parsed['organism']

    assert 'taxonomy' in parsed
    #assert '' == parsed['taxonomy']

    assert 'features' in parsed
    assert 'source' == parsed['features'][0][0]
    assert 'gene'   == parsed['features'][1][0]
    assert 'CDS'    == parsed['features'][2][0]

    assert 'sequence' in parsed
    assert 318 == len(parsed['sequence'])

def test_entry_parsing_only_include_locus():
    """genbank entry parsing only include locus"""
    parsed = parse_genbank(SINGLE_ENTRY, include=['locus'])
    assert isinstance(parsed, dict)

    assert 'locus' in parsed
    assert 'NM_001071821' == parsed['locus']

    assert 'division' in parsed
    assert 'PRI' == parsed['division']

    assert 'orientation' in parsed
    assert 'linear' == parsed['orientation']

    assert 'strandedness' in parsed
    assert '' == parsed['strandedness']

    assert 'nucleic_acid' in parsed
    assert 'mRNA' == parsed['nucleic_acid']

    assert 'date' in parsed
    assert '09-OCT-2006' == parsed['date']

    assert not 'definition' in parsed
    assert not 'accession' in parsed
    assert not 'version' in parsed
    assert not 'gi' in parsed
    assert not 'source' in parsed
    assert not 'organism' in parsed
    assert not 'taxonomy' in parsed
    assert not 'features' in parsed
    assert not 'sequence' in parsed

def test_entry_parsing_only_include_definition():
    """genbank entry parsing only include definition"""
    parsed = parse_genbank(SINGLE_ENTRY, include=['definition'])
    assert isinstance(parsed, dict)

    assert not 'locus' in parsed
    assert not 'division' in parsed
    assert not 'orientation' in parsed
    assert not 'strandedness' in parsed
    assert not 'nucleic_acid' in parsed
    assert not 'date' in parsed

    assert 'definition' in parsed
    assert 'Pan troglodytes somatic cytochrome c (CYCS), mRNA.' == parsed['definition']

    assert not 'accession' in parsed
    assert not 'version' in parsed
    assert not 'gi' in parsed
    assert not 'source' in parsed
    assert not 'organism' in parsed
    assert not 'taxonomy' in parsed
    assert not 'features' in parsed
    assert not 'sequence' in parsed

def test_entry_parsing_only_include_version():
    """genbank entry parsing only include version"""
    parsed = parse_genbank(SINGLE_ENTRY, include=['version'])
    assert isinstance(parsed, dict)

    assert not 'locus' in parsed
    assert not 'division' in parsed
    assert not 'orientation' in parsed
    assert not 'strandedness' in parsed
    assert not 'nucleic_acid' in parsed
    assert not 'date' in parsed
    assert not 'definition' in parsed

    assert 'accession' in parsed
    assert 'NM_001071821' == parsed['accession']

    assert 'version' in parsed
    assert '1' == parsed['version']

    assert 'gi' in parsed
    assert '115392118' == parsed['gi']

    assert not 'source' in parsed
    assert not 'organism' in parsed
    assert not 'taxonomy' in parsed
    assert not 'features' in parsed
    assert not 'sequence' in parsed

def test_entry_parsing_only_include_source():
    """genbank entry parsing only include source"""
    parsed = parse_genbank(SINGLE_ENTRY, include=['source'])
    assert isinstance(parsed, dict)

    assert not 'locus' in parsed
    assert not 'division' in parsed
    assert not 'orientation' in parsed
    assert not 'strandedness' in parsed
    assert not 'nucleic_acid' in parsed
    assert not 'date' in parsed
    assert not 'definition' in parsed
    assert not 'accession' in parsed
    assert not 'version' in parsed
    assert not 'gi' in parsed

    assert 'source' in parsed
    assert 'Pan troglodytes (chimpanzee)' == parsed['source']

    assert 'organism' in parsed
    assert 'Pan troglodytes' == parsed['organism']

    assert 'taxonomy' in parsed
    #assert '' == parsed['taxonomy']

    assert not 'features' in parsed
    assert not 'sequence' in parsed

def test_entry_parsing_only_include_features():
    """genbank entry parsing only include features"""
    parsed = parse_genbank(SINGLE_ENTRY, include=['features'])
    assert isinstance(parsed, dict)

    assert not 'locus' in parsed
    assert not 'division' in parsed
    assert not 'orientation' in parsed
    assert not 'strandedness' in parsed
    assert not 'nucleic_acid' in parsed
    assert not 'date' in parsed
    assert not 'definition' in parsed
    assert not 'accession' in parsed
    assert not 'version' in parsed
    assert not 'gi' in parsed
    assert not 'source' in parsed
    assert not 'organism' in parsed
    assert not 'taxonomy' in parsed
    
    assert 'features' in parsed
    assert 3 == len(parsed['features'])
    assert 'source' == parsed['features'][0][0]
    assert 'gene'   == parsed['features'][1][0]
    assert 'CDS'    == parsed['features'][2][0]

    assert not 'sequence' in parsed

def test_entry_parsing_only_include_source_feature():
    """genbank entry parsing only include source feature"""
    parsed = parse_genbank(SINGLE_ENTRY, include=['source_feature_only'])
    assert isinstance(parsed, dict)

    assert not 'locus' in parsed
    assert not 'division' in parsed
    assert not 'orientation' in parsed
    assert not 'strandedness' in parsed
    assert not 'nucleic_acid' in parsed
    assert not 'date' in parsed
    assert not 'definition' in parsed
    assert not 'accession' in parsed
    assert not 'version' in parsed
    assert not 'gi' in parsed
    assert not 'source' in parsed
    assert not 'organism' in parsed
    assert not 'taxonomy' in parsed
    
    assert 'features' in parsed
    assert 1 == len(parsed['features'])
    assert 'source' == parsed['features'][0][0]

    assert not 'sequence' in parsed

def test_entry_parsing_only_include_sequence():
    """genbank entry parsing only include sequence"""
    parsed = parse_genbank(SINGLE_ENTRY, include=['sequence'])
    assert isinstance(parsed, dict)

    assert not 'locus' in parsed
    assert not 'division' in parsed
    assert not 'orientation' in parsed
    assert not 'strandedness' in parsed
    assert not 'nucleic_acid' in parsed
    assert not 'date' in parsed
    assert not 'definition' in parsed
    assert not 'accession' in parsed
    assert not 'version' in parsed
    assert not 'gi' in parsed
    assert not 'source' in parsed
    assert not 'organism' in parsed
    assert not 'taxonomy' in parsed
    assert not 'features' in parsed

    assert 'sequence' in parsed
    #assert '' == parsed['sequence']

