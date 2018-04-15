# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def sync(request):
    if request.method == 'POST':
        actblue_data = json.loads(request.body)
        knack_values = transform(actblue_data)
        print 'would have sent {} to knack'.format(json.dumps(knack_values))
        return HttpResponse('')

def transform(actblue_values):
    knack_values = {}
    for k, v in settings.ACTBLUE_TO_KNACK_MAPPING.iteritems():
        path = k.split('#')
        knack_values[v] = walk(path, actblue_values)
    return knack_values


def walk(path, dict):
    if not dict or isinstance(dict, str):
        return None
    elif len(path) == 1:
        return dict.get(path[0])
    else:
        return walk(path[1:], dict.get(path[0]))
