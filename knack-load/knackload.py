import requests
import os
import io
import json

# all our little secrets ...
__APIKEY__ = None
__APIID__ = None

# where the knack data lives
__APIURI__ = None

#the headers, since they never change from request to request, since we are only
# doing POSTS here
__HEADERS__ = None

# set the credentials
def setCreds():
    # XXX TODO: verfiy this works on whatever app platform this is going to run on
    global __APIKEY__
    if __APIKEY__ is None:
        __APIKEY__ = os.environ['KNACK_API_KEY']

    global __APIID__
    if __APIID__ is None:
        __APIID__ = os.environ['KNACK_API_ID']

    global __APIURI__
    if __APIURI__ is None:
        __APIURI__ = os.environ['KNACK_URI']

    #set up the headers
    global __HEADERS__
    if __HEADERS__ is None:
        __HEADERS__ = {
            'Content-Type': "application/json",
            'X-Knack-Application-Id': "{0}".format(__APIID__),
            'X-Knack-REST-API-KEY': "{0}".format(__APIKEY__),
            }

# Load the json string into the Knack database
# payload should be json, if it is not, it should be rejected
# response is simplified version of the requests repsonse: code and error text or
# response object
def load( payload):
    # knack has a txn limit, so lets catch obvious errors before we waste a txn
    try:
        json_object = json.loads(payload)
    except ValueError:
        return "500", "Payload invalid json"

    response = requests.request("POST", __APIURI__, data=payload, headers=__HEADERS__)

    return(response.status_code, response.text)

setCreds()
