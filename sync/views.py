# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import base64
import json

from knackload import knackload

from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def sync(request):
    authorized = auth(request)
    if request.method == 'POST' and authorized:
        actblue_data = json.loads(request.body)
        knack_values = transform(actblue_data)

        # This will not respond to ActBlue until we've sent every item to Knack.
        # This _could_ cause timeouts, but might be OK?
        # Will depend on how many line items we get.
        for knack_value in knack_values:
            if getattr(settings, 'DEBUG'):
                print('sent {} to knack'.format(json.dumps(knack_value, indent=4)))

            return_status, result_string = knackload.load(json.dumps(knack_value))

            if return_status != 200:
                print('Error: We failed to send {} to knack'.format(knack_value))
                return HttpResponseServerError()
            else:
                result_data = json.loads(result_string)
                if getattr(settings, 'DEBUG'):
                    print(json.dumps(result_data, indent=4))

        return HttpResponse('')
    else:
        return HttpResponseForbidden()


def get_lineitems(actblue_values, mapping):
    """
    Parse information we need from ActBlue line items.

    Returns a list of dictionaries, one dict per line item.
    """
    knack_lineitems = []
    lineitems = actblue_values['lineitems']
    amountKey = mapping['lineitems#amount']
    entityKey = mapping['lineitems#entityId']

    for lineitem in lineitems:
        knack_lineitem = {}
        knack_lineitem[amountKey] = lineitem.get('amount')
        knack_lineitem[entityKey] = lineitem.get('entityId')
        knack_lineitems.append(knack_lineitem)

    return knack_lineitems


def transform(actblue_values):
    """
    Transform ActBlue's data into a list of Knack-keyed dictionaries,
    one per line item.
    """
    knack_values = {}
    try:
        # this works in Python 2
        scalar_mapping = settings.ACTBLUE_TO_KNACK_MAPPING_SCALARS.iteritems()
        array_items_mapping = settings.ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS
    except AttributeError:
        # this works in Python 3, and returns an generator like iteritems in Python 2
        scalar_mapping = settings.ACTBLUE_TO_KNACK_MAPPING_SCALARS.items()
        array_items_mapping = settings.ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS
    for key, value in scalar_mapping:
        path = key.split('#')
        if isinstance(value, list):
            for v in value:
                knack_values[v] = walk(path, actblue_values)
        else:
            knack_values[value] = walk(path, actblue_values)

    knack_lineitems = get_lineitems(actblue_values, array_items_mapping)
    for knack_lineitem in knack_lineitems:
        knack_lineitem.update(knack_values)  # updates in-place!

    return knack_lineitems


def walk(path, container):
    """
    Recurse over the ActBlue JSON object, and get the values that we need,
    based on the settings file.

    Returns a single value for each path.
    """
    if not container or isinstance(container, str):
        return None
    key = path[0]
    if len(path) == 1:
        if key.isdigit():
            return container[int(key)]
        else:
            return container.get(path[0])
    else:
        if key.isdigit():
            new_container = container[int(key)]
        else:
            new_container = container.get(path[0])
        return walk(path[1:], new_container)


def auth(request):
    auth_header = request.META['HTTP_AUTHORIZATION']
    encoded = auth_header.split(' ')[1].encode('ascii')
    username, password = base64.urlsafe_b64decode(encoded).split(b':')
    username = username.decode('utf-8')
    password = password.decode('utf-8')
    # TODO add encryption
    return username == settings.ACTBLUE_USERNAME and password == settings.ACTBLUE_PASSWORD
