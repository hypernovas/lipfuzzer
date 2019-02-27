# LipFuzzer 1.0



1. Where to download coreNLP tool used in NLTK:

https://stanfordnlp.github.io/CoreNLP/ (choose Enlgish)

Unzip it and remember the path

edit the path in NLPEngine.py (for coreNLP)

2. pip install inflect

or python -m pip install inflect

3. pip install pyenchant

5. Download [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) zip file and extract to the **root folder**

6. Directly run with python first.py


Note: 

Register your new module:
add sequence number at LipEngine.py

	self.supportedModule = [0, 1, 2, 3, ..., n]

and _init_.py file of ./modules folder

	__all__ = ["module_zero", "module_one", "module_two", ... ,"yours"]

