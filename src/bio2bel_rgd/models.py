# -*- coding: utf-8 -*-

"""RGD database models."""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

import pybel.dsl
from .constants import MODULE_NAME

Base = declarative_base()

GENE_TABLE_NAME = f'{MODULE_NAME}_gene'

marker_type_to_encoding = {
    'pseudo': 'G',
    'protein-coding': 'GRP',
    'ncrna': 'GR',
    'gene': 'G',
    'nan': 'G',
    'snrna': 'GR',
    'trna': 'GR',
    'rrna': 'GR',
}


class Gene(Base):  # type: ignore
    """Gene table."""

    __tablename__ = GENE_TABLE_NAME

    id = Column(Integer, primary_key=True)

    rgd_id = Column(String(255), nullable=False, index=True)
    symbol = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    entrez_id = Column(String(255), nullable=False, index=True)
    gene_type = Column(String(255), nullable=False, index=True)

    @property
    def bel_encoding(self) -> str:
        return marker_type_to_encoding[self.gene_type]

    def __repr__(self):
        return str(self.rgd_id)

    def __str__(self):
        return str(self.rgd_id)

    def serialize_to_protein_node(self) -> pybel.dsl.Gene:
        """Serialize to PyBEL node data dictionary."""
        return pybel.dsl.Gene(
            namespace='rgd',
            name=self.symbol,
            identifier=str(self.rgd_id)
        )
