# This module supports lemmatizing based on Part of Speech tag. For example, given an utterance 'Alexa, tell me about studies story' results in 'Alexa, tell me about studies story' 
# Rule: { rule_id: {'module': module_id, 'action': 'replace', 'match': 'POS', 'name': 'rule_name'}}
# POS (part of speech) = ['all', 'CC', 'CD', 'NNP', ...] Based on stanford parser tagset. 
# See https://catalog.ldc.upenn.edu/docs/LDC99T42/tagguid1.pdf for more.
# Example: { 1: {'module': 6, 'action': 'replace', 'match': 'all', name: 'lemmatize all POS tags'}} or you may match only 'NN'

def module_six(self, data, rule):
	#PoS = Part of Speech
	pos_map = {}

	for pos in data['de']:
		pos_map[pos[0][0]] = pos[0][1]
		pos_map[pos[2][0]] = pos[2][1]

	pos_match = rule['match']

	matched = False
	original_ut = data['ut']

	for word, pos in pos_map.items():
		if pos_match != 'all':
			if pos_match == pos:
				data['ut'] = data['ut'].replace(word, self.nlp.lemmatization(word))
				matched = True

		else:
			data['ut'] = data['ut'].replace(word, self.nlp.lemmatization(word))
			matched = True

	if original_ut != data['ut']:
		return data['ut']

