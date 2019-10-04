from importer import Importer
import sys
import pandas as pd
import warnings

#warnings.filterwarnings("ignore")

MIN_SUPPORT = .01
MIN_CONF = .6
#max_rows = 0
#candidates = [{}, {}]
#frequent = [{}, {}]

def main():
	#	inf = open(sys.argv[1], 'r')
	#	print(sys.argv[1])

	im = Importer()
	minSup = MIN_SUPPORT
	minConf = MIN_CONF

	if len(sys.argv)==4:
		data_path = sys.argv[2]
		label_path = sys.argv[3]


		if sys.argv[1] == "bakery":
			data = im.import_sparse(data_path)
			raw_labels = im.import_csv(label_path)
			labels = parse_good_labels(raw_labels)

		elif sys.argv[1] == "bingo":
			data = im.import_sparse(data_path)
			raw_labels = im.import_psv(label_path)
			labels = parse_author_labels(raw_labels)

		else:
			pass

	else:
		print("Using Default: \n\n")
		data = im.import_sparse("data/example/out1.csv")

		raw_labels = im.import_csv("data/apriori/goods.csv")
		labels = parse_good_labels(raw_labels)

	frequent = apriori(data, minSup)
	rules = genRules(data, minConf, frequent)
	#parse_output(rules, labels)
	parse_output(rules, labels)

	#all_rules = confidence(example1)
	#skylines = weed_out(all_rules)
	#parse_output(skylines)

# ----------------------------------------------------
# CALCULATE SUPPORT
# ----------------------------------------------------

def apriori(data, minSup):
	#support_1(data)
	max_rows = 0
	candidates = [{}, {}]
	frequent = [{}, {}]
	#fillCandidates()
	data2 = []
	for i in range((data.shape[0])):
		data2 = data2 + [frozenset(list(data.iloc[i, :]))]

	#print(data2)
	#data2 = set(data2)

	for i, row in data.iterrows(): 
		candidates = getCount(row, candidates)
		max_rows += 1



	for cand in candidates[1]:
		#print(i, goods[i], max_rows)
		val = candidates[1][cand]
		# print(val, max_rows, val/max_rows)
		if float(val)/float(max_rows) >= MIN_SUPPORT:
			frequent[1][cand] = val
		#candidates[1][frozenset([i])] = goods[i]
	


	#def support2(data, X, Y):
	#F[0] = support(T, I, minSup)
	k = 2
	while(1):
		#candidate[k] = candidateGen(frequent[k], k)
		# print(candidates, "\n\n\n")
		# print(frequent, "\n\n\n")

		candidates = candidateGen(k, candidates, frequent)
		frequent = frequent + [{}]
		for cand in candidates[k]:
			#for i, row in data.iterrows():
			for row in data2:

				#row = row.apply(frozenset, axis=1) 
				# print(row, cand, "\n")
				if cand.issubset(row):
					# print("found a subset")
					candidates[k][cand] += 1

		for cand in candidates[k]:
			count = float(candidates[k][cand])
			#print("\n\ncand: ", cand, "\nsupport: ", (count/float(max_rows)))
			if count / float(max_rows) > MIN_SUPPORT:
				# print(count/float(max_rows))
				frequent[k][cand] = count
				
		if len(frequent[k])==0:
			break

		k+=1
	return frequent

def getCount(row, candidates):
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

	return candidates

def candidateGen(n, candidates, frequent):
	# print(n)
	temp = frequent[n-1]
	candidates.append({})
	for i in temp:
		for j in temp:
#			newset = frozenset([i,j])
			newset = i | j

			#print(i, j, newset)
			if (len(newset) == n) and (newset not in candidates[n]):
				candidates[n][newset] = 0	#candidates[n][{ + [[temp[i], temp[j]]]

	return candidates

# ----------------------------------------------------
# CALCULATE CONFIDENCE
# ----------------------------------------------------

