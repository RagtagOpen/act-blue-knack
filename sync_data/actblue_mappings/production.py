ACTBLUE_TO_KNACK_MAPPING_SCALARS = {
    'contribution#createdAt': 'field_638',
    'contribution#recurringDuration': 'field_640',
    'contribution#contributionForm': ['field_643', 'field_671'],
    'contribution#refcode': 'field_646',
    'donor#firstname': 'field_647',
    'donor#lastname': 'field_648',
    'donor#addr1': 'field_649',
    'donor#city': 'field_651',
    'donor#state': 'field_652',
    'donor#zip': 'field_653',  # String, not an int
    'donor#country': 'field_654',
    'donor#employerData#occupation': 'field_655',
    'donor#employerData#employer': 'field_656',
    'donor#email': 'field_874',
    'donor#phone': 'field_658',  # String, not an int
}

ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS = {
    'lineitems#entityId': 'field_684',
    'lineitems#amount': 'field_639',
    'lineitems#committeeName': 'field_642',
}

KNACK_OBJECT_ID = '32'

FIELD_PREFIXES = {
    'field_643': 'https:/secure.actblue.com/donate/'
}
