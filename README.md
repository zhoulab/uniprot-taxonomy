# uniprot-taxonomy

Tool for extracting taxonomy information from the [Uniprot database](http://www.uniprot.org/taxonomy/).

This can be used on a downloaded tab-separated taxonomy file from Uniprot or by querying the database directly (only recommended for small queries).

## Local installation

using `pip`:

    $ git clone git@github.com:zhoulab/uniprot-taxonomy.git
    $ cd uniprot-taxonomy
    $ pip install -e .

## Classes

### Taxonomy

Class to allow lookup of organisms by taxon or mnemonic ID.

### Organism

Class to store taxonomy information of individual organisms.

## Examples

### Downloaded file

    > tax = Taxonomy('taxonomy-all.tab')
    > tax['HUMAN']
    Organism(taxon=9606,mnemonic="HUMAN")
    > tax[9606]
    Organism(taxon=9606,mnemonic="HUMAN")
    > tax[9606].lineage
    ['Eukaryota',
     'Metazoa',
     'Chordata',
     'Craniata',
     'Vertebrata',
     'Euteleostomi',
     'Mammalia',
     'Eutheria',
     'Euarchontoglires',
     'Primates',
     'Haplorrhini',
     'Catarrhini',
     'Hominidae',
     'Homo']

### Querying the Uniprot database

    > page = get_organisms_page(fmt='tab', mnemonic='HUMAN')
    > organisms = get_organisms(page)
    > organisms.next()
    Organism(taxon=9606,mnemonic="HUMAN")
