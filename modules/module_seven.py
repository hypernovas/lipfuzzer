import enchant

# This module supports prefix addition. For example, given an utterance 
# 'Alexa, tell me about election score', it results in 'Alexa, tell me about postelection score'.
# Rule: { rule_id: {'module': module_id, 'action': 'post', 'match': 'POS', 'name': 'rule_name'}}
# POS (part of speech) = ['all', 'CC', 'CD', 'NNP', ...] Based on stanford parser tagset. 
# See https://catalog.ldc.upenn.edu/docs/LDC99T42/tagguid1.pdf for more.
# Example: {1: {'module': 7, 'match': 'all', 'action': 'post', 'name': 'Add post prefix'}}

def module_seven(self, data, rule):
	match = rule['match']
	action = rule['action']

	en_dict = enchant.Dict("en_US")

	#PoS = Part of Speech
	pos_map = {}

	for pos in data['de']:
		pos_map[pos[0][0]] = pos[0][1]
		pos_map[pos[2][0]] = pos[2][1]

	pos_match = rule['match']
	# ~ print pos_match

	for word, pos in pos_map.items():
		if match != 'all':
			if pos == match:
				if en_dict.check(action+word):
					data['ut'] = data['ut'].replace(word, action+word)

		else:
			if en_dict.check(action+word):
				data['ut'] = data['ut'].replace(word, action+word)

	return data['ut']

		
