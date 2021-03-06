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



        
#tmp = np.array(list(job_dic.values()))

#df = pd.DataFrame(data = dict)