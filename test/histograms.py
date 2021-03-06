# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 19:01:07 2021

@author: Luc
"""
from utils.auteurs import Traitement
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils.auteurs import make_dictio
import pandas as pd

statement_file1 = open("../data/test_final.csv", encoding="utf8")
statement_file2 = open("../data/valid_final.csv", encoding="utf8")
statement_file3 = open("../data/train_final.csv", encoding="utf8")

politicians_file = open("../data/dataset.xls", encoding="utf8")

content = statement_file3.read() + "\n" + statement_file2.read()\
          + "\n" + statement_file3.read()

content2 = politicians_file.read()

statements = Traitement.text_traitement(content)
politicians = Traitement.author_traitement(content2)

dict_statement, dict_politician = make_dictio(statements, politicians)

both = set(dict_statement.keys()).intersection(dict_politician.keys())

dictio = {'author' : [], 'job' : [], 'state' : [], 'true_score' : [],\
          'score' : []}

for author, values in dict_statement.items():
    dictio['author'] += [author]
    dictio['job']    += [values['job']]
    dictio['state']  += [values['state']]
    dictio['true_score']    += [values['true_score']]
    dictio['score']    += [values['score']]

#dictio['true_score'] = np.array(dictio['true_score']) 
#dictio['score'] = np.array(dictio['score'] ) 

df = pd.DataFrame(data = dictio)


sns.set_theme(style="darkgrid")

sns.displot(df, x="state", col="job",binwidth=3, height=3)