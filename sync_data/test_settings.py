from .actblue_mappings.testing import (
    ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS,
    ACTBLUE_TO_KNACK_MAPPING_SCALARS,
    FIELD_PREFIXES,
    KNACK_DONOR_REQUIRED_FIELDS,
    KNACK_OBJECT_ID,
    TIMEZONE_CONVERSION_NEEDED,
)
from .base_settings import *

DEBUG = True

# this is needed for running tests
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "actblue-knack"}
}
