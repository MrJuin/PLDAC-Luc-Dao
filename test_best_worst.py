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