def genRules(data, minConf, frequent):
	rules = {}

	for group in frequent:
		#print("Group: ", group)
		for items in group:
			if len(items) <= 1:
				break
			for val in items:
				b = frozenset([val])
				a = items - b

				conf, sup = confidence(data, a, b)
				if conf >= minConf:
					not_sky = False
					subset_keys = []
					for key in iter(rules):
						if(items > key and key not in subset_keys):
							subset_keys += [key]

						elif(items < key):
							not_sky = True

						else:
							pass

					if not not_sky:

						#print("a: ", a, "b: ", b)
						if items in rules:
							#print("adding to key:", items)
							rules[items] += [[a, b, conf, sup]]

						else:
							#print("new key: ", items)
							rules[items] = [[a, b, conf, sup]]

					for key in subset_keys:
						del rules[key]

	#parse_output(rules)
	return rules


def confidence(data, itemset, v):
	num_items = 0
	num_matches = 0
	row_count = 0
	for i in range((data.shape[0])):
		row_count+=1
		row_as_set = frozenset(list(data.iloc[i, :]))
		if itemset.issubset(row_as_set):
			num_items+=1

			if v.issubset(row_as_set):
				num_matches+=1

	# print("Found {}/{}".format(num_matches, num_items))
	if num_items == 0:
		return 0.0

	conf = float(num_matches)/float(num_items)
	sup = num_matches/row_count

	return (conf, sup)



def remove_val(items, v):
	temp = []

	for i in items:
		if i != v:
			temp.append(i)
	
	return temp

def calc_conf(data, itemset, v):
	num_items = 0
	num_matches = 0
	
	# print("Evaluating set {} with item {}".format(itemset, v))
	for i, row in data.iterrows():
		found = [False]*len(itemset)
		has_v = False
		i = 1
		while i < len(row):
			j = 0
			while j < len(itemset):
				if itemset[j] == row[i]:
					found[j] = True
				elif v == row[i]:
					has_v = True
				j += 1
		if checkFound(found):
			num_items += 1
			num_matches += has_v
		i += 1 
	
	# print("Found {}/{}".format(num_matches, num_items))

	if num_items == 0:
		return 0.0
	return float(num_matches)/float(num_items)

def checkFound(list):
	for l in list:
		if l == False:
		 return False
	return True

# ----------------------------------------------------
# PARSING FUNCTIONS
# ----------------------------------------------------

def weed_out(rules):
	vals = [0]*50
	for r in rules:
		rule = r[0]
		for v in rule:
			indices = []
			removed = False
			if vals[v] != 0:
				rules.remove(r)
				removed = True
				break
			else:
				indices.append(v)
		if not removed:
			for i in indices:
				vals[i] += 1
	
	return rules
		 
		 
def parse_good_labels(data):
	labels = {}
	for i, row in data.iterrows():
		#print(row)
		labels[row["Id"]] = row['Flavor'][1:-1] + " " + row['Food'][1:-1]

	return labels

def parse_author_labels(data):
	labels = {}
	for i, row in data.iterrows():
		#print(row)
		labels[row["Id"]] = row['Name']# + " " + row['Food'][1:-1]

	return labels

# skylines is a list of [set, a, b, confidence]
# given a -> b	and set = a + b
def parse_output(rules, labels):
	print("Minimum Support: {}".format(MIN_SUPPORT))
	print("Minimum Confidence: {}".format(MIN_CONF))
	print("")
	for key in rules:
		#print("rules: ", rules[key])
		for rule in rules[key]:
			a = rule[0]
			b = rule[1]
			conf = rule[2]*100
			sup = rule[3]*100

			a_string = ""
			b_string = ""
			count = 0
			for entry in list(a):
				if(count>0):
					a_string += " and "
				a_string += labels[entry]
				count+=1

			for entry in list(b):
				b_string += labels[entry]

			#print("Given set {}".format(key))
			print("{} ---> {} \t\t[sup={} conf={}]".format(a_string, b_string, sup, conf))
			#print("")

def parse_output2(rules, labels):
	print("Minimum Support: {}".format(MIN_SUPPORT))
	print("Minimum Confidence: {}".format(MIN_CONF))
	print("")
	for key in rules:
		#print("rules: ", rules[key])
		for rule in rules[key]:
			a = rule[0]
			b = rule[1]
			conf = rule[2]*100
			sup = rule[3]*100

			#print("Given set {}".format(key))
			print("[sup={} conf={}]".format( sup, conf))


class mySets:
	def __init__(self, subset, count):
		self.subset = subset
		self.count = count


if __name__ == "__main__":
	 main()
