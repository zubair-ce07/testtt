import json

courses = []

for num in range(0, 8):
    file = open('jsons/' + str(num) + '.json', 'r')
    s_file = open('surveys/' + str(num) + '.json', 'r')
    course = json.loads(file.read())[0]
    surveys = json.loads(s_file.read())
    course['surveys'] = surveys
    courses += [course]

file = open('final.json', 'w')
file.write(json.dumps(courses))
