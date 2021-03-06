# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 19:01:07 2021

@author: Luc
"""
from utils.auteurs import Traitement
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

file1 = open("../data/test_final.csv", encoding="utf8")
file2 = open("../data/valid_final.csv", encoding="utf8")
file3 = open("../data/train_final.csv", encoding="utf8")

politicians_info = open("../data/dataset.xls", encoding="utf8")

content = file3.read() + "\n" + file2.read() + "\n" + file3.read()
content2 = politicians_info.read()

col = Traitement.text_traitement(content)
col_author = Traitement.author_traitement(content2)

dictio_author = {}
dictio = {'author' : {}, 'job' : {}, 'state' : {}, 'party' : {},\
          'nbr_mess' : {}, 'score' : {}}
num = ['true','barely-true', 'false', 'half-true', 'mostly-true', 'pants-fire']

for doc in range(len(col)):
    if col[doc].info["job"] != '':
        
        author = " ".join(col[doc].info['author'])
        try:
            dictio_author[author]
            
        except KeyError:
            dictio_author[author] = {}
            dictio_author[author]["party"] = col[doc].info["party"]
            dictio_author[author]["job"]   = col[doc].info["job"]
            dictio_author[author]["state"] = col[doc].info["state"]
            dictio_author[author]["true_score"] = [0]*6
            dictio_author[author]["score"] = np.float32(col[doc].info["counters"])
            dictio_author[author]["news"]  = np.array([], dtype = np.intc)
                    
        n = num.index(col[doc].info['fake_note'])
        dictio_author[author]["true_score"][n] += 1
        dictio_author[author]["news"] = np.append(dictio_author[author]["news"], doc)
        
        
dictio_author2 = {}
for doc in col_author:
    author = " ".join(doc.info.pop('name'))
    dictio_author2[author] = doc.info

both = set(dictio_author.keys()).intersection(dictio_author2.keys())

        
#tmp = np.array(list(job_dic.values()))

#df = pd.DataFrame(data = dict)