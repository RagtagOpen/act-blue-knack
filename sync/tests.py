import base64
import json
import logging
from copy import deepcopy
from unittest.mock import Mock, patch

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

client_headers = {
    "HTTP_AUTHORIZATION": "Basic: {}".format(
        base64.b64encode(
            f"{settings.ACTBLUE_USERNAME}:{settings.ACTBLUE_PASSWORD}".encode("utf-8")
        ).decode("utf-8")
    )
}

REQUIRED_FIELDS_ONLY = {
    "donor": {
        "firstname": "PIPPA",
        "lastname": "PRIVACY_ORIENTED",
        "addr1": "1234 Main Street",
        "city": "Chattanooga",
        "state": "TN",
        "zip": "30709",
        "country": "United States",
        "isEligibleForExpressLane": True,
        "employerData": {
            "employer": "Ragtag",
            "occupation": "Awesome Volunteer",
            "employerAddr1": None,
            "employerCity": None,
            "employerState": None,
            "employerCountry": None,
        },
    },
    "contribution": {
        "createdAt": "2018-01-24T21:43:36-05:00",
        "orderNumber": "AB12345678",
        "contributionForm": "example-slug",
        "refcode": "sample ref code",
        "refcode2": "sample ref code 2",
        "creditCardExpiration": "11/2020",
        "recurringPeriod": "once",
        "recurringDuration": 1,
        "abTestName": None,
        "isRecurring": False,
        "isPaypal": False,
        "isMobile": True,
        "abTestVariation": None,
        "isExpress": True,
        "withExpressLane": False,
        "expressSignup": False,
        "uniqueIdentifier": "5e829b71-9968-48e2-a824-8a4de908e61f",
        "status": "approved",
        "thanksUrl": (
            "https://secure.actblue.com/contribute/thanks/AB12345678"
            "?k=9f59dfbe&success=True"
        ),
    },
    "lineitems": [
        {
            "sequence": 0,
            "entityId": 12345,
            "fecId": None,
            "committeeName": "Example Committee",
            "amount": "1000.0",
            "paidAt": "2018-01-24T21:43:44-05:00",
            "lineitemId": 123456789,
        },
        {
            "sequence": 0,
            "entityId": 123456,
            "fecId": None,
            "committeeName": "Second Example Committee",
            "amount": "10.0",
            "paidAt": "2018-01-25T21:43:44-05:00",
            "lineitemId": 123456,
        },
    ],
}

ALL_FIELDS = {
    "donor": {
        "firstname": "ESMERELDA",
        "lastname": "TEST",
        "addr1": "1234 Main Street",
        "city": "Chattanooga",
        "state": "TN",
        "zip": "30709",
        "country": "United States",
        "email": "example@domain.com",
        "phone": "4235551212",
        "isEligibleForExpressLane": True,
        "employerData": {
            "employer": "Ragtag",
            "occupation": "Awesome Volunteer",
            "employerAddr1": None,
            "employerCity": None,
            "employerState": None,
            "employerCountry": None,
        },
    },
    "contribution": {
        "createdAt": "2018-01-24T21:43:36-05:00",
        "orderNumber": "AB12345678",
        "contributionForm": "example-slug",
        "refcode": "sample ref code",
        "refcode2": "sample ref code 2",
        "creditCardExpiration": "11/2020",
        "recurringPeriod": "once",
        "recurringDuration": 1,
        "abTestName": None,
        "isRecurring": False,
        "isPaypal": False,
        "isMobile": True,
        "abTestVariation": None,
        "isExpress": True,
        "withExpressLane": False,
        "expressSignup": False,
        "uniqueIdentifier": "5e829b71-9968-48e2-a824-8a4de908e61f",
        "status": "approved",
        "thanksUrl": (
            "https://secure.actblue.com/contribute/thanks/AB12345678"
            "?k=9f59dfbe&success=True"
        ),
    },
    "lineitems": [
        {
            "sequence": 0,
            "entityId": 12345,
            "fecId": None,
            "committeeName": "Example Committee",
            "amount": "1000.0",
            "paidAt": "2018-01-24T21:43:44-05:00",
            "lineitemId": 123456789,
        },
        {
            "sequence": 0,
            "entityId": 123456,
            "fecId": None,
            "committeeName": "Second Example Committee",
            "amount": "10.0",
            "paidAt": "2018-01-25T21:43:44-05:00",
            "lineitemId": 123456,
        },
    ],
}


