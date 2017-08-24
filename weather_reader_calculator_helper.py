def find_max(data, key):
	m = data[0]
	j=0
	for i in data:
		if m[key] is None or m[key] == '':
			m = data[j]

		if data[j][key] != None and data[j][key] != '':
			if int(data[j][key]) > int(m[key]):
				m = data[j]
		j += 1

	return m

def find_min(data, key):
	m = data[0]
	j=0
	for i in data:
		if m[key] is None or m[key] == '':
			m = data[j]

		if data[j][key] != None and data[j][key] != '':
			if int(data[j][key]) < int(m[key]):
				m = data[j]
		j += 1

	return m

def calculate_avg(data, key):
	i = 0
	j = len(data)-1
	sum = 0
	#print(data)
	#return
	while(i<j):
		
		if data[i][key] is None or data[i][key] == '':
			i+=1
			continue
		elif data[j][key] is None or data[j][key] == '':
			j -= 1
			continue
		
		sum += int(data[i][key]) + int(data[j][key])
		i += 1 
		j -= 1

	return {"average": sum/len(data)}