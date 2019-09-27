import nltk
from utteranceIO import *
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.parse.stanford import StanfordDependencyParser
from nltk.corpus.reader.cmudict import *
from nltk.corpus import wordnet
import enchant
from nltk.corpus import treebank
nltk.download('cmudict')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('treebank')

# data structure: self.packedDic[p.uid, p.gid] = {'ut': p.utterance, 'to': p.token, 'le': p.lemma, 'po': p.postag, 'de': p.dependency}
# uid: utterance id, 0 - 999999 reserved for lapsus input.
## Seed utterance start from 1,000,000
# gid: gedget id, 0 - 99999 reserved for lapsus type
## multiple seed utterances can belong to a gedget, starting from 100,000

class NLPEngine(object):
	def __init__(self):
		#self.fileInput = 'testInput.txt'
		self.path_to_jar = './stanford-corenlp-full-2018-10-05/stanford-corenlp-3.9.2.jar'
		self.path_to_models_jar = './stanford-corenlp-full-2018-10-05/stanford-corenlp-3.9.2-models.jar'
		self.d = enchant.Dict("en_US")
	#lemmatization
	def lemmatization(self, inStr):
		lmtzr = WordNetLemmatizer()
		return lmtzr.lemmatize(inStr.lower())

	#phonimization
	def phonimizer(self, inWord):
		arpabet = nltk.corpus.cmudict.dict()
		if wordnet.synsets(inWord.lower()) and self.d.check(inWord.lower()):
			# ~ print('Phonimizer is processing: ' + inWord)
			try:
				return arpabet[inWord.lower()][0] # there could be multiple outputs, now choose the first
			except ValueError:
				return 'None'
		return 'None'

	#dependency parsing
	def depParse(self, inStr):
		dependency_parser = StanfordDependencyParser(path_to_jar=self.path_to_jar, path_to_models_jar=self.path_to_models_jar)
		result = dependency_parser.raw_parse(inStr)
		dep = next(result)
		return list(dep.triples())
	#tokenization
	def tokenize(self, inStr):
		tokens = nltk.word_tokenize(inStr)
		return tokens

	# PoS Tagging
	def posTagging(self, inStr):
		return nltk.pos_tag(inStr)

