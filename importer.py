import pandas as pd
import numpy as np

# ALL SPARSE FILES
SPARSE_FILES = ['data/apriori/1000/1000-out1.csv', 'data/apriori/5000/5000-out1.csv', 'data/apriori/20000/20000-out1.csv',
   'data/apriori/75000/75000-out1.csv']

# Imports sparse csv and returns the Pandas df
# WARNING: csv must include column names on first line
class Importer:
   def import_sparse(self, inf):
      chunksize = 10       # perhaps try some different values here?
      chunks = pd.read_csv( inf, chunksize=chunksize, dtype={'txt':'category'} )
      df = pd.concat( chunk.to_sparse(fill_value=0.0) for chunk in chunks )
      return df
   
   def import_csv(self, inf):
      df = pd.read_csv(inf)
      return df

   def import_psv(self, inf):
      df = pd.read_csv(inf, sep="\ \|\ ", header=None, names={'Id', 'Name'})#, dtype = {'id':np.int32, 'name':str})
      return df
   
   def import_list(self, files, file_type="sparse"):
      dfs = []
      if file_type == 'sparse':
         dfs = [self.import_sparse(f) for f in files]
      else:
         dfs = [self.import_csv(f) for f in files]
      return dfs

# TESTING
'''
im = Importer()
tests = im.import_list(SPARSE_FILES[1:3])
for t in tests:
   print(t)

   '''
