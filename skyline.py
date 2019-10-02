import importer
import sys

'''T is the market baskets, I is the items, minSup is the threshold for support'''

def main():
    inf = open(sys.argv[1], 'r')
    print(sys.argv[1])


def support(T, X, Y):
    F[0] = support(T, I, minSup)
    k=1
    
    while(1):
       C[k] = candidateGen(F[k], key)
       for c in C[k]:
           count[c] = 0

        for t in T:
            for c in C[k]:
                if(c in t):
                    count[c]++

        F[k] = those in C[k] if support > min support
        k = k+1
    


        if(F[k]==0):
            break

'''   
   total = T["Id"].max()
    
    print(T['1'].value_counts())

    support = 0

    print("Total: ", total, "\nCount: ", count, "\nSupport: ", support)
'''
def getCount(T, x):
    for idx, tuple in T.iterrows():
        print(idx, tupel);


if __name__ == "__main__":
    main()
