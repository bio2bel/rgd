# -*- coding: utf-8 -*-

import networkx as nx
import pandas as pd
from typing import Iterable, Mapping, Optional, Tuple

from bio2bel.manager import AbstractManager
from bio2bel.manager.flask_manager import FlaskMixin
from bio2bel.manager.namespace_manager import BELNamespaceManagerMixin
from pybel import BELGraph
from pybel.constants import IDENTIFIER, NAME, NAMESPACE
from pybel.dsl import BaseEntity
from pybel.manager.models import Namespace, NamespaceEntry
from .constants import MODULE_NAME
from .models import Base, RatGene
from .parsers import get_genes_df


class Manager(AbstractManager, BELNamespaceManagerMixin, FlaskMixin):
    """Rat gene nomenclature and orthologies."""

    _base = Base
    module_name = MODULE_NAME

    flask_admin_models = [RatGene]

    namespace_model = RatGene
    identifiers_recommended = 'Rat Genome Database'
    identifiers_pattern = '^\d{4,}$'
    identifiers_miriam = 'MIR:00000047'
    identifiers_namespace = 'rgd'
    identifiers_url = 'http://identifiers.org/rgd/'

    def count_genes(self) -> int:
        """Count the genes in the database."""
        return self._count_model(RatGene)

    def summarize(self) -> Mapping[str, int]:
        """Summarize the database.s"""
        return dict(rat_genes=self.count_genes())

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

        genes_df.to_sql(RatGene.__tablename__, self.engine, if_exists='append', index=False)
        self.session.commit()

    def get_gene_by_rgd_id(self, rgd_id: str) -> Optional[RatGene]:
        """Get a gene by its RGD gene identifier, if it exists.

        :param rgd_id: An RGD gene identifier (automatically strips the "RGD:" prefix if present)
        """
        return self.session.query(RatGene).filter(RatGene.rgd_id == rgd_id).one_or_none()

    def get_gene_by_rgd_symbol(self, rgd_symbol: str) -> Optional[RatGene]:
        """Get a gene by its RGD gene symbol, if it exists.

        :param rgd_symbol: An RGD gene symbol
        """
        return self.session.query(RatGene).filter(RatGene.symbol == rgd_symbol).one_or_none()

    def get_gene_by_entrez_id(self, entrez_id: str) -> Optional[RatGene]:
        """Get a gene by its Entrez gene identifier, if it exists.

        :param entrez_id: An Entrez gene identifier
        """
        return self.session.query(RatGene).filter(RatGene.entrez_id == entrez_id).one_or_none()

    def enrich_entrez_equivalences(self, graph: BELGraph):
        """Add equivalent Entrez nodes for RGD nodes."""
        raise NotImplementedError

    def normalize_rat_genes(self, graph: BELGraph) -> None:
        mapping = {
            node: gene_model.as_bel(func=node.function)
            for node, gene_model in self.iter_rat_genes(graph)
        }
        nx.relabel_nodes(graph, mapping, copy=False)

    def iter_rat_genes(self, graph: BELGraph) -> Iterable[Tuple[BaseEntity, RatGene]]:
        """Iterate over pairs of BEL nodes and Rat genes."""
        for node in graph:
            rat_gene = self.get_rat_gene_from_bel(node)
            if rat_gene is not None:
                yield node, rat_gene

    def get_rat_gene_from_bel(self, node: BaseEntity) -> Optional[RatGene]:
        namespace = node.get(NAMESPACE)

        if not namespace or namespace.lower() not in {'rgd', 'rgdid'}:
            return

        identifier = node.get(IDENTIFIER)
        name = node.get(NAME)

        if identifier is None and name is None:
            raise ValueError

        if namespace.lower() == 'rgdid':
            return self.get_gene_by_rgd_id(name)

        elif namespace.lower() == 'rgd':
            if identifier is not None:
                return self.get_gene_by_rgd_id(identifier)
            else:  # elif name is not None:
                return self.get_gene_by_rgd_symbol(name)

    def _create_namespace_entry_from_model(self, gene: RatGene, namespace: Namespace) -> NamespaceEntry:
        return NamespaceEntry(
            encoding=gene.bel_encoding,
            name=gene.symbol,
            identifier=gene.rgd_id,
            namespace=namespace
        )

    @staticmethod
    def _get_identifier(gene: RatGene):
        return gene.rgd_id
