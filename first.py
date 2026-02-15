from lipfuzzer import lipEngine

l = lipEngine()
l.loadRule("data/testRule.txt")
l.loadData("data/testInput.txt")
l.fuzz(OUTPUTSTEP=True)
