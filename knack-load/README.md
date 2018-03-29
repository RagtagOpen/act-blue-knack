# act-blue-knack
Python module that access the KNACK database in order to POST a new record to the Sister Disctrict instance.

The load function takes a fully formed json payload representing a donor record.  The module uses the Knack object API.  The module expects the following environment variables:

KNACK_URI: The URI used by the Knack object API, including the Sister Disctrict object key
KNACK_API_KEY: The Sister District Knack API key
KNACK_API_ID: The Sister District Knack Application ID

The module returns the HTTP return code and the error moessage or created object.
