import json
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--f",help="input the JSON key whose values need to be listed")
parser.add_argument("filepath",help="input the JSON file path")
args = parser.parse_args()
keyoccstats = dict()
valuesofkeys = dict()
with open(args.filepath) as f:
    Jsons = f.readlines()
Count = len(Jsons)
if args.f:
    for index in range(0, len(Jsons) - 1):
        parsed = json.loads(Jsons[index])
        value = parsed[args.f]
        if value in valuesofkeys:
            valuesofkeys[value] += 1
        else:
            valuesofkeys[value] = 1
    print("Total Rows " + str(Count))
    allstats = valuesofkeys.keys()
    for everystat in allstats:
        print(everystat + ", " + str(valuesofkeys[everystat]))
else:
    for index in range(0,len(Jsons)-1):
        parsed = json.loads(Jsons[index])
        for key in parsed:
            if key in keyoccstats:
                keyoccstats[key] +=1
            else:
                keyoccstats[key] =1
    print '{0} {1}'.format("Total Rows",str(Count))
    allkeys = keyoccstats.keys()
    for everykey in allkeys:
        perc = float((int(keyoccstats[everykey])) / 0.65)
        print(everykey+": ["+str(perc)+"%]")

