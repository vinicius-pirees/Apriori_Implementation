from apriori_implementation import apriori
import pandas
import numpy as np
import os

file_path = os.path.realpath('..') + '/apriori_implementacao/resources/t25i10d10_transformed.txt'

raw = pandas.read_csv(file_path, header=None)

def transform(row):
    return row.strip().replace(' ', ',')

transactions = raw[0].apply(transform)

dataset_size = transactions.shape[0]

transactions_list = []
for i in range(dataset_size):
    transactions_list.append(transactions[i])

data = {'col': transactions_list}

df = pandas.DataFrame.from_dict(data)

apriori(df, 0.8, 0.95)

