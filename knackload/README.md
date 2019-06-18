# act-blue-knack

Python module that accesses the Knack database in order to POST a new record to the Sister District instance.

The load function takes a fully formed JSON payload representing a donor record. The module uses the Knack object API. The module expects the following environment variables:

KNACK_API_KEY: The Sister District Knack API key
KNACK_API_ID: The Sister District Knack Application ID

The module returns the HTTP staus code and the error message or created object.

Testing: run `pytest`! (`pip install -U pytest` if you do not have it.)
