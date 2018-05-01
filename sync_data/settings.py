import os

from .base_settings import *

DEBUG = False

if os.getenv('KNACK_ENVIRONMENT') == 'production':
    from .actblue_mappings.production import ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS, ACTBLUE_TO_KNACK_MAPPING_SCALARS, KNACK_OBJECT_ID
else:
    from .actblue_mappings.testing import ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS, ACTBLUE_TO_KNACK_MAPPING_SCALARS, KNACK_OBJECT_ID
