# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import base64
import json
import logging

from dateutil import parser
from django.conf import settings
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseServerError)
from django.views.decorators.csrf import csrf_exempt
from knackload import knackload
from pytz import timezone

logger = logging.getLogger(__name__)


@csrf_exempt
def sync(request):
    """
    Entry point.  Receives a POST from ActBlue, transforms it, and POSTs it on to Knack

    Returns a 200, 403, or 500 to ActBlue.
    """
    authorized = auth(request)
    if request.method == 'POST' and authorized:
        actblue_data = json.loads(request.body)
        try:
            order_id = actblue_data['contribution']['orderNumber']
            logger.info(
                "Received order number {} from ActBlue".format(order_id))
        except Exception:
            order_id = "UNKNOWN"
            logger.warning(
                "ActBlue data warning: contribution#orderNumber not found")
        knack_values = transform(actblue_data)
        knack_object_id = settings.KNACK_OBJECT_ID

        # This will not respond to ActBlue until we've sent every item to Knack.
        # This _could_ cause timeouts, but might be OK?
        # Will depend on how many line items we get.
        for knack_value in knack_values:
            logger.debug('Knack Sending {}'.format(
                json.dumps(knack_value, indent=4)))
            try:
                entity_id_key = settings.ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS['lineitems#entityId']
                lineitem_entity_id = knack_value[entity_id_key]
            except Exception:
                logger.warning(
                    'ActBlue data warning: lineitems#entityId not found')
                lineitem_entity_id = 'UNKNOWN'

            return_status, result_string = knackload.load(
                json.dumps(knack_value), knack_object_id)

            if return_status != 200:
                logger.error('Knack Send Failed', extra={
                    'order': order_id,
                    'lineitem': lineitem_entity_id,
                    'status_code': return_status,
                })
                return HttpResponseServerError()
            else:
                logger.info('Knack Send Success: We sent order {}, lineitem {} to knack'.format(
                    order_id, lineitem_entity_id))
                result_data = json.loads(result_string)
                logger.debug(json.dumps(result_data, indent=4))

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
    committee_name = mapping['lineitems#committeeName']
    paid_at_data = mapping['lineitems#paidAt']

    for lineitem in lineitems:
        knack_lineitem = {}
        if 'amount' not in lineitem:
            logger.warning('ActBlue data warning: amount not found')
        else:
            knack_lineitem[amount_key] = lineitem.get('amount')
        if 'entityId' not in lineitem:
            logger.warning('ActBlue data warning: entityId not found')
        else:
            knack_lineitem[entity_key] = lineitem.get('entityId')
        if 'committeeName' not in lineitem:
            logger.warning('ActBlue data warning: committeeName not found')
        else:
            knack_lineitem[committee_name] = lineitem.get('committeeName')
        if 'paidAt' not in lineitem:
            logger.warning('ActBlue data warning: paidAt not found')
        else:
            knack_lineitem[paid_at_data] = lineitem.get('paidAt')
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
        field_prefixes = settings.FIELD_PREFIXES.iteritems()
        timezone_conversions_needed = settings.TIMEZONE_CONVERSION_NEEDED
    except AttributeError:
        # this works in Python 3, and returns an generator like iteritems in Python 2
        scalar_mapping = settings.ACTBLUE_TO_KNACK_MAPPING_SCALARS.items()
        array_items_mapping = settings.ACTBLUE_TO_KNACK_MAPPING_ARRAY_ITEMS
        field_prefixes = settings.FIELD_PREFIXES.items()
        timezone_conversions_needed = settings.TIMEZONE_CONVERSION_NEEDED

    knack_required_fields = settings.KNACK_DONOR_REQUIRED_FIELDS

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
        """
        do string transformations
        """
        try:
            for fkey, fvalue in field_prefixes:
                knack_lineitem[fkey] = fvalue + knack_lineitem[fkey]
        except Exception:
            logger.warning(
                'ActBlue data warning: Error applying prefix {}'.format(fvalue))

        """
        do timezone conversions
        """
        try:
            for fkey in timezone_conversions_needed:
                aware_datetime = parser.parse(knack_lineitem[fkey])
                knack_lineitem[fkey] = aware_datetime.astimezone(
                    timezone('America/Los_Angeles')).replace(tzinfo=None).isoformat()
        except Exception:
            continue

        """
        check for required fields. Figure out ActBlue mapping by looking in sync_data/actblue_mappings/
        """
        for fkey in knack_required_fields:
            if fkey not in knack_lineitem or not knack_lineitem[fkey]:
                logger.warning(
                    'ActBlue data warning: {} not found'.format(knack_required_fields[fkey]))
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
            if int(key) in container:
                return container[int(key)]
        else:
            if path[0] in container:
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
    passes = (username == settings.ACTBLUE_USERNAME and password ==
              settings.ACTBLUE_PASSWORD)
    if not passes:
        logging.warning(
            'Unauthorized access attempted with username {}'.format(username)
        )
    return passes
