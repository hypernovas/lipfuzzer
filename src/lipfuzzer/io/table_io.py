class TablePack(object):
	def __init__(self):
		self.filePath = ''
		self.wordKey = ''
		self.wordValue = ''
		self.lookupTable = {}
		self.readTable = {}
		#self.tmp = {}

	def initializng(self):
		#self.lookupTable[self.wordKey] = [self.wordValue]
		target = open(self.filePath, 'w')
		target.write(str(self.lookupTable))

	def reading(self):
		s = open(self.filePath).read()
		self.readTable = eval(s)

	def update(self, key, value):
		self.reading()
		tmp = {key : [value]}
		if key in self.readTable.keys():
			self.readTable[key] = self.readTable[key] + [value]
		else:
			self.readTable.update(tmp)
		target = open(self.filePath, 'w')
		target.write(str(self.readTable))
		
	def mutualUpdate(self, key, value):
		self.reading()
		tmp = {key : [value]}
		if key in self.readTable.keys():
			self.readTable[key] = self.readTable[key] + [value]
		else:
			self.readTable.update(tmp)
		tmp2 = {value : [key]}
		if value in self.readTable.keys():
			self.readTable[value] = self.readTable[value] + [key]
		else:
			self.readTable.update(tmp2)
		target = open(self.filePath, 'w')
		target.write(str(self.readTable))

	def confuLookup(self, inStr):
		self.filePath = 'testTable.txt'
		self.reading()
		tmp = []
		if inStr in self.readTable.keys(): # lookup for just two inference
			tmp = tmp + self.readTable[inStr]
			if tmp[0] in self.readTable.keys():
				if self.readTable[tmp[0]][0] != inStr:
					return True, tmp + self.readTable[tmp[0]]
				else: 
					return True, tmp
			else:
				return True, tmp
		else: 
#			print 'Confusable Knowledge Base: Word(s) not found! \n'
			return False, None

#t = TablePack()
#t.filePath = 'testTable.txt'
#t.wordKey = 'a' 
#t.wordValue = 'b'
#t.initializng()
#print t.lookupTable['a']
#print t.lookupTable
#t.update('b','a')
#print t.readTable


## test for lookup
# ~ t = TablePack()
# ~ result = t.confuLookup('a lot')
# ~ print result

