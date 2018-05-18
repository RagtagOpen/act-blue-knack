ACTBLUE_TO_KNACK_MAPPING_SCALARS = {
    'contribution#createdAt': 'field_969',
    'contribution#contributionForm': ['field_982', 'field_988'],
    'contribution#refcode': 'field_987',
    'donor#firstname': 'field_972',
    'donor#lastname': 'field_973',
    'donor#addr1': 'field_974',
    'donor#city': 'field_975',
    'donor#state': 'field_976',
    'donor#zip': 'field_977',  # String, not an int
    'donor#country': 'field_978',
    'donor#email': 'field_984',
    'donor#phone': 'field_986',  # String, not an int
}

ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS = {
    'lineitems#entityId': 'field_981',
    'lineitems#amount': 'field_970',
    'lineitems#committeeName': 'field_971',
}

KNACK_OBJECT_ID = '42'

FIELD_PREFIXES = {
    'field_982': 'https:/secure.actblue.com/donate/'
}
