# -*- coding: utf-8 -*-

"""This module contains constants for the Bio2BEL RGD package"""

from bio2bel.utils import get_connection, get_data_dir

MODULE_NAME = 'rgd'
DATA_DIR = get_data_dir(MODULE_NAME)
DEFAULT_CACHE_CONNECTION = get_connection(MODULE_NAME)
