# This module supports Phoneme mutation with any length. 

def module_four(self, data, rule):
	# find length of phoneme in rules
	phlen = len(rule['match']) - 1
	#print("length is " + str(phlen))
	match_ph = {}
	MATCH = False
	hit = 0
	print data['ph']
	for key, val in data['ph'].iteritems():
		#print("val is " + str(val))
		if val == 'None':
			continue
		if len(val) >= phlen:
			for s in range(len(val) - phlen + 1):
				for y in range(1, phlen+1): 
					if str(val[s+ y-1]).upper() == str(rule['match'][y]).upper():
						MATCH = True
						match_ph[key] = [s+y-1, y]
					else: 
						MATCH == False
						match_ph = {}
				if MATCH == True:
					#print str(match_ph)
					for matchkey, vals in match_ph.iteritems():
						print data['ph'][matchkey]
						for y in range(phlen): 
							data['ph'][matchkey][vals[0]-y] = rule['action'][vals[1]-y]
							#print data['ph'][matchkey]
				return data['ph']
					
						
		
	
