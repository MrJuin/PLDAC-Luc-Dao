# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 19:01:07 2021

@author: Luc
"""
from auteurs import Traitement
import numpy as np

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


#barely true, false, half true, mostly true, pant on fire

t1 = mat[:,[1,4]].sum(axis = 1) 
t2 = (mat.sum(axis = 1) + 1e-4)
bestwrong = np.argmax(t1 / t2)
bestwrong2 = np.argmax(t1)
wrong  = col[ind_pers[bestwrong]]
wrong2 = col[ind_pers[bestwrong2]]

bestliar = np.argmax(mat[:,4])
liar = col[ind_pers[bestliar]]