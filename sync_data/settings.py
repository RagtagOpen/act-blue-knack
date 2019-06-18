import os

from .base_settings import *

DEBUG = False

if os.getenv('KNACK_ENVIRONMENT') == 'production':
    from .actblue_mappings.production import (
        ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS,
        ACTBLUE_TO_KNACK_MAPPING_SCALARS,
        KNACK_DONOR_REQUIRED_FIELDS,
        KNACK_OBJECT_ID,
        FIELD_PREFIXES,
        TIMEZONE_CONVERSION_NEEDED,
    )
else:
    from .actblue_mappings.testing import (
        ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS,
        ACTBLUE_TO_KNACK_MAPPING_SCALARS,
        KNACK_DONOR_REQUIRED_FIELDS,
        KNACK_OBJECT_ID,
        FIELD_PREFIXES,
        TIMEZONE_CONVERSION_NEEDED,
    )
