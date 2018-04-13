import io
import sys
import json
import argparse
# a bit ugly, but we just need this for the tests
# will make this more general when we fix the tests overall
sys.path.append('..')
import knackload

#let us get your file ...
inputfile = None

#and this is probably all overkill, but, eh, if it actually gets to be a real
# test program, it doesn;t hurt to have the infrastructure in place.  Plus, really,
# I just cut and paste it out of every python program I ever write and do some quick mods ..
parser = argparse.ArgumentParser(description="Knack Load tests")

parser.add_argument("-i", "--input", required=True,
                    help="File containing json payload")

args = parser.parse_args()
inputfile  = args.input

with open (inputfile, encoding="utf-8") as f:
    vol = json.load(f)

# json.load puts the string in single quotes for reasons that
# elude understanding since json strings are supposed to be double quoted
# so we dump it out to get them back in double quotes so any json parsers
# will accept them
(return_status, result_string) = knackload.load( json.dumps(vol) )
result_data = json.loads(result_string)
print(json.dumps(result_data, indent=4))
