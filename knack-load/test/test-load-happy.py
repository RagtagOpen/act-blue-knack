import io
import sys
import json

# a bit ugly, but we just need this for the tests
# will make this more general when we fix the tests overall
sys.path.append('..')
import knackload

with open ("test_blue.json", encoding="utf-8") as f:
    vol = json.load(f)

# json.load puts the string in single quotes for reasons that 
# elude understanding since json strings are supposed to be double quoted
# so we dump it out to get them back in double quoites so any json parsers
# will accept them
result = knackload.load( json.dumps(vol) )
print(result)
