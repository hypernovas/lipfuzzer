# Fuzzing Engine
from __future__ import print_function
import inflect, sys
from ruleIO import *
from utteranceIO import *
from NLPEngine import *

sys.path.append('./modules/')
from modules import *


class lipEngine(object):
	def __init__(self, outPath="out.txt"):
		self.readRuleSet = {}
		self.outPath = outPath
		self.supportedModule = [0, 1, 2, 3, 4, 5, 6, 7]
		
	def loadRule(self, path):
		print("\n[lipEngine] Loading rules")

		r = rulePack()
		r.readRule(path)
		self.readRuleSet = r.getReadRuleSet()

		for rule in self.readRuleSet.values():
			if rule['module'] not in self.supportedModule:
				print("Module " + str(rule['module']) + " not suppported")
				continue
	
	def loadData(self, path):
		print("[lipEngine] Loading data\n")

		self.uu = UtterancePack()
		self.uu.filePath = path
		self.uu.reading()
		self.nlp = NLPEngine()
		for key, value in self.uu.readUtteranceSet.items():
			print('===============>> ' + str(value['ut']))
			value['to'] = self.nlp.tokenize(value['ut'])
			value['de'] = self.nlp.depParse(value['ut'])
			value['ph'] = {}
			value['le'] = {}
			ind = 0
			for x in value['to']:
				value['le'][ind] = self.nlp.lemmatization(x)
				value['ph'][ind] = self.nlp.phonimizer(x)
				ind += 1
			print(str(value))

	def fuzz(self, rules=[], INHERITCHANGE=False, OUTPUTSTEP=False):
		print("\n[lipEngine] Fuzzing...\n")

		if len(rules) == 0:
			rules = sorted(self.readRuleSet.keys())

		for key, value in self.uu.readUtteranceSet.items():
			data = value.copy()
			applied_rule = []

			print("Input: ")
			print(str(data))

			for rule_id in rules:
				if not INHERITCHANGE:
					data = value.copy()
					applied_rule = ["r" + str(rule_id) + "m" + str(self.readRuleSet[rule_id]['module'])]
				else:
					applied_rule.append("r" + str(rule_id) + "m" + str(self.readRuleSet[rule_id]['module']))
					
				#~ print(".....+++++")
				#~ print self.readRuleSet[rule_id]['module']
				#~ print self.readRuleSet[rule_id]
				out = self.execModule(self.readRuleSet[rule_id]['module'], data, self.readRuleSet[rule_id])

				if OUTPUTSTEP:
					print("\nRules applied: " + str(applied_rule))
					
					if out is not None and str(out).strip() is not None:
						print("[Result]: " + str(out))
					#~ else:
						#~ print "Result: " + str(data) + "\n"

			if not OUTPUTSTEP:
				print("Final Output: ")
				print(str(data))

			print("==============\n")
				
	def execModule(self, mod_id, data, rule):
		out = ""
		p = inflect.engine()
		mod_name = "module_" + str(p.number_to_words(mod_id))
		print(mod_name)
		exec("out = " + mod_name + "." + mod_name + "(self, data, rule)")
		return out

# ~ l = lipEngine()
# ~ l.loadRule("ruleFile.txt")
# ~ l.loadData("datashort.txt")
# ~l.fuzz(OUTPUTSTEP=True)
