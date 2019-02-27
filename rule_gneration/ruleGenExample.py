from ruleIO import *

r = rulePack()
# firt match then action
r.addRule(0, 'crypto', 'crypt',  'mod0')
r.addRule(1, ('NN', 'compound', 'NN'), ('front', 'a'),  'mod1')
r.addRule(2, 'NNP', 'remove', 'mod2') 
#~ r.addRule(3, 'NN', ('add', 'a'),  'mod3')
r.addRule(4, ('end','AO1', 'R'), ('swap', 'AW1', 'L'),  'mod4')
r.addRule(5, 'post', 'remove',  'mod5')
r.addRule(6, 'replace', 'all',  'mod6')
#~ r.addRule(7, 'all', 'un',  'mod7')

r.genRuleFile('testRule.txt')
