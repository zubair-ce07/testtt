import json
import sys
if (len(sys.argv)>2):
    keyvalue = sys.argv[2]
    filename = sys.argv[3]
else:
    filename = sys.argv[1]
JsonData = open(filename)
keyoccstats = dict()
valuesofkeys = dict()

JsonString = JsonData.read()
Jsons = JsonString.split('\n')
Count = len(Jsons)
if (len(sys.argv)>2):
    for index in range(0, len(Jsons) - 1):
        parsed = json.loads(Jsons[index])
        value = parsed[keyvalue]
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
        array = parsed.keys()
        for key in parsed:
            if key in keyoccstats:
                keyoccstats[key] +=1
            else:
                keyoccstats[key] =1
    print("Total Rows "+str(Count))
    allkeys = keyoccstats.keys()
    for everykey in allkeys:
        perc = float((int(keyoccstats[everykey])) / 0.66)
        print(everykey+": ["+str(perc)+"%]")

