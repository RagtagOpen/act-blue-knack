from .base_settings import *

DEBUG = False

ACTBLUE_TO_KNACK_MAPPING = {
    'contribution#createdAt': '638',
    'contribution#recurringDuration': '640',
    'contribution#contributionForm': '643',
    'contribution#refcode': '646',
    'donor#firstname': '647',
    'donor#lastname': '648',
    'donor#addr1': '649',
    'donor#city': '651',
    'donor#state': '652',
    'donor#zip': '653', # String, not an int
    'donor#country': '654',
    'donor#employerData#occupation': '655',
    'donor#employerData#employer': '656',
    'donor#email': '874',
    'donor#phone': '658', # String, not an int
    'lineitems#entityId': '684',
    'lineitems#amount': '639',
}
