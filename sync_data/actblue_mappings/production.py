ACTBLUE_TO_KNACK_MAPPING_SCALARS = {
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
    'lineitems#paidAt': 'field_969',
    'lineitems#entityId': 'field_981',
    'lineitems#amount': 'field_970',
    'lineitems#committeeName': 'field_971',
}

KNACK_DONOR_REQUIRED_FIELDS = [
    'field_897', # first name
    'field_898', # last name
    'field_899', # addr1
    'field_901', # city
    'field_902', # state
    'field_903', # zip
    'field_904', # country
]

KNACK_OBJECT_ID = '42'

FIELD_PREFIXES = {
    'field_982': 'https://secure.actblue.com/donate/'
}

TIMEZONE_CONVERSION_NEEDED = ['field_969']
