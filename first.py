from LipEngine import *

l = lipEngine()
l.loadRule("testRule.txt")
l.loadData("testInput.txt")
l.fuzz(OUTPUTSTEP=True)
