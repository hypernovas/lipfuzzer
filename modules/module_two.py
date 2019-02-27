# This module supports word's removing based on Part of Speech tag. For example, given an utterance, 
# it can remove all determiner (DT). For example, removing DT from 'Hey Google, a Crypto Wallet' results in 
# 'Hey Google, Crypto Wallet' 
# Rule: { rule_id: {'module': module_id, 'action': 'remove', 'match': 'POS', 'name': 'rule_name'}}
# POS (part of speech) = ['CC', 'CD', 'NNP', ...] Based on stanford parser tagset. 
# See https://catalog.ldc.upenn.edu/docs/LDC99T42/tagguid1.pdf for more.
# Example: { 1: {'module': 2, 'action': 'remove', 'match': 'DT', name: 'remove all determiner'}}

def module_two(self, data, rule):
	#PoS = Part of Speech
	pos_map = {}

	for pos in data['de']:
		pos_map[pos[0][0]] = pos[0][1]
		pos_map[pos[2][0]] = pos[2][1]

	pos_match = rule['match']
	# ~ print pos_match

	for word, pos in pos_map.items():
		if pos == pos_match:
			data['ut'] = data['ut'].replace(word, "")
			
	#data['to'] = self.nlp.tokenize(data['ut'])
	#data['de'] = self.nlp.depParse(data['ut'])
	#data['ph'] = {}
	#data['le'] = {}
	#ind = 0
	#for x in data['to']:
	#	data['le'][ind] = self.nlp.lemmatization(x)
	#	data['ph'][ind] = self.nlp.phonimizer(x)
	#	ind += 1

	return data['ut']