def mock_knackload_load(payload, knack_object_id):
    return (
        200,
        json.dumps(
            {
                "id": "5d09414f2ceba5000cc0f572",
                "field_896": "sample ref code",
                "field_896_raw": "sample ref code",
                "field_889": "$1,000.00",
                "field_889_raw": "1,000.00",
                "field_888": "01/24/2018",
                "field_888_raw": {
                    "date": "01/24/2018",
                    "date_formatted": "01/24/2018",
                    "hours": "12",
                    "minutes": "00",
                    "am_pm": "AM",
                    "unix_timestamp": 1516752000000,
                    "iso_timestamp": "2018-01-24T00:00:00.000Z",
                    "timestamp": "01/24/2018 12:00 am",
                    "time": 1123,
                },
                "field_892": "Example Committee",
                "field_892_raw": "Example Committee",
                "field_893": (
                    '<a href="https://secure.actblue.com/donate/example-slug">'
                    "https://secure.actblue.com/donate/example-slug</a>"
                ),
                "field_893_raw": {
                    "url": "https://secure.actblue.com/donate/example-slug"
                },
                "field_897": "PIPPA",
                "field_897_raw": "PIPPA",
                "field_898": "PRIVACY_ORIENTED",
                "field_898_raw": "PRIVACY_ORIENTED",
                "field_935": 12345,
                "field_935_raw": 12345,
                "field_907": "",
                "field_908": "",
                "field_887": "",
                "field_922": "example-slug",
                "field_922_raw": "example-slug",
                "field_931": "",
                "field_890": "",
                "field_891": "",
                "field_886": "",
                "field_894": "",
                "field_895": "",
                "field_899": "1234 Main Street",
                "field_899_raw": "1234 Main Street",
                "field_900": "",
                "field_901": "Chattanooga",
                "field_901_raw": "Chattanooga",
                "field_902": "TN",
                "field_902_raw": "TN",
                "field_903": 30709,
                "field_903_raw": 30709,
                "field_904": "United States",
                "field_904_raw": "United States",
                "field_905": "",
                "field_906": "",
                "field_909": "",
                "field_910": "",
                "field_911": "",
                "field_912": "",
                "field_913": "",
                "field_914": "",
                "field_915": "",
                "field_916": "",
                "field_917": "",
                "field_918": "",
                "field_919": "",
                "field_920": "",
                "field_921": "",
                "field_923": "",
                "field_924": "",
                "field_925": "",
                "field_926": "",
                "field_927": "",
                "field_928": "",
                "field_929": "",
                "field_930": "",
                "field_932": "",
                "field_933": "",
                "field_934": "",
                "field_936": "",
                "field_937": "",
                "field_938": "",
                "field_939": "",
                "field_940": "06/18/2019",
                "field_940_raw": {
                    "date": "06/18/2019",
                    "date_formatted": "06/18/2019",
                    "hours": "12",
                    "minutes": "00",
                    "am_pm": "AM",
                    "unix_timestamp": 1560816000000,
                    "iso_timestamp": "2019-06-18T00:00:00.000Z",
                    "timestamp": "06/18/2019 12:00 am",
                    "time": 720,
                },
                "field_941": "",
                "field_942": "",
                "field_943": "",
                "field_944": "",
                "field_945": "",
                "field_946": "",
                "field_947": "",
                "field_948": "",
                "field_949": "",
                "field_950": "",
                "field_951": "",
                "field_952": "",
                "field_953": "",
                "field_954": "",
                "field_955": "",
                "field_956": "",
                "field_957": "",
                "field_958": "",
                "field_959": "",
                "field_960": "",
                "field_961": "",
                "field_962": "",
                "field_963": "",
                "field_964": "",
                "field_965": "",
            }
        ),
    )


class MockKnackAPITestsMixin:
    do_mock = True

    def setUp(self):
        if self.do_mock:
            self.patcher = patch("sync.views.knackload.load", mock_knackload_load)
            self.patcher.start()

    def tearDown(self):
        if self.do_mock:
            self.patcher.stop()


