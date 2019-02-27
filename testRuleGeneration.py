# Generating Rules

# Word Exhange Rule
## type 1: check any in Lapsus word knowledge base, if it is generate all possible pairs
from ruleIO import *

r = rulePack()
r.filePath = 'testRule.txt'
r.len = 1
r.rid = 1
r.mid = 1
r.initializing()
r.reading()
print r.readRuleSet
r.det[0] = 'ANY_Confu'
r.act[0] = 'ALL'
r.update(1,1)
