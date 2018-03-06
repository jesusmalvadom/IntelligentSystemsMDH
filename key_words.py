import numpy as np
import nltk
from nltk.corpus import wordnet as wn
import sys
import re

nltk.download('wordnet')

bad_words = [' ', " ", "aboard", "about", "above", "according", "across", "addition", "after", "against", "ahead", "along",
"alongside", "amid", "amidst", "among", "amongst", "around", "as", "aside", "astride", "at", "athwart",
"atop", "away", "barring", "because", "before", "behind", "below", "beneath", "beside", "between", "betwixt",
"beyond", "but", "by", "circa", "concerning", "close", "despite", "down", "due", "during", "except", "excluding",
"failing", "far", "for", "from", "in", "front", "spite", "inside", "instead", "into", "like", "minus", "near", "next",
"notwithstanding", "of", "off", "on", "behalf", "top", "out", "onto", "opposite", "out", "outside", "over", "owing", "past",
"per", "persuant", "plus", "prior", "pro", "regarding", "regardless", "round", "save", "since", "thanks", "thank",
"through", "throughout", "till", "to", "toward", "towards", "under", "underneath", "unlike", "until", "up", "upon",
"via", "with", "within", "without", "and", "the", "they", "you", "she", "are", "was", "his", "her", "their", "ours",
"its", "him", "hers", "our", "yours", "theirs", "that", "this", "those", "these", "will", "must", "would", "might", 
"should", "each", "only", "which", "what", "where", "when", "how", "why", "who", "never", "always", "get", "have", "had", "has", 
"cannot", "aren", "isn", "weren", "were", "wasn", "was", "did", "doesn", "does", "can", "get", "gets", "got", "than", "already", "any",
"much", "while", "here", "there", "not", "other", "too", "many", "some", "all", "just", "even", "them"]

delimiters = r'( |\;|\,|\.|\:|\s|\n|\(|\)|\[|\]|\{|\}|\"|\”|\“|\'|\’|\‘|\?|\!|\¿|\||\-)\s*'

# It applies different rules to delete some words
def check_word(word):
	if len(word) > 2:	# If length is less than 2
		if not bool(re.search(r'\d', word)): # If it contains any number
			if word not in bad_words: # If it is on the unimportant words list
				return True
	return False

# This function checks if a word is a synonime of any of the words on the list given
# It returns the synonim if any, and False otherwise
def check_synonims_in_list(word, word_list):
	for synset in wn.synsets(word):
		for lemma in synset.lemma_names():
			if lemma in word_list:
				return lemma
	return False


def key_words(input_file):
	key_vector = {}

	for line in input_file:
		word_l = re.split(delimiters, line)

		for word in word_l:
			word = word.lower()
			if (check_word(word) == True): # It satisfies the rules we have in check_word()
				if word not in key_vector: # It is not already in our list of key words

					aux = check_synonims_in_list(word, key_vector)
					if aux == False:
						key_vector[word] = 1
					else:
						key_vector[aux] += 1
				else:
					key_vector[word] += 1

				
	return key_vector


if len(sys.argv) > 1:
	infile = open(sys.argv[1], 'r')
	d = key_words(infile)
	d = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
	print(d)
else:
	print("Introduce the name of the .txt file as a parameter")



