class SyncViewTest(MockKnackAPITestsMixin, TestCase):
    def test_authentication_fails_no_auth(self):
        with self.assertLogs(level="WARNING") as logs:
            response = self.client.post(
                reverse("sync"),
                json.dumps(REQUIRED_FIELDS_ONLY),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 403)
        self.assertIn(
            (
                "WARNING:sync.views:Unauthorized access attempted with no "
                "authorization header"
            ),
            logs.output,
        )

    def test_authentication_fails_bad_auth(self):
        with self.assertLogs(level="WARNING") as logs:
            response = self.client.post(
                reverse("sync"),
                json.dumps(REQUIRED_FIELDS_ONLY),
                content_type="application/json",
                HTTP_AUTHORIZATION="Basic: {}".format(
                    base64.b64encode(b"foo:bar").decode("utf-8")
                ),
            )
            self.assertEqual(response.status_code, 403)
        self.assertIn(
            "WARNING:sync.views:Unauthorized access attempted with username foo",
            logs.output,
        )

    def test_required_fields(self):
        with self.assertLogs(level="INFO") as logs:
            response = self.client.post(
                reverse("sync"),
                json.dumps(REQUIRED_FIELDS_ONLY),
                content_type="application/json",
                **client_headers,
            )
            self.assertEqual(response.status_code, 200)
        self.assertIn(
            (
                f"INFO:sync.views:Received order number "
                f"{REQUIRED_FIELDS_ONLY['contribution']['orderNumber']} from ActBlue"
            ),
            logs.output,
        )

    def test_missing_order_number(self):
        data = deepcopy(REQUIRED_FIELDS_ONLY)
        del data["contribution"]["orderNumber"]
        with self.assertLogs(level="WARNING") as logs:
            response = self.client.post(
                reverse("sync"),
                json.dumps(data),
                content_type="application/json",
                **client_headers,
            )
            self.assertEqual(response.status_code, 200)
        self.assertIn(
            (
                "WARNING:sync.views:ActBlue data warning: contribution#orderNumber "
                "not found"
            ),
            logs.output,
        )

    def test_missing_required_fields_firstname(self):
        data = deepcopy(REQUIRED_FIELDS_ONLY)
        del data["donor"]["firstname"]
        with self.assertLogs(level="WARNING") as logs:
            response = self.client.post(
                reverse("sync"),
                json.dumps(data),
                content_type="application/json",
                **client_headers,
            )
            self.assertEqual(response.status_code, 200)
        self.assertIn(
            "WARNING:sync.views:ActBlue data warning: first name not found", logs.output
        )

    def test_missing_required_fields_lastname(self):
        data = deepcopy(REQUIRED_FIELDS_ONLY)
        del data["donor"]["lastname"]
        with self.assertLogs(level="WARNING") as logs:
            response = self.client.post(
                reverse("sync"),
                json.dumps(data),
                content_type="application/json",
                **client_headers,
            )
            self.assertEqual(response.status_code, 200)
        self.assertIn(
            "WARNING:sync.views:ActBlue data warning: last name not found", logs.output
        )

    def test_missing_required_fields_addr1(self):
        data = deepcopy(REQUIRED_FIELDS_ONLY)
        del data["donor"]["addr1"]
        with self.assertLogs(level="WARNING") as logs:
            response = self.client.post(
                reverse("sync"),
                json.dumps(data),
                content_type="application/json",
                **client_headers,
            )
            self.assertEqual(response.status_code, 200)
        self.assertIn(
            "WARNING:sync.views:ActBlue data warning: addr1 not found", logs.output
        )

    def test_missing_required_fields_city(self):
        data = deepcopy(REQUIRED_FIELDS_ONLY)
        del data["donor"]["city"]
        with self.assertLogs(level="WARNING") as logs:
            response = self.client.post(
                reverse("sync"),
                json.dumps(data),
                content_type="application/json",
                **client_headers,
            )
            self.assertEqual(response.status_code, 200)
        self.assertIn(
            "WARNING:sync.views:ActBlue data warning: city not found", logs.output
        )

    def test_missing_required_fields_state(self):
        data = deepcopy(REQUIRED_FIELDS_ONLY)
        del data["donor"]["state"]
        with self.assertLogs(level="WARNING") as logs:
            response = self.client.post(
                reverse("sync"),
                json.dumps(data),
                content_type="application/json",
                **client_headers,
            )
            self.assertEqual(response.status_code, 200)
        self.assertIn(
            "WARNING:sync.views:ActBlue data warning: state not found", logs.output
        )

    def test_missing_required_fields_zip(self):
        data = deepcopy(REQUIRED_FIELDS_ONLY)
        del data["donor"]["zip"]
        with self.assertLogs(level="WARNING") as logs:
            response = self.client.post(
                reverse("sync"),
                json.dumps(data),
                content_type="application/json",
                **client_headers,
            )
            self.assertEqual(response.status_code, 200)
        self.assertIn(
            "WARNING:sync.views:ActBlue data warning: zip not found", logs.output
        )

    def test_missing_required_fields_country(self):
        data = deepcopy(REQUIRED_FIELDS_ONLY)
        del data["donor"]["country"]
        with self.assertLogs(level="WARNING") as logs:
            response = self.client.post(
                reverse("sync"),
                json.dumps(data),
                content_type="application/json",
                **client_headers,
            )
            self.assertEqual(response.status_code, 200)
        self.assertIn(
            "WARNING:sync.views:ActBlue data warning: country not found", logs.output
        )

    def test_all_fields(self):
        response = self.client.post(
            reverse("sync"),
            json.dumps(ALL_FIELDS),
            content_type="application/json",
            **client_headers,
        )
