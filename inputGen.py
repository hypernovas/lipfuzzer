from utteranceIO import *

p = UtterancePack()
p.filePath = 'testInput.txt'
p.initilize()
p.utterance = 'Alexa, talk about story'
p.update((0,0,1))
p.utterance = 'Sleeping Sounds Relax, Study or Meditate'
p.update((0,0,2))
p.utterance = 'Necessary Blackness Podcast'
p.update((0,0,3))
p.utterance = 'St. Louis PostDispatch'
p.update((0,0,4))
p.utterance = 'Coinbase Prices Briefing'
p.update((0,0,5))
p.utterance = 'Amazon Pay Deal of the Day'
p.update((0,0,6))
