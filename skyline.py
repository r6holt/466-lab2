from importer import Importer
import sys
import pandas as pd

'''data is the market baskets, items is the items, minSup is the threshold for support'''

MIN_SUPPORT = .1
MIN_CONF = .6
goods = [0]*50
max_rows = 0
candidates = [{}, {}]
frequent = [{}, {}]
counts = []

def main():
	#  inf = open(sys.argv[1], 'r')
	#  print(sys.argv[1])
	im = Importer()
	example1 = im.import_sparse("data/example/out1.csv")
	apriori(example1, goods, MIN_SUPPORT)

def apriori(data, goods, minSup):
	#support_1(data)
	global max_rows
	global frequent
	global candidates
	max_rows = 0
	#fillCandidates()
	data2 = []
	for i in range((data.shape[0])):
		data2 = data2 + [frozenset(list(data.iloc[i, :]))]

	#print(data2)
	#data2 = set(data2)

	for i, row in data.iterrows(): 
		getCount(row)
		max_rows += 1



	for cand in candidates[1]:
		#print(i, goods[i], max_rows)
		val = candidates[1][cand]
		print(val, max_rows, val/max_rows)
		if float(val)/float(max_rows) >= MIN_SUPPORT:
			frequent[1][cand] = val
		#candidates[1][frozenset([i])] = goods[i]
	


	#def support2(data, X, Y):
	#F[0] = support(T, I, minSup)
	k = 2
	while(1):
		#candidate[k] = candidateGen(frequent[k], k)
		print(candidates, "\n\n\n")
		print(frequent, "\n\n\n")

		candidateGen(k)
		frequent = frequent + [{}]
		for cand in candidates[k]:
			#for i, row in data.iterrows():
			for row in data2:

				#row = row.apply(frozenset, axis=1) 
				print(row, cand, "\n")
				if cand.issubset(row):
					print("found a subset")
					candidates[k][cand] += 1

		for cand in candidates[k]:
			count = float(candidates[k][cand])
			#print("\n\ncand: ", cand, "\nsupport: ", (count/float(max_rows)))
			if count / float(max_rows) > MIN_SUPPORT:
				print(count/float(max_rows))
				frequent[k][cand] = count
				
		if len(frequent[k])==0 :
			break

		k+=1

#        for t in T:
#             for c in C[k]:
#                 if(c in t):
#                     count[c] += 1

#         F[k] = those in C[k] if support > min support
#         k = k+1
	 
def getCount(row):
	i = 1
	while i < len(row):
		
		if not pd.isna(row[i]):

			temp = int(row[i])
			key = frozenset([temp])
			if key in candidates[1]:
				candidates[1][key] += 1
			else:
				candidates[1][key] = 1
		i += 1

def candidateGen(n):
	print(n)
	temp = frequent[n-1]
	candidates.append({})
	for i in temp:
		for j in temp:
#			newset = frozenset([i,j])
			newset = i | j

			#print(i, j, newset)
			if (len(newset) == n) and (newset not in candidates[n]):
				candidates[n][newset] = 0  #candidates[n][{ + [[temp[i], temp[j]]]
					 

class mySets:
	def __init__(self, subset, count):
		self.subset = subset
		self.count = count


if __name__ == "__main__":
	 main()
