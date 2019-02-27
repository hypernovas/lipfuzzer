from utteranceIO import *

p = UtterancePack()
p.filePath = 'testInput.txt'
p.initilize()
p.utterance = 'Alexa, talk about story store'
p.update((0,0,1))
p.utterance = 'Alexa, open studies guide'
p.update((0,0,2))
p.utterance = 'Alexa, enable postseason ticket'
p.update((0,0,3))
p.utterance = 'Alexa, enable crypto wallets'
p.update((0,0,4))

