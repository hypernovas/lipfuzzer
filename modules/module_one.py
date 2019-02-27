# This module supports word's addition based on word's dependency. For example, given an utterance 
# 'Hey Google, Crypto Wallet', which has NNP compound NNP structure (NNP = singular proper noun), 
# it can add 'my' in front. This results in 'Hey Google, My Crypto Wallet'.
# Rule: { rule_id: {'module': module_id, 'action': ('position', 'word'), 'match': ('{POS', 'Relation', 'POS'), 'name': 'rule_name'}}
# position = ['front', 'back', 'between']
# POS (part of speech) = ['CC', 'CD', 'NNP', ...] Based on stanford parser tagset. 
# See https://catalog.ldc.upenn.edu/docs/LDC99T42/tagguid1.pdf for more.
# Relation = Grammatical Relation (eg., 'compound', 'discourse', etc.)
# See https://nlp.stanford.edu/nlp/javadoc/javanlp-3.5.0/edu/stanford/nlp/trees/EnglishGrammaticalRelations.html for more.
# Example: {1: {'module': 1, 'match': ('NNP', 'compound', 'NNP'), 'action': ('front', 'My'), 'name': 'Add Word based on Relation'}}

def module_one(self, data, rule):
	for pos in data['de']:
		#PoS = Part of Speech
		curr_word1_pos = pos[0][1]
		curr_dep = pos[1]
		curr_word2_pos = pos[2][1]
		curr_word1 = pos[0][0]
		curr_word2 = pos[2][0]
		
		match_rule = rule['match']
		# ~ print match_rule
		match_word1_pos = match_rule[0]
		match_dep = match_rule[1]
		match_word2_pos = match_rule[2]
		location_rule = rule['action']
		action_location = location_rule[0]
		action_word = location_rule[1]

		if curr_word1_pos == match_word1_pos and curr_dep == match_dep and curr_word2_pos == match_word2_pos:
			i1 = data['ut'].find(curr_word1)
			i2 = data['ut'].find(curr_word2)

			len_first = len(curr_word1)
			len_last = len(curr_word2)

			first_index = i1
			last_index = i2
	
			if i1 > i2:
				first_index = i2
				last_index = i1

				len_first = len(curr_word2)
				len_last = len(curr_word1)

			

			if action_location == 'front':
				data['ut'] = data['ut'][:first_index] + action_word + " " + data['ut'][first_index:]
			elif action_location == 'between':
				data['ut'] = data['ut'][:first_index + len_first] + " " + action_word + " " + data['ut'][last_index:]
			elif action_location == 'back':
				data['ut'] = data['ut'][:last_index + len_last] + " " + action_word + data['ut'][last_index + len_last:]
			else:
				print("Invalid rule")
		
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
