ACTBLUE_TO_KNACK_MAPPING_SCALARS = {
    'contribution#createdAt': 'field_888',
    'contribution#contributionForm': ['field_893', 'field_922'],
    'contribution#refcode': 'field_896',
    'donor#firstname': 'field_897',
    'donor#lastname': 'field_898',
    'donor#addr1': 'field_899',
    'donor#city': 'field_901',
    'donor#state': 'field_902',
    'donor#zip': 'field_903',  # String, not an int
    'donor#country': 'field_904',
    'donor#email': 'field_908',
    'donor#phone': 'field_909',  # String, not an int
}

ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS = {
    'lineitems#entityId': 'field_935',
    'lineitems#amount': 'field_889',
    'lineitems#committeeName': 'field_892',
}

KNACK_OBJECT_ID = '41'

FIELD_PREFIXES = {
    'field_893': 'https:/secure.actblue.com/donate/'
}
