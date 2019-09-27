# Read, Write Utterance data structure
class UtterancePack(object):
	def __init__(self):
		self.utterance = ""
		self.uid = 0
		self.gid = 0
		self.dependency = {''}
		self.packedDic = {}
		self.readUtteranceSet = {}
		self.filePath = ""
		self.postag= {''}
		self.token = {''}
		self.lemma = {''}
		self.phoneme = []
		self.cato = ''
		self.keyNeeded = {}		

	def initilize(self):
		target = open(self.filePath, 'w')
		target.write(str(self.packedDic))

	def reading(self):
		s = open(self.filePath).read()
		self.readUtteranceSet = eval(s)

	def findWithUid(self, inuid, dic):
		self.keyNeeded = [(uid, gid, utype) for uid, gid, utype in dic.keys() if uid == inuid]

	def findWithGid(self, ingid, dic):
		self.keyNeeded = [(uid, gid, utype) for uid, gid, utype in dic.keys() if gid == ingid]
	
	def findWithUtype(self, inUtype, dic):
		self.keyNeeded = [(uid, gid, utype) for uid, gid, utype in dic.keys() if utype == inUtype]

	def update(self, key):
		self.reading()
		tmp = {key : {'ut': self.utterance, 'to': self.token, 'le': self.lemma, 'po': self.postag, 'de': self.dependency, 'ca': self.cato, 'ph': self.phoneme}}# utterance (voice commands, tokens, lemma of words, tags, dependency, category of the voice command, and phoneme)
		if key in self.readUtteranceSet.keys():
			print('[error-utterance]: key conflict.')
			exit()
		else:
			self.readUtteranceSet.update(tmp)
		target = open(self.filePath, 'w')
		target.write(str(self.readUtteranceSet))
		
	def write(self, inSet, inPath):
		target = open(inPath, 'w')
		target.write(str(inSet))

#p = UtterancePack()
#p.filePath = 'testUtterance.txt'
#p.initilize()
#p.utterance = 'testy'
#p.update((1,1,1))
#print p.readUtteranceSet
#p.findWithUid(1, p.readUtteranceSet)
#print p.keyNeeded
