import re

# This module supports word's swapping (or replacing). For example, given an utterance, 
# it can substitute the word 'crypto' with 'crypt'. 
# Rule: { rule_id: {'module': module_id, 'action': 'final_word', 'match': 'initial_word', 'name': 'rule_name'}}
# Example: { 1: {'module': 0, 'action': 'crypt', 'match': 'crypto', name: 'sample_rule'}}

def module_zero(self, data, rule): # this is a word swapping function, for example, swap "crypto" with "crypt"
		for current_word in data['to']:
			match_word = rule['match']
			action_word = rule['action']

			if current_word.lower() == match_word:
				insensitive_hippo = re.compile(re.escape(match_word), re.IGNORECASE)
				data['ut'] = insensitive_hippo.sub(re.escape(action_word), data['ut'])

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
