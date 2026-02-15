"""NLP Engine for linguistic processing and analysis."""

from __future__ import annotations

import sys
from pathlib import Path

import enchant
import nltk
from nltk.corpus import wordnet
from nltk.corpus.reader.cmudict import *
from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem.wordnet import WordNetLemmatizer

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lipfuzzer.io.utterance_io import *

# Download required NLTK data
nltk.download("cmudict")
nltk.download("wordnet")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")
nltk.download("treebank")


class NLPEngine:
    """Natural Language Processing engine for voice command analysis.

    Provides tokenization, lemmatization, phoneme conversion, and dependency parsing
    for voice assistant security testing.

    Data structure: self.packedDic[p.uid, p.gid] = {
        'ut': p.utterance,
        'to': p.token,
        'le': p.lemma,
        'po': p.postag,
        'de': p.dependency
    }

    ID ranges:
    - uid (utterance id): 0-999999 reserved for lapsus input, 1000000+ for seed utterances
    - gid (gadget id): 0-99999 reserved for lapsus type, 100000+ for multiple seed utterances
    """

    def __init__(self) -> None:
        """Initialize NLP engine with Stanford CoreNLP parsers."""
        self.path_to_jar = "./stanford-corenlp-full-2018-10-05/stanford-corenlp-3.9.2.jar"
        self.path_to_models_jar = "./stanford-corenlp-full-2018-10-05/stanford-corenlp-3.9.2-models.jar"
        self.d = enchant.Dict("en_US")

    def lemmatization(self, inStr: str) -> str:
        """Convert word to its lemma (base form).

        Args:
            inStr: Input word string

        Returns:
            Lemmatized word in lowercase
        """
        lmtzr = WordNetLemmatizer()
        return lmtzr.lemmatize(inStr.lower())

    def phonimizer(self, inWord: str) -> str | list[str]:
        """Convert word to phoneme representation using CMU dictionary.

        Args:
            inWord: Input word

        Returns:
            Phoneme representation or 'None' if not found
        """
        arpabet = nltk.corpus.cmudict.dict()
        if wordnet.synsets(inWord.lower()) and self.d.check(inWord.lower()):
            try:
                # Return first phoneme representation (multiple may exist)
                return arpabet[inWord.lower()][0]
            except (ValueError, KeyError):
                return "None"
        return "None"

    def depParse(self, inStr: str) -> list[tuple]:
        """Parse dependency tree of input sentence.

        Args:
            inStr: Input sentence string

        Returns:
            List of dependency triples
        """
        dependency_parser = StanfordDependencyParser(
            path_to_jar=self.path_to_jar,
            path_to_models_jar=self.path_to_models_jar,
        )
        result = dependency_parser.raw_parse(inStr)
        dep = next(result)
        return list(dep.triples())

    def tokenize(self, inStr: str) -> list[str]:
        """Tokenize input string into words.

        Args:
            inStr: Input sentence string

        Returns:
            List of tokens
        """
        return nltk.word_tokenize(inStr)

    def posTagging(self, inStr: list[str]) -> list[tuple[str, str]]:
        """Perform Part-of-Speech tagging.

        Args:
            inStr: List of tokens

        Returns:
            List of (word, POS tag) tuples
        """
        return nltk.pos_tag(inStr)

