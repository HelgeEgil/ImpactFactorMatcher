import pandas as pd
import pprint

df = pd.read_excel("NVI - 1936 HAUKELAND 2022.xlsx")
# print(df.columns)
# print(df.ISSN)
# print(df.PUBLISERINGSKANALNAVN)

issn = set(df.ISSN)
print(issn)
print(len(issn))
