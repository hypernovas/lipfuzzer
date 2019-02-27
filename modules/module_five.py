import enchant

# This module supports prefix removal. For example, given an utterance 
# 'Alexa, tell me about postelection result', which has 'post' as a prefix, 
# it can remove the prefix. This results in 'Alexa, tell me about election result'.
# Rule: { rule_id: {'module': module_id, 'action': 'remove', 'match': 'target_prefix', 'name': 'rule_name'}}
# target_prefix = ['post', 'mis', 'over', etc...]
# Example: {1: {'module': 5, 'match': 'post', 'action': 'remove', 'name': 'Remove post prefix'}}

def module_five(self, data, rule):
	match = rule['match']
	action = rule['action']

	en_dict = enchant.Dict("en_US")
	
	for word in data['to']:
		replaced = word
		matched = word
		removed = False

		if word.find(match+"-") == 0:
			matched = match+"-"
			replaced = word.replace(match+"-", "")
			removed = True
				
		elif word.find(match) == 0:
			replaced = word.replace(match, "")
			removed = True

		if removed:
			if en_dict.check(replaced):
				data['ut'] = data['ut'].replace(word, replaced)
				return data['ut']

	
		
