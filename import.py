import pandas as pd

class Importer:
   def import_csv(self, file):
      df = pd.read_csv(file)
      return df

im = Importer()

example = im.import_csv("../data/1000/1000i.csv")