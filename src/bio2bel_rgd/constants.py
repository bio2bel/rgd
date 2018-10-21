# -*- coding: utf--*-

"""This module contains constants for the Bio2BEL RGD package."""

import os

from bio2bel import get_data_dir

MODULE_NAME = 'rgd'
DATA_DIR = get_data_dir(MODULE_NAME)

GENES_URL = 'ftp://ftp.rgd.mcw.edu/pub/data_release/GENES_RAT.txt'
GENES_PATH = os.path.join(DATA_DIR, 'GENES_RAT.txt')
GENES_HEADER = [
    'GENE_RGD_ID',
    'SYMBOL',
    'NAME',
    'GENE_DESC',
    'CHROMOSOME_CELERA',
    'CHROMOSOME_[oldAssembly#] chromosome for the old reference assembly',
    'CHROMOSOME_[newAssembly#] chromosome for the current reference assembly',
    'FISH_BAND',
    'START_POS_CELERA',
    'STOP_POS_CELERA',
    'STRAND_CELERA',
    'START_POS_[oldAssembly#]',
    'STOP_POS_[oldAssembly#]',
    'STRAND_[oldAssembly#]',
    'START_POS_[newAssembly#]',
    'STOP_POS_[newAssembly#]',
    'STRAND_[newAssembly#]',
    'CURATED_REF_RGD_ID',
    'CURATED_REF_PUBMED_ID',
    'UNCURATED_PUBMED_ID',
    'NCBI_GENE_ID',
    'UNIPROT_ID',
    'UNCURATED_REF_MEDLINE_ID',
    'GENBANK_NUCLEOTIDE',
    'TIGR_ID',
    'GENBANK_PROTEIN',
    'UNIGENE_ID',
    'SSLP_RGD_ID',
    'SSLP_SYMBOL',
    'OLD_SYMBOL',
    'OLD_NAME',
    'QTL_RGD_ID',
    'QTL_SYMBOL',
    'NOMENCLATURE_STATUS',
    'SPLICE_RGD_ID',
    'SPLICE_SYMBOL',
    'GENE_TYPE',
    'ENSEMBL_ID',
]
