# -*- coding: utf--*-

from bio2bel_rgd import Manager
from tests.cases import TemporaryCacheClassMixin


class TestPopulate(TemporaryCacheClassMixin):
    manager: Manager

    def test_count(self):
        self.assertEqual(9, self.manager.count_genes())
