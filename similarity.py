import numpy as np
import math

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


list1={'apple':2, 'orange':6, 'papaya':10}
list2={'apple':1, 'orange':2, 'papaya':5}

euclidean = EuclideanDistance(list1,list2)
cosine = CosineSimilarity(list1,list2)
ts_ss = TSSS(list1,list2)

print("Euclidian: ", euclidean)
print("Coseno: ", cosine)
print("TS-SS: ", ts_ss)

