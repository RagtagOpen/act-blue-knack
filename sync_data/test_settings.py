from .base_settings import *

ACTBLUE_TO_KNACK_MAPPING = {
    'contribution#createdAt': '888',
    'contribution#recurringDuration': '890',
    'contribution#contributionForm': '893',
    'contribution#refcode': '896',
    'donor#firstname': '897',
    'donor#lastname': '898',
    'donor#addr1': '899',
    'donor#city': '901',
    'donor#state': '902',
    'donor#zip': '903', # String, not an int
    'donor#country': '904',
    'donor#employerData#occupation': '905',
    'donor#employerData#employer': '906',
    'donor#email': '908',
    'donor#phone': '909', # String, not an int
    'lineitems#entityId': '935',
    'lineitems#amount': '889',
}
