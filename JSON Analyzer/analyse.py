import json
import sys
import argparse

_keyoccurencestats = dict()
_valuesofkeys = dict()
parser = argparse.ArgumentParser()
parser.add_argument("--f",help="input the JSON key whose values need to be listed")
parser.add_argument("filepath",help="input the JSON file path")
args = parser.parse_args()

def main():
    "The main function of the program"
with open(args.filepath) as f:
    Jsons = f.readlines()
Count = len(Jsons)
if args.f:
    for index in range(0, len(Jsons) - 1):
        parsed = json.loads(Jsons[index])
        value = parsed[args.f]
        if value in _valuesofkeys:
            _valuesofkeys[value] += 1
        else:
            _valuesofkeys[value] = 1
    print '{0} {1}'.format("Total Rows ",str(Count))
    allstats = _valuesofkeys.keys()
    for everystat in allstats:
        print '{0} {1} {2}'.format(everystat,", ", str(_valuesofkeys[everystat]))
else:
    for index in range(0,len(Jsons)-1):
        parsed = json.loads(Jsons[index])
        for key in parsed:
            if key in _keyoccurencestats:
                _keyoccurencestats[key] +=1
            else:
                _keyoccurencestats[key] =1
    print '{0} {1}'.format("Total Rows",str(Count))
    allkeys = _keyoccurencestats.keys()
    for everykey in allkeys:
        perc = float((int(_keyoccurencestats[everykey])) / 0.65)
        print '{0} {1} {2} {3}'.format(everykey,": [",str(perc),"%]")

if __name__ == "__main__": main()
