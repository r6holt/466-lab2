from importer import Importer
import sys
import pandas as pd

'''data is the market baskets, items is the items, minSup is the threshold for support'''

MIN_SUPPORT = .1
MIN_CONF = .6
goods = [0]*50
max_rows = 0
candidates = [[], []]
counts = []

def main():
   #  inf = open(sys.argv[1], 'r')
   #  print(sys.argv[1])
   im = Importer()
   example1 = im.import_sparse("data/example/out1.csv")
   support_1(example1)
   fillCandidates(2)

   for row in candidates:
       print(row)
   #print(candidates)

def support_1(data, n):
   max_rows = 0
   for row in data.iterrows():
      getCount(row[1])
      max_rows += 1
   
   i = 0
   while i < len(goods):
      print(i, goods[i], max_rows)
      if float(goods[i])/float(max_rows) > MIN_SUPPORT:
         candidates[1].append(i)
      i += 1

def support_n(my_set, n)
   max_rows = 0
   for row in data.iterrows():
      getCount(row[1])
      max_rows += 1

   i = 0
   while i < len(goods):
      print(i, goods[i], max_rows)
      if float(goods[i])/float(max_rows) > MIN_SUPPORT:
         candidates[1].append(i)
      i += 1


# def support2(T, X, Y):
#     F[0] = support(T, I, minSup)
#     k=1
    
#     while(1):
#        C[k] = candidateGen(F[k], key)
#        for c in C[k]:
#            count[c] = 0

#         for t in T:
#             for c in C[k]:
#                 if(c in t):
#                     count[c] += 1

#         F[k] = those in C[k] if support > min support
#         k = k+1
    


'''   
   total = data["itemsd"].max()
    
    print(data['1'].value_counts())

    support = 0

    print("dataotal: ", total, "\ncandidatesount: ", count, "\nSupport: ", support)
'''
def getCount(row):
    i = 1
    while i < len(row):
      if not pd.isna(row[i]):
         goods[int(row[i])] += 1
      i += 1

def fillCandidates(n):
    temp = frequent[n-1]
    candidates.append([])
    for i in range(len(temp)-1):
        for j in range(i+1, len(temp)):
            candidates[n] = candidates[n] + [[temp[i], temp[j]]]


if __name__ == "__main__":
    main()
