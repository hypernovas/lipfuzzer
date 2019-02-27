# The Rule Input/Output has following functionalityies 02/25/2019
## 1) Read rule file and save in the local ruleSet dictionary
## 2) Add a single rule or set of rules to the current ruleSet dictionary
## 3) Get a single rule or set of rules and return
## 4) Update a rule
## 5) Print rule(s) to console
## 6) Generate rule file

# Basic principle of rules:
## Rules are kept in this form {rule_id: {'module': module_id, 'action': expected_action, 'match': pattern, 'name': human_readable_name}}
## 1) rule_id: a unique integer indicating the ID of each rule
## 2) module: a unique integer indicating the ID of the module associated with this rule.
## 3) action: an action specifier when matched pattern is found, specifies how to mutate. It is per slot (either phoneme or word).
## 4) match: a pattern to be searched in the input data. That is also what kind of patterns are vulnerable. 

# module_id example listing
## 1: word exchange, simple swaping
## 2: word adition, add words based on sentence structure and the part of speech tag
## 3: word deletion, delete words based on sentence structure and the part of speech tag
## 4: phoneme exchange, phoneme swaping
## 5: Phoneme blends
## 6: Morpheme exchange 
## 7: shifting, tense shifting.. 



class rulePack(object):
	def __init__(self):
		self.rule_id = 0
		self.readRule_id = 0
		self.ruleSet = {}
		self.readRuleSet = {}

	# Read rule from a file
	def readRule(self, path):
		s = open(path).read()
		self.readRuleSet = eval(s)
		self.readRule_id = max(self.readRuleSet, key=self.readRuleSet.get)
		
	# Getters
	def getRule(self, rule_id):
		if rule_id not in self.ruleSet.keys():
			print "Rule #" + str(rule_id) + " does not exist."
			return {}

		return self.ruleSet[rule_id]

	def getRuleSet(self):
		return self.ruleSet

	## For readRule
	def getReadRule(self, rule_id):
		if rule_id not in self.readRuleSet.keys():
			print "Rule #" + str(rule_id) + " does not exist."
			return {}

		return self.readRuleSet[rule_id]

	def getReadRuleSet(self):
		return self.readRuleSet

	# Setters
	def addRule(self, mod_id, match, action, name=""):
		self.rule_id += 1
		self.ruleSet[self.rule_id] = {'name': name, 'module': mod_id, 'match': match, 'action': action}

	def addRuleSet(self, path):
		fp = open(path).read()
		ruleSet = eval(fp)

		for rule_id in sorted(ruleSet):
			self.rule_id += 1
			self.ruleSet[self.rule_id] = ruleSet[rule_id]

	def updateRule(self, rule_id, mod_id, match, action, name=""):	
		if rule_id not in self.ruleSet.keys():
			print "Rule #" + str(rule_id) + " does not exist."
			return

		self.ruleSet[rule_id] = {'name': name, 'module': mod_id, 'match': match, 'action': action}

	## For readRule
	def addReadRule(self, mod_id, match, action, name=""):
		self.readRuleSet[self.readRule_id] = {'name': name, 'module': mod_id, 'match': match, 'action': action}
		self.readRule_id += 1

	def updateReadRule(self, rule_id, mod_id, match, action, name=""):	
		if rule_id not in self.readRuleSet.keys():
			print "Rule #" + str(rule_id) + " does not exist."
			return

		self.readRuleSet[rule_id] = {'name': name, 'module': mod_id, 'match': match, 'action': action}

	# Print
	def printRule(self, rule_id):
		if rule_id not in self.ruleSet.keys():
			print "Rule #" + str(rule_id) + " does not exist."
			return

		print "Rule #" + str(rule_id) + " = " + str(self.ruleSet[rule_id])

	def printRuleSet(self):
		for rule_id in sorted(self.ruleSet):
			if self.ruleSet[rule_id]['name'] != "":
				print "Rule #" + str(rule_id) + " [" + self.ruleSet[rule_id]['name'] + "]:"
			else:
				print "Rule #" + str(rule_id) + ":"

			print "\tModule: " + str(self.ruleSet[rule_id]['module'])
			print "\tmatch: " + str(self.ruleSet[rule_id]['match'])
			print "\taction: " + str(self.ruleSet[rule_id]['action'])

	## For readRule
	def printReadRule(self, rule_id):
		if rule_id not in self.readRuleSet.keys():
			print "Rule #" + str(rule_id) + " does not exist."
			return

		print "Rule #" + str(rule_id) + " = " + str(self.readRuleSet[rule_id])

	def printReadRuleSet(self):
		for rule_id in sorted(self.readRuleSet):
			if self.readRuleSet[rule_id]['name'] != "":
				print "Rule #" + str(rule_id) + " [" + self.readRuleSet[rule_id]['name'] + "]:"
			else:
				print "Rule #" + str(rule_id) + ":"

			print "\tModule: " + str(self.readRuleSet[rule_id]['module'])
			print "\tmatch: " + str(self.readRuleSet[rule_id]['match'])
			print "\taction: " + str(self.readRuleSet[rule_id]['action'])
	
	#Generate rule file
	def genRuleFile(self, path):
		fp = open(path, 'w')
		fp.write(str(self.ruleSet))
		

# Example Usage
# ~ r = rulePack()
# ~ r.addRule(2, 'NNP', 'remove', 'mod2')
# ~ r.addRule(1, ('front', 'a'), ('NNP', 'compound', 'NNP'), 'mod1')

# ~ r.printRuleSet()
# ~ r.printRule(2)

# ~ r.updateRule(1, 2, 'NNPS', 'remove', 'mod2')
# ~ r.addRuleSet('testRuleIO.txt')

# ~ r.genRuleFile('ruleFile.txt')
