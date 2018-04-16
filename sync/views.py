# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import base64
import json

@csrf_exempt
def sync(request):
    authorized = auth(request)
    if request.method == 'POST' and authorized:
        actblue_data = json.loads(request.body)
        knack_values = transform(actblue_data)
        print "would have sent {} to knack".format(json.dumps(knack_values))
        return HttpResponse('')
    else:
        return HttpResponseForbidden()

def transform(actblue_values):
    knack_values = {}
    for k, v in settings.ACTBLUE_TO_KNACK_MAPPING.iteritems():
        path = k.split('#')
        knack_values[v] = walk(path, actblue_values)
    return knack_values


def walk(path, container):
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
    encoded = str(auth_header.split(' ')[1]) # requires a str not unicode ¯\_(ツ)_/¯
    username, password = base64.urlsafe_b64decode(encoded).split(':')
    # TODO add encryption
    return  username == settings.ACTBLUE_USERNAME and password == settings.ACTBLUE_PASSWORD
