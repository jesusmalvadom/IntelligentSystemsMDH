import numpy as np
from nltk.corpus import wordnet as wn
import nltk
import math
import sys
import re
import os 

print("Configurating wordnet libraries...")
nltk.download('wordnet')
print("DONE")

# List of words that are not interesting for comparision such as prepositions or determinants
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
"much", "while", "here", "there", "not", "other", "too", "many", "some", "all", "just", "even", "them", "then", "self", "such", "none"]

# List of the delimeters used to analyzed the text
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

# This function creates a dictionary of all the key words in the input_file with their frequency
# It returns the dictionary alphabetically sorted
def key_words(input_file):
	key_vector = {}
	key_vector_sorted = {}

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

	
	for key in sorted(key_vector.keys()):
		key_vector_sorted[key] = key_vector[key]
	
	return key_vector_sorted

# This function sort a dictionary alphabetically
def sort_dict(d):
	sorted_d = {}
	for key in sorted(d.keys()):
		sorted_d[key] = d[key]
	return sorted_d

# It fills the dictionary with 0 in case it doesn't contain one of the key_words
def fill_dict(d, key_words_list):

	for key_word in key_words_list:
		if key_word not in d.keys():
			d[key_word] = 0

	d = sort_dict(d)
	return d

# It fills all the dictionaries in the matrix depending on the list of keywords
def fill_matrix(matrix, key_words_list):
	aux_matrix = []
	for d in matrix:
		d = fill_dict(d, key_words_list)
		aux_matrix.append(d)
	return aux_matrix 

# Similarity based on euclidean formula
def EuclideanDistance(list1, list2):
	suma=0.0

	for key in list1.keys():

		suma += (list1[key]-list2[key]) ** 2

	suma **= 0.5
	return suma

# Similarity based on cosine formula
def CosineSimilarity(list1, list2):
	suma=0.0
	mod_a=0.0
	mod_b=0.0

	for key in list1.keys():
		suma += (list1[key]*list2[key])

	mod_a = np.sum(np.power(list(list1.values()), 2))
	mod_a = np.power(mod_a, 0.5)

	mod_b = np.sum(np.power(list(list2.values()), 2))
	mod_b = np.power(mod_b, 0.5)

	return suma/(mod_a*mod_b)

# Similarity based on TSS_SS formula
def TSSS(list1, list2):
	mod_a = 0.0
	mod_b = 0.0

	mod_a = np.sum(np.power(list(list1.values()), 2))
	mod_b = np.sum(np.power(list(list2.values()), 2))

	MD = abs(mod_a-mod_b)

	V = CosineSimilarity(list1,list2)
	ED = EuclideanDistance(list1,list2)

	theta = math.degrees(math.acos(V)) + 10

	#We can also implement SS and compare too
	TSSS = (mod_a * mod_b *	math.sin(theta) * theta * math.pi *	((ED+MD)**2)) / 720
	return TSSS


###############################################################################################
################################### Main part of the script ###################################    
###############################################################################################

# We load the DB of texts we already have to compare with
cases_DB = os.listdir("20-newsgroups/")
key_words_matrix = []
key_words_list = []
extra_keys = []
n_dict = 0

# for each case, we create its own dictionary
for case_title in cases_DB:
	print(case_title)
	case_file = open('20-newsgroups/' + case_title, 'r', errors='ignore')
	d = key_words(case_file)

	# If it's the first dictionary we are exploring, we just append it,
	# otherwise, we have to check for synonims with the previous ones
	if n_dict != 0:
		for key in list(d):
			syn = check_synonims_in_list(key, key_words_list)
			if syn != False:
				d[syn] = d.pop(key)

	for word in d.keys():
		if word not in key_words_list:
			key_words_list.append(word)

	key_words_matrix.append(sort_dict(d))
	n_dict += 1


# Here we have the matrix with all the dictionaries containing key words and their frequency
# All the dictionaries have the same length because they are filled with 0 in those spaces where
# the words didn't appear
key_words_list = sorted(key_words_list)
key_words_matrix = fill_matrix(key_words_matrix, key_words_list)



while(1):
	# Now the program will ask the user to enter the name of the file he/she wants to compare with
	input_file_name = input('Introduce the name of the file to analyse: ')

	try:
		f = open(input_file_name)
	except IOError:
		print('\nError opening the file\n\tIntroduce the name again\n\n')
	else:
		with f:

			f = open(input_file_name)
			d_in = key_words(f)

			# First, we check if there are any synonims in the text and replace them
			# We also check if there are any new words to add to the rest of dictionaries
			for key in list(d_in.keys()):
				# print("KEY: %s" % key)
				syn = check_synonims_in_list(key, key_words_list)
				# print("SYN: "),
				# print(syn)
				if syn != False:
					d_in[syn] = d_in.pop(key)
				else:
					if key not in key_words_list:
						extra_keys.append(key)
						key_words_list.append(key)


			# Second, we fill the dictionary with 0 on those places needed to have the same length
			d_in = fill_dict(d_in, key_words_list)
			d_in = sort_dict(d_in)

			# We also add the new words to the previous dictionaries from the database
			for new_word in extra_keys:
				for vector in key_words_matrix:
					vector[new_word] = 0
					vector = sort_dict(vector)


			euclidean_sim = []
			cosine_sim = []
			tss_sim = []

			# Third, we calculate the similarity with the cases in the Database
			for vector in key_words_matrix:
				euclidean_sim.append(EuclideanDistance(d_in, vector))
				cosine_sim.append(CosineSimilarity(d_in, vector))
				tss_sim.append(TSSS(d_in, vector))


			# Lastly, we display the results for each method:
			# Euclidean Distance
			print("\nEuclidean Distance Method: ")
			for i in range(len(cases_DB)):
				print("{} - {}".format(i+1, cases_DB[euclidean_sim.index(min(euclidean_sim))])),
				euclidean_sim[euclidean_sim.index(min(euclidean_sim))] = float('Inf')


			# Cosine Similarity
			print("\n\nCosine Distance Method: ")
			for i in range(len(cases_DB)):
				print("{} - {}".format(i+1, cases_DB[cosine_sim.index(max(cosine_sim))])),
				cosine_sim[cosine_sim.index(max(cosine_sim))] = float('-Inf')


			# TSS_S Method
			print("\n\nTSS Method: ")
			for i in range(len(cases_DB)):
				print("{} - {}".format(i+1, cases_DB[tss_sim.index(max(tss_sim))])),
				tss_sim[tss_sim.index(max(tss_sim))] = float('-Inf')


			print("\n\n")


















