# for DT Addition
#

def module_three(self, data, rule):
	#PoS = Part of Speech
	pos_map = {}

	for pos in data['de']:
		pos_map[pos[0][0]] = pos[0][1]
		pos_map[pos[2][0]] = pos[2][1]

	pos_match = rule['match']
	# ~ print pos_match
	for word, pos in pos_map.items():
		if pos == pos_match:
			inserted = "a " + word
			data['ut'] = data['ut'].replace(word, inserted)

	return data['ut']
