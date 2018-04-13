#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for sending ActBlue data to a Knack database
"""

import json
import os
import requests

KNACK_URI = 'https://api.knack.com/v1/objects/object_{}/records'

def knack_credentials():
    """
    Read Knack credentials from the local environment and construct headers object.

    Returns the headers with the the api key and api id.
    """

    api_key = os.environ['KNACK_API_KEY']
    api_id = os.environ['KNACK_API_ID']
    headers = {
        'Content-Type': "application/json",
        'X-Knack-Application-Id': "{0}".format(api_id),
        'X-Knack-REST-API-KEY': "{0}".format(api_key),
        }

    return headers

def knack_object_id():
    """
    Read the Knack object id from the local environment.
    """
    return os.environ['KNACK_OBJECT_ID']

def load(payload):
    """
    Read JSON as a string and POST it to the Knack database.

    Returns 500 if the JSON is not valid.
    Returns the status code from the POST to Knack otherwise.
    """
    headers = knack_credentials()
    # Check for valid JSON so we don't send bad data to Knack
    try:
        json.loads(payload)
    except ValueError:
        return 500, 'Payload is invalid json'

    object_id  = knack_object_id()
    uri = KNACK_URI.format(object_id)
    response = requests.request("POST", uri, data=payload, headers=headers)

    return response.status_code, response.text
