#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for sending ActBlue data to a Knack database
"""

import json
import os
import requests

def knack_credentials():
    """
    Read Knack credentials from local environment and construct headers object.

    Returns a tuple of the Knack URI and the headers.
    """

    api_key = os.environ['KNACK_API_KEY']
    api_id = os.environ['KNACK_API_ID']
    headers = {
        'Content-Type': "application/json",
        'X-Knack-Application-Id': "{0}".format(api_id),
        'X-Knack-REST-API-KEY': "{0}".format(api_key),
        }
    knack_uri = os.environ['KNACK_URI']

    return knack_uri, headers

def load(payload):
    """
    Read JSON as a string and POST it to the Knack database.

    Returns 500 if the JSON is not valid.
    Returns the status code from the POST to Knack otherwise.
    """
    knack_uri, headers = knack_credentials()
    # Check for valid JSON so we don't send bad data to Knack
    try:
        json.loads(payload)
    except ValueError:
        return 500, 'Payload is invalid json'
    response = requests.request("POST", knack_uri, data=payload, headers=headers)

    return response.status_code, response.text
