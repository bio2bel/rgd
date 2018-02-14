# -*- coding: utf-8 -*-


class Manager(object):
    """Manages the RGD database"""

    def __init__(self, connection=None):
        """

        :param Optional[str] connection:
        """
        raise NotImplementedError

    def drop_all(self):
        """Drops the database"""
        raise NotImplementedError

    def create_all(self):
        """Creates the database"""
        raise NotImplementedError

    def populate(self):
        """Populates the database"""
        raise NotImplementedError

    def get_gene_by_rgd_id(self, rgd_id):
        """Gets a gene by its RGD gene identifier if it exists

        :param str mgi_id: An RGD gene identifier (automatically strips the "RGD:" prefix if present)
        :rtype: Optional[Gene]
        """
        raise NotImplementedError

    def get_gene_by_rgd_symbol(self, rgd_symbol):
        """Gets a gene by its RGD gene symbol if it exists

        :param str rgd_symbol: An RGD gene symbol
        :rtype: Optional[Gene]
        """
        raise NotImplementedError

    def get_gene_by_entrez_id(self, entrez_id):
        """Gets a gene by its Entrez gene identifier if it exists

        :param str entrez_id: An Entrez gene identifier
        :rtype: Optional[Gene]
        """
        raise NotImplementedError

    def enrich_entrez_equivalences(self, graph):
        """Adds equivalent Entrez nodes for RGD nodes

        :type graph: pybel.BELGraph
        """
        raise NotImplementedError
