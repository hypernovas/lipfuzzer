import boto3
from utteranceIO import *
import os
import glob
import random
import re
    


print fullTable
playlap = {}
firstPickFullLap = {}
lapCounting = 0
for key, val in setRead.iteritems():
	for k1, k2 in fullTable.iteritems():
		insensitive_hippo = re.compile(re.escape('Alexa '), re.IGNORECASE)
		val = insensitive_hippo.sub('Alexa, ', val)
		if re.search(k1, val, re.IGNORECASE):
			insensitive_hippo = re.compile(re.escape(k1), re.IGNORECASE)
			tempStr = insensitive_hippo.sub(k2, val)
			firstPickFullLap[key + (lapCounting,)] = tempStr
			# ~ print val
			# ~ print tempStr
			lapCounting += 1
	lapCounting = 0

print len(firstPickFullLap)

	
uu = UtterancePack()
newFile = 'result.txt'
uu.write(firstPickFullLap, newFile)

#print newSet


