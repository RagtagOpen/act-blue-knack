# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import base64
import json

from knackload import knackload

from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

def log_debug(string):
    if getattr(settings, 'DEBUG'):
        print(string)

@csrf_exempt
def sync(request):
    """
    Entry point.  Receives a POST from ActBlue, transforms it, and POSTs it on to Knack

    Returns a 200, 403, or 500 to ActBlue.
    """
    authorized = auth(request)
    if request.method == 'POST' and authorized:
        actblue_data = json.loads(request.body)
        knack_values = transform(actblue_data)

        # This will not respond to ActBlue until we've sent every item to Knack.
        # This _could_ cause timeouts, but might be OK?
        # Will depend on how many line items we get.
        for knack_value in knack_values:
            log_debug('sent {} to knack'.format(json.dumps(knack_value, indent=4)))

            return_status, result_string = knackload.load(json.dumps(knack_value))

            if return_status != 200:
                order_id = actblue_data['contribution']['orderNumber']
                entity_id_key = settings.ACTBLUE_TO_KNACK_MAPPING_SCALARS['lineitems#entityId']
                lineitem_entity_id = knack_value[entity_id_key]

                error_msg = 'Error: We failed to send order {}, lineitem {} to knack'
                print(error_msg.format(order_id, lineitem_entity_id))
                log_debug('Error: We failed to send ' + knack_value)

                return HttpResponseServerError()
            else:
                result_data = json.loads(result_string)
                log_debug(json.dumps(result_data, indent=4))

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
    amount_key = mapping['lineitems#amount']
    entity_key = mapping['lineitems#entityId']

    for lineitem in lineitems:
        knack_lineitem = {}
        knack_lineitem[amount_key] = lineitem.get('amount')
        knack_lineitem[entity_key] = lineitem.get('entityId')
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
            for val in value:
                knack_values[val] = walk(path, actblue_values)
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
    """
    Make sure an incoming request is authorized.

    Returns a boolean.
    """
    auth_header = request.META['HTTP_AUTHORIZATION']
    encoded = auth_header.split(' ')[1].encode('ascii')
    username, password = base64.urlsafe_b64decode(encoded).split(b':')
    username = username.decode('utf-8')
    password = password.decode('utf-8')
    # TODO add encryption
    return username == settings.ACTBLUE_USERNAME and password == settings.ACTBLUE_PASSWORD
