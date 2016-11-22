import urllib
import urllib2
from StringIO import StringIO


url = 'http://www.uniprot.org/taxonomy/'
keys = ['scientific', 'common', 'mnemonic', 'rank',
        'strain', 'host', 'linked', 'id']
mapping = {'Common name': 'common_name',
           'Lineage': 'lineage',
           'Mnemonic': 'mnemonic',
           'Other Names': 'other_names',
           'Parent': 'parent',
           'Rank': 'rank',
           'Reviewed': 'reviewed',
           'Scientific name': 'scientific_name',
           'Synonym': 'synonym',
           'Taxon': 'taxon',
           'Virus hosts': 'virus_hosts'}


class Taxonomy(object):
    """A class for containing organism objects.

    Attributes
    ----------
    taxons: dict of Organism objects with taxon ID keys
    mnemonics : dict of Organism objects mnemonic keys
    """

    def __init__(self, filename=None):
        self.taxons = dict()
        self.mnemonics = dict()
        if filename:
            with open(filename) as f:
                organisms = get_organisms(f)
                self._get_taxonomy(organisms)

    def _get_taxonomy(self, organisms):
        """Initialize self.taxons and self.mnemonics.

        Parameters
        ----------
        organisms : iterable of Organism objects
        """
        for organism in organisms:
            self.taxons[organism.taxon] = organism
            if organism.mnemonic:
                self.mnemonics[organism.mnemonic] = organism

    def __getitem__(self, key):
        """Return organism given taxon or mnemonic key."""
        if type(key) is int:
            if key not in self.taxons:
                raise KeyError('Taxon {} is not in the taxonomy.'.format(key))
            return self.taxons[key]
        if type(key) is str:
            if key not in self.mnemonics:
                raise KeyError('Mnenomic "{}" is not in the taxonomy.'.format(key))
            return self.mnemonics[key]
        raise ValueError('{} must be a taxon number or mnemonic ID.'.format(key))

    def __len__(self):
        """Return number of organisms in the taxonomy."""
        return len(self.taxons)


class Organism(object):
    """A class for organisms in the Uniprot taxonomy database.

    Attributes
    ----------
    common_name : str
    lineage : list of str
    mnemonic : str
    other_names : list of str
    parent : int
    rank : str
    reviewed : str
    scientific_name : str
    synonym : str
    taxon : int
    virus_hosts : str
    """

    def __init__(self, **kwargs):
        """Set attributes based on `mapping`.

        `taxon` and `parent` are ints.
        `lineage` and `other_names` are delimited by '; '.
        """
        for key, value in kwargs.items():
            if key not in mapping:
                raise KeyError('"{}" is not a valid key.'.format(key))
            if value == '':
                value = None
            elif key in ['Taxon', 'Parent']:
                value = int(value)
            elif key in ['Lineage', 'Other Names']:
                value = value.split('; ')
            setattr(self, mapping[key], value)
        for key, attr in mapping.items():
            if not hasattr(self, attr):
                setattr(self, attr, None)

    def __repr__(self):
        if not self.mnemonic:
            string = 'Organism(taxon={0.taxon})'
        else:
            string = 'Organism(taxon={0.taxon},mnemonic="{0.mnemonic}")'
        return string.format(self)


def get_organisms(stream):
    """Return iterable of Organism objects
    from a tab-delimited stream with header column.

    Parameters
    ----------
    stream : abstract stream object
    """
    header = stream.readline().rstrip().split('\t')
    for i, line in enumerate(stream.readlines()):
        yield Organism(**dict(zip(header, line.rstrip().split('\t'))))


def get_organisms_page(fmt='tab', contact=None, **kwargs):
    """Return page stream from a query.

    Parameters
    ----------
    fmt : 'tab'/'rdf'
    kwargs : keyword arguments to be used for query
    """
    for arg in kwargs:
        if arg not in keys:
            raise KeyError('"{}" is not a valid key'.format(arg))
    queries = list(_get_queries(**kwargs))
    query_string = '+'.join(queries)
    params = {'query': query_string,
              'format': fmt}
    return get_page_stream(url, params=params, contact=contact)


def _get_queries(**kwargs):
    """Queries in Uniprot's URL format.

    Used by get_organisms_page().
    """
    for key, value in kwargs.items():
        if value:
            yield '{}:{}'.format(key, value)


def get_page_stream(url, params=None, contact=None):
    """Return page as a file-like stream.

    Parameters
    ----------
    url : request URL
    params : dict of URL parameters to be encoded
    contact : e-mail address for Uniprot's debugging purposes

    Returns
    -------
    StringIO object (for page to be read as a file-like stream)
    """
    if params:
        data = urllib.urlencode(params)
        request = urllib2.Request(url, data)
    else:
        request = urllib2.Request(url)
    if contact:
        request.add_header('User-Agent', 'Python %s' % contact)
    else:
        contact = ""
    response = urllib2.urlopen(request)
    page = response.read(200000)
    return StringIO(page)
