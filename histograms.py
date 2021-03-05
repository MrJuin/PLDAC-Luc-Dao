# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 19:01:07 2021

@author: Luc
"""
from auteurs import Traitement
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

file1 = open("./data/test_final.csv", encoding="utf8")
file2 = open("./data/valid_final.csv", encoding="utf8")
file3 = open("./data/train_final.csv", encoding="utf8")

politicians_info = open("./data/dataset.xls", encoding="utf8")

content = file3.read() + "\n" + file2.read() + "\n" + file3.read()
content2 = politicians_info.read()

col = Traitement.text_traitement(content)
col_author = Traitement.author_traitement(content2)

mat_job = np.array([d.info["job"] for d in col])
ind_pers = np.where(mat_job != '')[0]

mat = np.array([d.info["counters"] for d in np.array(col)[ind_pers]], dtype = np.float32)

"""
Différentes distribution des sentiments,fake_note, subject, context, author, 
job, party et state
"""

# JOB
list_job = np.unique(mat_job)[1:] # On ne prend pas les non-jobs
dict_job = dict(list(zip(list_job, np.arange(len(list_job)))))
hist_job = [dict_job[i] for i in mat_job[ind_pers]]


fig, ax = plt.subplots(1,1, figsize=(100,100))
ax.hist(hist_job, bins = range(len(list_job)))
ax.set_xticks(np.arange(len(list_job)))
ax.set_xticklabels(list_job,rotation=90,fontsize=8)
