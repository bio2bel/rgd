# -*- coding: utf--*-

from bio2bel.downloading import make_df_getter
from .constants import GENES_PATH, GENES_URL

__all__ = [
    'get_genes_df',
]

get_genes_df = make_df_getter(
    GENES_URL,
    GENES_PATH,
    sep='\t',
    usecols=[
        0,  # RGD identifier
        1,  # Symbol
        2,  # Name
        3,  # Description
        20,  # NCBI_GENE_ID
        36,  # Gene type
    ],
    names=[
        'rgd_id',
        'symbol',
        'name',
        'description',
        'entrez_id',
        'gene_type',
    ],
    header=0,
    comment='#',
)
