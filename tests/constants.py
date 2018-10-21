# -*- coding: utf-8 -*-

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
resources_path = os.path.join(dir_path, 'resources')

TEST_ORTHOLOGS_URL = os.path.join(resources_path, 'RGD_ORTHOLOGS.txt')
TEST_GENES_URL = os.path.join(resources_path, 'test.GENES_RAT.txt')
