# -*- coding: utf-8 -*-

from typing import Mapping, Optional

import pandas as pd

from bio2bel.manager import AbstractManager
from bio2bel.manager.flask_manager import FlaskMixin
from bio2bel.manager.namespace_manager import BELNamespaceManagerMixin
from pybel import BELGraph
from pybel.manager.models import Namespace, NamespaceEntry
from .constants import MODULE_NAME
from .models import Base, Gene
from .parsers import get_genes_df


class Manager(AbstractManager, BELNamespaceManagerMixin, FlaskMixin):
    """Manages the RGD database."""

    _base = Base
    module_name = MODULE_NAME
    flask_admin_models = [Gene]
    namespace_model = Gene

    def count_genes(self) -> int:
        """Count the genes in the database."""
        return self._count_model(Gene)

    def summarize(self) -> Mapping[str, int]:
        """Summarize the database.s"""
        return dict(genes=self.count_genes())

    def is_populated(self):
        """Check if the database is populated."""
        return 0 < self.count_genes()

    def populate(self, genes_url: Optional[str] = None) -> None:
        """Populate the database."""
        genes_df = get_genes_df(url=genes_url)

        # delete entries with missing entrez identifiers
        genes_df = genes_df[pd.notna(genes_df.entrez_id)]
        genes_df.entrez_id = genes_df.entrez_id.map(int).map(str)

        # add protein-coding to all missing entries
        genes_df.loc[pd.isna(genes_df.gene_type), 'gene_type'] = 'protein-coding'

        genes_df.to_sql(Gene.__tablename__, self.engine, if_exists='append', index=False)
        self.session.commit()

    def get_gene_by_rgd_id(self, rgd_id: str) -> Optional[Gene]:
        """Get a gene by its RGD gene identifier, if it exists.

        :param rgd_id: An RGD gene identifier (automatically strips the "RGD:" prefix if present)
        """
        raise NotImplementedError

    def get_gene_by_rgd_symbol(self, rgd_symbol: str) -> Optional[Gene]:
        """Get a gene by its RGD gene symbol, if it exists.

        :param rgd_symbol: An RGD gene symbol
        """
        raise NotImplementedError

    def get_gene_by_entrez_id(self, entrez_id: str) -> Optional[Gene]:
        """Get a gene by its Entrez gene identifier, if it exists.

        :param entrez_id: An Entrez gene identifier
        """
        raise NotImplementedError

    def enrich_entrez_equivalences(self, graph: BELGraph):
        """Add equivalent Entrez nodes for RGD nodes."""
        raise NotImplementedError

    def _create_namespace_entry_from_model(self, gene: Gene, namespace: Namespace) -> NamespaceEntry:
        return NamespaceEntry(
            encoding=gene.bel_encoding,
            name=gene.symbol,
            identifier=gene.rgd_id,
            namespace=namespace
        )

    @staticmethod
    def _get_identifier(gene: Gene):
        return gene.rgd_id
