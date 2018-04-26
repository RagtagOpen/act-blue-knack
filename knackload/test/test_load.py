#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for Knackload
"""

from unittest.mock import MagicMock
import requests
import knackload

KNACK_OBJECT_ID = 1000

class MockResponse():
    """A mock response for Requests"""
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


def test_load_success():
    mock_credentials = ('mock_uri', 'mock_headers')
    mock_response = MockResponse(200, 'mock_text')
    knackload.knack_credentials = MagicMock(return_value=mock_credentials)
    knackload.knack_object_id = MagicMock(return_value=1)
    requests.request = MagicMock(return_value=mock_response)

    test_json = '{"key": "value"}'
    status_code, text = knackload.load(test_json, KNACK_OBJECT_ID)
    assert status_code == 200
    assert text == 'mock_text'

def test_load_invalid_json():
    mock_credentials = ('mock_uri', 'mock_headers')
    knackload.knack_credentials = MagicMock(return_value=mock_credentials)
    knackload.knack_object_id = MagicMock(return_value=1)

    test_json = '{"invalid: "json"}'
    status_code, text = knackload.load(test_json, KNACK_OBJECT_ID)
    assert status_code == 500
    assert text == 'Payload is invalid json'
