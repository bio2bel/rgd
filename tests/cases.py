# -*- coding: utf--*-

from bio2bel.testing import AbstractTemporaryCacheClassMixin
from bio2bel_rgd import Manager
from tests.constants import TEST_GENES_URL


class TemporaryCacheClassMixin(AbstractTemporaryCacheClassMixin):
    Manager = Manager

    @classmethod
    def populate(cls):
        cls.manager.populate(
            genes_url=TEST_GENES_URL,
        )
