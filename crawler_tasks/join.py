import json
courses = []

for num in range(0, 8):
    file = open('jsons/' + str(num) + '.json', 'r')
    courses+= json.loads(file.read())

file = open('final.json', 'w')
file.write(json.dumps(courses))